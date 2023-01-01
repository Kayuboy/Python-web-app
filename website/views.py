from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Message
import json
from website import db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    usernames = User.query.all()
    
    return render_template("home.html", user=current_user, usernames=usernames)

@views.route('/chat')
@login_required
def chat():
    user_messages = Message.query.all()
    return render_template("chat.html", user=current_user, user_messages=user_messages)

# Add a new message to the chat
@views.route('/send', methods=['POST'])
@login_required
def send_message():
    text = request.form['text']
    user_id = request.form['user_id']
    user_message = Message(text=text, user_id=user_id)
    db.session.add(user_message)
    db.session.commit()
    return redirect('/chat')


    





