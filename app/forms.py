# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProfilePhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpeg','jpg','png','gif'], 'Images only!')
    ])

    class Meta:
        csrf = False    # ← disable the form’s own CSRFField
