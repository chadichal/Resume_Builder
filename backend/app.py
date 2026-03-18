from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
import random

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ MODELS ------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class OTPVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    otp = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # updated (no warning)

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('index.html')

# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        otp = str(random.randint(100000, 999999))
        print(f"OTP for {email}: {otp}")

        session['email'] = email
        session['password'] = password

        otp_record = OTPVerification(email=email, otp=otp)
        db.session.add(otp_record)
        db.session.commit()

        return redirect(url_for('verify_otp'))

    return render_template('register.html')

# -------- VERIFY OTP --------
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        email = session.get('email')

        record = OTPVerification.query.filter_by(email=email).first()

        if record and record.otp == entered_otp:
            user = User(email=email, password=session['password'])
            db.session.add(user)
            db.session.delete(record)
            db.session.commit()

            return redirect(url_for('login'))

        return "Invalid OTP"

    return render_template('verify_otp.html')

# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))

        return "Login Failed"

    return render_template('login.html')

# -------- DASHBOARD --------
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------- CREATE RESUME --------
@app.route('/create-resume')
@login_required
def create_resume():
    return render_template('resume_form.html')

# -------- FIX FOR /resume --------
@app.route('/resume')
@login_required
def resume_redirect():
    return redirect(url_for('create_resume'))

# -------- LOGOUT --------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------ RUN ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)