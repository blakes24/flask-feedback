from app import db
from models import User, Feedback

db.drop_all()
db.create_all()

u = User.register(username="jane123", email="jane@jane.com", pwd="terriblepassword", first_name="Jane", last_name="Doe")
db.session.add(u)
db.session.commit()

f = Feedback(title="Password", content="NVM my bad", username="jane123")

db.session.add(f)
db.session.commit()