from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from sqlalchemy.testing.pickleable import User
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email Does Not Exist', category='error')


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exist', category='error')

        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(first_name) < 1:
            flash('First name must be at least 1 character', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user) #creates new user in the database
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)

@auth.route('/minor', methods=['GET', 'POST'])
def minor():
    if request.method == 'POST':
        # Geometric Input
        t = float(request.form.get('thickness'))
        d = float(request.form.get('depth'))
        Lb = float(request.form.get('length'))
        e = float(request.form.get('eccentricity'))
        P_max = float(request.form.get('maxload'))

        # Constants
        # Yield Strength (ksi)
        Fy = float(36)
        # Modulus of Elasticity (ksi)
        E = float(29000)
        # Lateral-torsional buckling modification factor
        Cb = float(1)

        # Modulus Calculation
        Z = float(((d * t * t)) / 4)
        S = float(((d * t * t)) / 6)

        # Check yielding for rectangular bars bent about minor axis (AISC F11-1)
        My_1_6 = float((1.6 * Fy * S) / 12)
        Mp = float((Z * Fy) / 12)
        Mn = min(Mp, My_1_6)

        # Determine maximum allowable applied load
        P_all = ((Mn / 1.67) / (e / 12))

        # Bending Strength Unity Check
        Unity = P_max / P_all

        if Unity <= 1:
            flash('Analysis Complete: Pass - Unity = ' + str(Unity.__round__(2)), category='message')
        else:
            flash('Analysis Complete: Fail - Unity = ' + str(Unity.__round__(2)), category='error')

    return render_template("minor.html", user=current_user)

@auth.route('/major', methods=['GET', 'POST'])
def major():
    if request.method == 'POST':
        # Geometric Input
        t = float(request.form.get('thickness'))
        d = float(request.form.get('depth'))
        Lb = float(request.form.get('length'))
        e = float(request.form.get('eccentricity'))
        P_max = float(request.form.get('maxload'))

        # Constants
        # Yield Strength (ksi)
        Fy = float(36)
        # Modulus of Elasticity (ksi)
        E = float(29000)
        # Lateral-torsional buckling modification factor
        Cb = float(1)

        # Modulus Calculation
        Z = float(((t * d * d)) / 4)
        S = float(((t * d * d)) / 6)

        # Check yielding for rectangular bars bent about minor axis (AISC F11-1)
        print()
        Lbd_t2 = float(Lb * d) / (t * t)
        E08_Fy = float((0.08 * E) / Fy)
        E19_Fy = float((1.9 * E) / Fy)
        My = float(Fy * S) / 12
        Mp = float(Fy * Z) / 12
        if Lbd_t2 <= E08_Fy:
            My_1_6 = float((1.6 * Fy * S) / 12)
            Mp = float((Z * Fy) / 12)
            Mn = min(Mp, My_1_6)


        # Check lateral torsional buckling (AISC F11-2)
        else:
            if Lbd_t2 <= E19_Fy and E08_Fy < Lbd_t2:
                Mn = min(float(Cb * (1.52 - 0.274 * (Lbd_t2) * (Fy / E)) * My), Mp)
            else:
                if E19_Fy < Lbd_t2:
                    Fcr = float((1.9 * E * Cb) / Lbd_t2)
                    Mn = min((Fcr * S), Mp)


        # Determine maximum allowable applied load
        P_all = float((Mn / 1.67) / (e / 12))

        # Bending Strength Unity Check
        Unity = P_max / P_all


        if Unity <= 1:
            flash('Analysis Complete: Pass - Unity = ' + str(Unity.__round__(2)), category='message')
        else:
            flash('Analysis Complete: Fail - Unity = ' + str(Unity.__round__(2)), category='error')


    return render_template("major.html", user=current_user)

