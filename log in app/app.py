from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "superusersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email address already exists, Please Log in.', 'danger')
            return redirect(url_for('login'))
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        found_user = User.query.filter_by(email=email).first()
        if found_user and check_password_hash(found_user.password, password):
            session['user_id'] = found_user.id
            session['user_name'] = found_user.name
            flash('Login successful!', 'success')
            return redirect(url_for('landing'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/landing')
def landing():
    user_name = session.get('user_name')
    if user_name:
        return render_template('landing.html', user=user_name)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)