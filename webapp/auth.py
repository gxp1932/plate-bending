from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/register')
def register():
    return "<p>Register</p>"

@auth.route('/minor')
def minor():
    return "<p>Steel Plate in Minor Axis Bending Analysis</p>"

@auth.route('/major')
def major():
    return "<p>Steel Plate in Major Axis Bending Analysis</p>"

