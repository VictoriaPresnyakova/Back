from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    jwt_token = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    products = db.relationship('Product', back_populates='user')
