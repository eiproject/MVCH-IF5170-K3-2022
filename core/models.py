# import pytz
# from datetime import datetime

# # Change this to your server timezone
# tz = pytz.timezone('Asia/Jakarta')

# from core import db # , login_manager
# # from flask_login import UserMixin

# class Users(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(100), nullable=False)
#     date_registered = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=tz))
#     last_login = db.Column(db.DateTime, nullable=True)

# db.create_all()