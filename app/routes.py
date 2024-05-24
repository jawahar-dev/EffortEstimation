import statistics
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from .models import User, Task
from . import login_manager, bcrypt, mongo
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

# Routes
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
                flash("User registered successfully", "success")
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
                flash("Logged in successfully", "success")
                return redirect(url_for('routes.tasks'))
            else:
                flash("Invalid credentials", "danger")
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
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
        Task.create_task(name, complexity, size, task_type, notes)
        flash("Estimation Submitted successfully", "success")
        return redirect(url_for('routes.tasks'))
    tasks = Task.find_all()
    return render_template('tasks.html', tasks=tasks)




@bp.route('/tasks/<string:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.find_by_id(task_id)
    if request.method == 'POST':
        name = request.form['name']
        complexity = request.form['complexity']
        size = request.form['size']
        task_type = request.form['task_type']
        notes = request.form['notes']
        Task.update_task(task_id, name, complexity, size, task_type, notes)
        flash("Task updated successfully", "success")
        return redirect(url_for('routes.tasks'))
    return render_template('edit_task.html', task=task)

@bp.route('/tasks/<string:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    Task.delete_task(task_id)
    flash("Task deleted successfully", "success")
    return redirect(url_for('routes.tasks'))


# def calculate_estimation(estimates):
    # Dummy logic to calculate average hours and confidence level
    hours = [estimate.hours for estimate in estimates]
    if hours:
        avg_hours = statistics.mean(hours)
        confidence_level = statistics.stdev(hours) if len(hours) > 1 else 0
    else:
        avg_hours = confidence_level = 0
    return avg_hours, confidence_level


    estimates = Estimate.find_by_project_id(project_id)
    avg_hours, confidence_level = calculate_estimation(estimates)
    return render_template('estimate_result.html', avg_hours=avg_hours, confidence_level=confidence_level)