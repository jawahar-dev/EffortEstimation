from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token
from .models import User, Task
from . import login_manager, bcrypt, mongo
from bson.objectid import ObjectId
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('routes', __name__) 


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)

#validations for username and password
def validate_username(username):
    return len(username) >= 3

def validate_password(password):
    return len(password) >= 4

# Routes to access effort-estimation tool
@bp.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not validate_username(username):
            flash("Username must be at least 3 characters long", "danger")
        elif not validate_password(password):
            flash("Password must be at least 4 characters long", "danger")
        else:
            existing_user = User.find_by_username(username)
            if existing_user:
                flash("User already exists", "danger")
            else:
                User.create_user(username, password)
                return redirect(url_for('routes.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not validate_username(username):
            flash("Invalid username or password", "danger")
        elif not validate_password(password):
            flash("Invalid username or password", "danger")
        else:
            user = User.find_by_username(username)
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity={'username': user.username})
                login_user(user)
                return redirect(url_for('routes.tasks'))
            else:
                flash("Invalid credentials", "danger")
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@bp.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        name = request.form['name']
        complexity = request.form['complexity']
        size = request.form['size']
        task_type = request.form['task_type']
        notes = request.form['notes']

        # Create and save the new task
        new_task = Task.create_task(name, complexity, size, task_type, notes)

        return redirect(url_for('routes.task_details', task_id=new_task['_id']))

    tasks = Task.find_all()
    return render_template('tasks.html', tasks=tasks)

@bp.route('/task/<task_id>', methods=['GET'])
@login_required
def task_details(task_id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        flash("Task not found", "danger")
        return redirect(url_for('routes.tasks'))

    # Calculate estimation based on historical data
    average_hours, confidence_level, estimated_range = Task.calculate_estimation(task['name'])
    return render_template('estimated-efforts.html', task=task, average_hours=average_hours, confidence_level=confidence_level, estimated_range=estimated_range)




