# views.py
from app import app, db, csrf
from app.models import Users, Profile, Favourite
from flask import request, jsonify, send_from_directory
import jwt
import datetime
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from flask_wtf.csrf import generate_csrf
import os
from app.forms import ProfilePhotoForm
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


SECRET_KEY = app.config['SECRET_KEY']

###
# Helper Functions
###

def form_errors(form):
    """Collect form errors from Flask-WTF"""
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = Users.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



###
# Routes
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@csrf.exempt
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    photo = data.get('photo', None)

    if not all([username, password, name, email]):
        return jsonify(message="Missing required registration fields."), 400

    if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
        return jsonify(message="User with this username or email already exists"), 409
 
    user = Users(username=username, password=password, name=name, email=email, photo=photo)
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201

@csrf.exempt
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify(token=token, user_id=user.id), 200

    return jsonify(message="Invalid username or password"), 401

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify(message="Logged out successfully")


from flask import make_response

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/uploads/<filename>', methods=['GET'])
def serve_profile_photo(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


@app.route('/api/users/<int:user_id>/photo', methods=['POST'])
@csrf.exempt  
@token_required
def upload_user_photo(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    form = ProfilePhotoForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

        user = Users.query.get_or_404(user_id)
        user.photo = filename
        db.session.commit()

        return jsonify(message="Photo uploaded", photo=filename), 201
    else:
        return jsonify(errors=form_errors(form)), 400

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from sqlalchemy import desc

@app.route('/api/profiles', methods=['GET'])
@token_required
def get_profiles(current_user):
    limit  = request.args.get('limit', 4, type=int)
    offset = request.args.get('offset', 0, type=int)

    query = Profile.query.filter(Profile.user_id_fk != current_user.id)

    query = query.order_by(desc(Profile.id))

    profiles = query.offset(offset).limit(limit).all()

    profiles_data = [{
        'id':           p.id,
        'user_id_fk':   p.user_id_fk,
        'description':  p.description,
        'parish':       p.parish,
        'sex':          p.sex,
        'race':         p.race,
        'birth_year':   p.birth_year,
        'height':       p.height,
        'fav_cuisine':  p.fav_cuisine,
        'fav_colour':   p.fav_colour,
        'fav_school_subject': p.fav_school_subject,
        'political':    p.political,
        'religious':    p.religious,
        'family_oriented': p.family_oriented,
        'photo':        p.user.photo if p.user else None,
        'user': {
          'name': p.user.name if p.user else None,
          'date_joined': p.user.date_joined.isoformat() if p.user else None
        }
    } for p in profiles]

    return jsonify(profiles=profiles_data)




@csrf.exempt
@app.route('/api/profiles', methods=['POST'])
@token_required
def add_profile(current_user):
    data = request.get_json()

    profile_count = Profile.query.filter_by(user_id_fk=current_user.id).count()
    if profile_count >= 3:
        return jsonify(message="You cannot have more than 3 profiles"), 403

    required_fields = ['description', 'parish', 'biography', 'sex', 'race', 'birth_year', 'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject']
    for field in required_fields:
        if not data.get(field):
            return jsonify(message=f"Missing field: {field}"), 400

    profile = Profile(
        user_id_fk=current_user.id,
        description=data['description'],
        parish=data['parish'],
        biography=data['biography'],
        sex=data['sex'],
        race=data['race'],
        birth_year=data['birth_year'],
        height=data['height'],
        fav_cuisine=data['fav_cuisine'],
        fav_colour=data['fav_colour'],
        fav_school_subject=data['fav_school_subject'],
        political=data.get('political', False),
        religious=data.get('religious', False),
        family_oriented=data.get('family_oriented', False)
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({
    "message": "Profile created successfully",
    "profile": {
        "id": profile.id,
        "description": profile.description,
        "parish": profile.parish,
        "biography": profile.biography,
        "sex": profile.sex,
        "race": profile.race,
        "birth_year": profile.birth_year,
        "height": profile.height,
        "fav_cuisine": profile.fav_cuisine,
        "fav_colour": profile.fav_colour,
        "fav_school_subject": profile.fav_school_subject,
        "political": profile.political,
        "religious": profile.religious,
        "family_oriented": profile.family_oriented,
        "user_id_fk": profile.user_id_fk
    }
}), 201


@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@token_required
def get_profile(current_user, profile_id):
    profile = Profile.query.get_or_404(profile_id)
    user = Users.query.get_or_404(profile.user_id_fk)

    profile_data = {
        'id': profile.id,
        'description': profile.description,
        'parish': profile.parish,
        'biography': profile.biography,
        'sex': profile.sex,
        'race': profile.race,
        'birth_year': profile.birth_year,
        'height': profile.height,
        'fav_cuisine': profile.fav_cuisine,
        'fav_colour': profile.fav_colour,
        'fav_school_subject': profile.fav_school_subject,
        'political': profile.political,
        'religious': profile.religious,
        'family_oriented': profile.family_oriented,
        'user': {
            'name': user.name,
            'email': user.email,
            'photo': user.photo
        }
    }

    return jsonify(profile=profile_data)


@csrf.exempt
@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@token_required
def favourite_profile(current_user, user_id):
    data = request.get_json()
    fav_profile_id = data['fav_user_id_fk']

    existing_fav = Favourite.query.filter_by(user_id_fk=current_user.id, fav_user_id_fk=fav_profile_id).first()
    if existing_fav:
        return jsonify(message="Already favourited"), 409

    fav = Favourite(user_id_fk=current_user.id, fav_user_id_fk=fav_profile_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify(message="Profile added to favourites"), 201

@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@token_required
def get_matches(current_user, profile_id):
    me = Profile.query.get_or_404(profile_id)
    
    candidates = Profile.query.filter(
        Profile.id != me.id,
        Profile.user_id_fk != current_user.id
    ).all()

    results = []
    for p in candidates:
    
        age_ok = abs(me.birth_year - p.birth_year) <= 5

    
        height_diff_inches = abs(me.height - p.height) 
        height_ok = 3 <= height_diff_inches <= 10

        field_matches = sum([
            me.fav_cuisine       == p.fav_cuisine,
            me.fav_colour        == p.fav_colour,
            me.fav_school_subject== p.fav_school_subject,
            me.political         == p.political,
            me.religious         == p.religious,
            me.family_oriented   == p.family_oriented,
        ])
        fields_ok = field_matches >= 3

        if age_ok and height_ok and fields_ok:
            results.append({
                'id':           p.id,
                'description':  p.description,
                'parish':       p.parish,
                'sex':          p.sex,
                'race':         p.race,
                'birth_year':   p.birth_year,
                'height':       p.height,
                'photo': p.user.photo if p.user else None,
                'matches':      field_matches
            })

    return jsonify(matches=results)


@app.route('/api/search', methods=['GET'])
@token_required
def search_profiles(current_user):
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')


    query = Profile.query.join(Users).filter(Profile.user_id_fk != current_user.id)


    if name:
        query = query.filter(Profile.description.ilike(f'%{name}%'))
    if birth_year:
        query = query.filter(Profile.birth_year == int(birth_year))
    if sex:
        query = query.filter(Profile.sex == sex)
    if race:
        query = query.filter(Profile.race == race)

    profiles = query.all()

    results = [{
    'id': p.id,
    'description': p.description,
    'parish': p.parish,
    'sex': p.sex,
    'race': p.race,
    'birth_year': p.birth_year,
    'photo': p.user.photo if p.user else None,
    'user': {
        'name': p.user.name if p.user else "User",
        'date_joined': p.user.date_joined.isoformat() if p.user else None
    }
} for p in profiles]


    return jsonify(results=results)

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_details(current_user, user_id):
    user = Users.query.get_or_404(user_id)

    profiles = Profile.query.filter_by(user_id_fk=user.id).all()
    profiles_data = [{
        'id': p.id,
        'description': p.description
    } for p in profiles]

    return jsonify(user={
        'id':           user.id,
        'name':         user.name,
        'email':        user.email,
        'photo':        user.photo,
        'date_joined':  user.date_joined.isoformat(),
        'profiles':     profiles_data
    })


@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
@token_required
def get_user_favourites(current_user, user_id):
    favourites = Favourite.query.filter_by(user_id_fk=user_id).all()

    favs = []
    for f in favourites:
        p = Profile.query.get(f.fav_user_id_fk)
        if not p:
            continue

        if p.user_id_fk == current_user.id:
            continue

        favs.append({
            'id': p.id,
            'description': p.description,
            'parish': p.parish,
            'sex': p.sex,
            'race': p.race,
            'birth_year': p.birth_year,
            'height': p.height,
            'photo': p.user.photo if p.user else None,
        })

    return jsonify(favourites=favs)



@app.route('/api/users/favourites/<int:N>', methods=['GET'])
@token_required
def get_top_favourites(current_user, N):
    query = (
        db.session
          .query(Profile, db.func.count(Favourite.id).label('count'))
          .join(Favourite, Favourite.fav_user_id_fk == Profile.id)
          .filter(Profile.user_id_fk != current_user.id)
          .group_by(Profile.id)
    )

    top = query.limit(N).all()

    result = [{
        'id':           profile.id,
        'description':  profile.description,
        'parish':       profile.parish,
        'race':         profile.race,
        'sex':          profile.sex,
        'birth_year':   profile.birth_year,
        'photo':        profile.user.photo if profile.user else None,
        'favorite_count': count
    } for profile, count in top]

    return jsonify(top_favourites=result)

###
# Render
###
from flask import Blueprint

frontend = Blueprint('frontend', __name__)

@frontend.route('/', defaults={'path': ''})
@frontend.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists("dist/" + path):
        return send_from_directory('dist', path)
    else:
        return send_from_directory('dist', 'index.html')

###
# Error Handlers
###
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return jsonify(message="Resource not found."), 404
