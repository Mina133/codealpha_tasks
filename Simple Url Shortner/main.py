from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    long_url = db.Column(db.String(500), nullable=False)

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get("url")
    if not long_url:
        return jsonify({"error": "Missing URL"}), 400
    
    short_url = generate_short_url()
    while URLMapping.query.filter_by(short_url=short_url).first():
        short_url = generate_short_url()
    
    new_mapping = URLMapping(short_url=short_url, long_url=long_url)
    db.session.add(new_mapping)
    db.session.commit()
    
    return render_template('index.html', short_url=request.host_url + short_url)

@app.route('/<short_url>')
def redirect_url(short_url):
    mapping = URLMapping.query.filter_by(short_url=short_url).first()
    if mapping:
        return redirect(mapping.long_url)
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
