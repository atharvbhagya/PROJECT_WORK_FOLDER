from flask import Blueprint, render_template

from project.auth import is_logged_in
# from . import db

main= Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')


@main.route('/profile/<string:username>')
@is_logged_in
def profile(username):

    return render_template('profile.html', username=username)