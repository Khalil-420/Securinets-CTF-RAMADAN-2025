from main import db, User, app, strongpassword
from random import randint
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    db.session.query(User).delete()
    u = User(username="KonaN.g7q9g4ea7q@seurinets.tekup", password=generate_password_hash(strongpassword), avatar="/assets/img/KonaN.png", role=2, totp_secret=1337)
    db.session.add(u)
    db.session.commit()