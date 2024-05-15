from app import db, login
from app.search import SearchableMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    username = db.Column(db.String(16), unique=True, index=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(64), unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    instagram_link = db.Column(db.String(256))
    telegram_link = db.Column(db.String(256))
    items = db.relationship('Item', back_populates='seller', lazy=True)
    carts = db.relationship('Cart', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    items = db.relationship('Item', back_populates='category', lazy=True)

class Item(SearchableMixin, db.Model):
    __tablename__ = 'item'
    __searchable__ = ['item_name']
    id = db.Column(db.Integer, primary_key=True)
    images = db.Column(db.String, default='default.png')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_item_category_id'))
    category = db.relationship('Category', back_populates='items', lazy=True)
    item_name = db.Column(db.String(126), nullable=False)
    item_desc = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.String, db.ForeignKey('status.id', name='fk_item_status_id'))
    item_status = db.relationship('Status', back_populates='items', lazy=True)
    price = db.Column(db.Integer, default='')
    price_currency = db.Column(db.String, default="ETB")
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_item_user_id'), index=True)
    seller = db.relationship('User', back_populates='items', lazy=True)
    carts = db.relationship('Cart', back_populates='items', lazy=True)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default='Not Mentioned.')
    items = db.relationship('Item', back_populates='item_status', lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_cart_user_id'), index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', name='fk_cart_item_id'))
    quantity = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='carts', lazy=True)
    items = db.relationship('Item', back_populates='carts', lazy=True)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)