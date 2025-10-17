from flask import Flask, jsonify
from flask_cors import CORS # Import CORS
# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable CORS for your app

# Define the data that our frontend will fetch
def get_link_data():
    """
    This function returns a dictionary containing all the profile data.
    In the future, this data will come from a database.
    """
    return {
        "profile_picture_url": "profile.png",
        "username": "@adtya",
        "bio": "A short and catchy bio about you! (Now from the backend!)",
        "links": [
            {
                "title": "GitHub",
                "url": "https://github.com/a-dtya"
            },
            {
                "title": "Twitter",
                "url": "https://twitter.com/yourusername"
            },
            {
                "title": "LinkedIn",
                "url": "https://www.linkedin.com/in/yourusername/"
            },
            {
                "title": "My Personal Blog",
                "url": "https://yourblog.com"
            }
        ]
    }

@app.route('/api/data')
def get_data():
    """
    This is our API endpoint. When the frontend requests this URL,
    it will send back our data in JSON format.
    """
    data = get_link_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)