from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/users/')
def display_user():
    users = [
        {
            "id": 1,
            "username": "username1",
            "email": "data1@sample.com"
        },
        {
            "id": 2,
            "username": "username2",
            "email": "data2@sample.com"
        }
    ]

    # passing data to the template
    return render_template("show_user.html", users=users)
