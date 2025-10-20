from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS #type: ignore
from flask_sqlalchemy import SQLAlchemy #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'linkhub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'  # change in production
db = SQLAlchemy(app)
# -----------------------------

# --- Database Model Definitions ---
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), nullable=False, default="@yourusername")
    bio = db.Column(db.String(255), default="Your default bio")
    profile_picture_url = db.Column(db.String(255), default="/static/profile.png")

    links = db.relationship('Link', backref='profile', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "bio": self.bio,
            "profile_picture_url": self.profile_picture_url
        }


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url
        }

# --------------------------------
# --- Admin API Routes ---

@app.route('/api/profile', methods=['GET', 'POST'])
def manage_profile():
    """
    GET: Returns the current profile data.
    POST: Updates the profile data.
    """
    
    # Get the one-and-only profile (or create it if it's missing)
    profile = db.session.get(Profile, 1)
    if not profile:
        profile = Profile()
        db.session.add(profile)
    
    if request.method == 'POST':
        # Get data from the form's JSON body
        data = request.json
        
        # Update the profile object with new data
        profile.username = data.get('username', profile.username)
        profile.bio = data.get('bio', profile.bio)
        profile.profile_picture_url = data.get('profile_pic', profile.profile_picture_url)
        
        # Save the changes to the database
        db.session.commit()
        
        return jsonify({"message": "Profile updated successfully!", "profile": profile.to_dict()})

    # For a GET request, just return the current profile data
    return jsonify(profile.to_dict())
# --- Page-Serving Routes ---

@app.route('/')
def home_page():
    """ Serves the main index.html page. """
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    """ Serves the admin.html page. """
    return render_template('admin.html')

@app.route('/static/<path:path>')
def send_static(path):
    """ Serves static files (CSS, JS, images). """
    return send_from_directory('static', path)

# --- API Data Route ---

@app.route('/api/data')
def get_data():
    """
    Fetches all data from the database.
    This is the endpoint our JavaScript should call.
    """
    # Find the first profile, or create one if it doesn't exist
    profile = db.session.get(Profile, 1)
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    all_links = Link.query.all()
    
    data = {
        # The data is now nested
        "profile": profile.to_dict(),
        "links": [link.to_dict() for link in all_links]
    }
    return jsonify(data)

# SIGNUP
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    password = generate_password_hash(data['password'])
    
    if Profile.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = Profile(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = Profile.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({"token": token})
# --------------------------------

if __name__ == '__main__':
    # If you haven't, remember to create the new 'profile' table!
    # 1. 'py'
    # 2. 'from app import app, db'
    # 3. 'with app.app_context():'
    # 4. '    db.create_all()'
    # 5. 'exit()'
    app.run(debug=True)