# seed.py
from app import app, db
from app.models import Users, Profile, Favourite

def seed_users():
    print("Clearing dependent tables...")
    Favourite.query.delete()
    Profile.query.delete()
    Users.query.delete()
    db.session.commit()

    print("🌱 Seeding new users...")
    users = [
        Users(username="amara.sterling", password="password123", name="Amara Sterling", email="amara@example.com"),
        Users(username="zane.thompson", password="password123", name="Zane Thompson", email="zane@example.com"),
        Users(username="jasmine.chen", password="password123", name="Jasmine Chen", email="jasmine@example.com"),
        Users(username="malik.johnson", password="password123", name="Malik Johnson", email="malik@example.com"),
        Users(username="isabella.rivera", password="password123", name="Isabella Rivera", email="isabella@example.com"),
        Users(username="ravi.kapoor", password="password123", name="Ravi Kapoor", email="ravi@example.com"),
        Users(username="tahlia.browne", password="password123", name="Tahlia Browne", email="tahlia@example.com"),
        Users(username="ezekiel.brooks", password="password123", name="Ezekiel Brooks", email="ezekiel@example.com"),
        Users(username="lucia.dsouza", password="password123", name="Lucia D'Souza", email="lucia@example.com"),
        Users(username="kai.williams", password="password123", name="Kai Williams", email="kai@example.com"),
        Users(username="aaliyah.grant", password="password123", name="Aaliyah Grant", email="aaliyah@example.com"),
        Users(username="noah.sinclair", password="password123", name="Noah Sinclair", email="noah@example.com"),
        Users(username="sasha.petrova", password="password123", name="Sasha Petrova", email="sasha@example.com"),
        Users(username="jamari.lewis", password="password123", name="Jamari Lewis", email="jamari@example.com"),
        Users(username="chloe.summers", password="password123", name="Chloe Summers", email="chloe@example.com"),
        Users(username="mateo.reyes", password="password123", name="Mateo Reyes", email="mateo@example.com"),
        Users(username="nyla.walker", password="password123", name="Nyla Walker", email="nyla@example.com"),
        Users(username="omar.khan", password="password123", name="Omar Khan", email="omar@example.com"),
        Users(username="gianna.moretti", password="password123", name="Gianna Moretti", email="gianna@example.com"),
        Users(username="dante.richards", password="password123", name="Dante Richards", email="dante@example.com")
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Seeded 20 users successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_users()
