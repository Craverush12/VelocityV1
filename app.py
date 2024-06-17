from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
db = SQLAlchemy(app)

import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyC-N8pmMCpJ_pcjJ8UfaPj24rZjXBM6nk4"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

generation_config = {
    "temperature": 1.9,
    "top_p": 0.95,
    "top_k": 50,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    prompt_count = db.Column(db.Integer, default=0)
    last_prompt_time = db.Column(db.DateTime, default=datetime.utcnow)

# Ensure database is created within an application context
with app.app_context():
    db.create_all()

def generate_prompts(user_input):
    keywords = user_input.split()
    text_prompt = ""
    image_prompt = ""
    
    if keywords[0] == "summarize":
        text_prompt = f"Summarize the following article in 3 sentences: {' '.join(keywords[1:])}"
    elif keywords[0] == "translate":
        text_prompt = f"Translate the following sentence to Hindi: {' '.join(keywords[1:])}"
    else:
        text_prompt = f"Create a text-based prompt for the following input in such a manner that when i feed it into any text based LLMs t should help me enhance my output from that tool,it has to be descriptive,with a sense of creativity and a set of suggested example prompts too: {' '.join(keywords)}"
        image_prompt = f"Create an image-based prompt for the following input in such a manner that when i feed it into any text based LLMs t should help me enhance my output from that tool,it has to be descriptive,with a sense of creativity and a set of suggested example prompts too: {' '.join(keywords)}"
    
    return text_prompt, image_prompt

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "User already exists!"
    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if 'user_id' not in session:
        return redirect(url_for('signup'))

    user = User.query.get(session['user_id'])
    if request.method == "POST":
        if user.prompt_count >= 15:
            if datetime.utcnow() - user.last_prompt_time < timedelta(minutes=7):
                return "Wait for 7 minutes or buy premium"
            else:
                user.prompt_count = 0

        user_input = request.form["prompt"]
        text_prompt, image_prompt = generate_prompts(user_input)

        chat_session = model.start_chat(history=[])
        text_response = chat_session.send_message(text_prompt)
        image_response = chat_session.send_message(image_prompt) if image_prompt else None

        text_generated = text_response.text if text_response else ""
        image_generated = image_response.text if image_response else ""

        user.prompt_count += 1
        user.last_prompt_time = datetime.utcnow()
        db.session.commit()

        return render_template("index.html", text_prompt=text_prompt, text_generated=text_generated, image_prompt=image_prompt, image_generated=image_generated)
    return render_template("index.html")

@app.context_processor
def inject_tailwind():
    return {'tailwind_css': '/static/css/main.css'}

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
