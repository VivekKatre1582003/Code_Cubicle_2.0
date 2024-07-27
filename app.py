from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['APPROVED_FOLDER'] = 'static/approved'
app.config['SECRET_KEY'] = 'your_secret_key'  # Set your secret key here
db = SQLAlchemy(app)

# Create upload and approved directories if they do not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['APPROVED_FOLDER'], exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.String(500), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    points = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('user_page'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('user_page'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or not request.form['address'] or not request.form['problem']:
        flash('Please provide all required fields and a file.')
        return redirect(url_for('user_page'))
    
    if 'user_id' not in session:
        flash('Please log in to upload files.')
        return redirect(url_for('login'))

    file = request.files['file']
    address = request.form['address']
    problem = request.form['problem']
    user_id = session['user_id']
    
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('user_page'))
    
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    new_submission = Submission(user_id=user_id, image_path=filename, address=address, problem=problem)
    db.session.add(new_submission)
    db.session.commit()
    
    return redirect(url_for('status'))

@app.route('/status')
def status():
    if 'user_id' not in session:
        flash('Please log in to view the status.')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    submissions = Submission.query.filter_by(user_id=user_id).all()
    return render_template('status.html', submissions=submissions)

@app.route('/user')
def user_page():
    if 'user_id' not in session:
        flash('Please log in to view your page.')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    submissions = Submission.query.filter_by(user_id=user_id).all()
    return render_template('user_page.html', submissions=submissions)

@app.route('/admin')
def admin():
    submissions = Submission.query.filter_by(approved=False).all()
    return render_template('admin.html', submissions=submissions)

@app.route('/approve/<int:id>')
def approve(id):
    submission = Submission.query.get_or_404(id)
    if submission:
        submission.approved = True
        submission.points += 10
        approved_path = os.path.join(app.config['APPROVED_FOLDER'], os.path.basename(submission.image_path))
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], submission.image_path)
        os.rename(original_path, approved_path)
        submission.image_path = os.path.join('approved', os.path.basename(submission.image_path))
        db.session.commit()
        flash('Submission approved and points updated.')
    return redirect(url_for('approved'))

@app.route('/disapprove/<int:id>')
def disapprove(id):
    submission = Submission.query.get_or_404(id)
    if submission:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], submission.image_path))
        db.session.delete(submission)
        db.session.commit()
        flash('Submission disapproved and removed.')
    return redirect(url_for('admin'))

@app.route('/approved')
def approved():
    submissions = Submission.query.filter_by(approved=True).all()
    return render_template('approve.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
