from . import db
from passlib.hash import bcrypt
from flask import jsonify

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def generate_hash(password):
        return bcrypt.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return bcrypt.verify(password, hash)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class KeyValueModel(db.Model):
    __tablename__ = 'key_value'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    key = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(120), nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, user_id, key, value):
        item = cls.query.filter_by(key = key, user_id = user_id).first()
        item.value = value
        db.session.commit()

    @classmethod
    def get(cls, user_id, key):
        return cls.query.filter_by(user_id = user_id , key = key).first()
    
    @classmethod
    def exists(cls, user_id, key):
        query = cls.get(user_id, key)
        return bool(query)
    
    @classmethod
    def getAllForUser(cls, user_id):
        return jsonify([item.serialize for item in cls.query.filter_by(user_id = user_id).all()])


    @property
    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'key' : self.key,
            'value' : self.value
        }