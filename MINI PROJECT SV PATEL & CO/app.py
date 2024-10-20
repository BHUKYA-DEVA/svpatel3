
from flask import Flask, render_template, request, redirect, url_for,jsonify,flash,session
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from werkzeug.security import generate_password_hash, check_password_hash
import json 
from bson.objectid import ObjectId

app = Flask(__name__)
@app.route('/')
def index2():
    return render_template('index1.html')


@app.route('/index')
def index():
    return render_template('index.html')
           
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog_detail')
def blog_detail():
    return render_template('blog_detail.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/team_detail')
def team_detail():
    return render_template('team_detail.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')
@app.route('/logout')
def logout():
    # Add your logout logic here (e.g., clearing session)
    return redirect(url_for('login'))









# Route to delete feedback
@app.route('/delete_feedback/<feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    try:
        # Find and delete the feedback by its ID
        result = collection.delete_one({'_id': ObjectId(feedback_id)})

        if result.deleted_count == 1:
            flash('Feedback deleted successfully!', 'success')
        else:
            flash('Feedback not found!', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect(url_for('index1'))



# Connect to MongoDB

client = MongoClient('mongodb://localhost:27017/')
db = client['deva']  # Replace with your database name
collection = db['deva']  # Replace with your collection name

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()  # Get data from the form using JSON
        
        if not data:
            raise ValueError("No data provided")
        
        # Extracting data from request
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        # Insert into MongoDB
        collection.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'message': message
        })

        return jsonify({"success": True, "message": "Form submitted successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Connect to your MongoDB server
db = client['login_db']  # Use your MongoDB database
users_collection = db['users']  # Collection to store user information

# Default username and password setup (only for demonstration purposes)
DEFAULT_USERNAME = 'SVPATEL'
DEFAULT_PASSWORD = '1234'  # This should be hashed in a real application

# Check if default user exists, if not, create it
def initialize_default_user():
    if not users_collection.find_one({"username": DEFAULT_USERNAME}):
        hashed_password = generate_password_hash(DEFAULT_PASSWORD)
        users_collection.insert_one({
            "username": DEFAULT_USERNAME,
            "password": hashed_password
        })

initialize_default_user()

# Route for login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        username = data['username']
        password = data['password']

        # Find user by username
        user = users_collection.find_one({"username": username})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Verify the password
        if check_password_hash(user['password'], password):
            session['user'] = username  # Set user session
            return jsonify({"success": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for rendering the login form
@app.route('/login_form', methods=['GET'])
def login_form():
    return render_template('index.html')  # This should be the HTML file for the login form


# Dashboard placeholder route
@app.route('/dashboard')
def index1():
    # Fetch data from MongoDB
    items = collection.find()  # Retrieve all documents from the collection

    # Convert MongoDB Cursor to list of dictionaries
    items_list = list(items)
    
    # Render data using a template
    return render_template('admin_login.html', items=items_list)
    
    
    
    
    
    
    
    
    
client = MongoClient("mongodb://localhost:27017/")  # Connect to your MongoDB server
db = client['deva']  # Use your MongoDB database
collection = db['deva']  # Collection from which to retrieve data

if __name__ == '__main__':
    app.run(debug=True)