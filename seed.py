from app import db
from models import User

db.drop_all()
db.create_all()

u = User(username="jane123", email="jane@jane.com", password="terriblepassword", first_name="Jane", last_name="Doe")
db.session.add(u)
db.session.commit()
