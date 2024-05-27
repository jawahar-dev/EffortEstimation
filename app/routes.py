import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token
from .models import User, Tasks
from . import login_manager, bcrypt, mongo
from bson.objectid import ObjectId
from flask_login import login_user, logout_user, login_required, current_user

#registering our app with flask blueprint
bp = Blueprint('routes', __name__) 

#initializing logging module to log log messages of our app
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',handlers=[logging.FileHandler("EffortEstmt.log")])  
logger = logging.getLogger(__name__)


#loading the current logged in user
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


#register route, to register with effort estmitation tool
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not validate_username(username):
            logger.error(f'Username is not valid: {username}')
            flash("Username must be at least 3 characters long", "danger")
        elif not validate_password(password):
            logger.error(f'Password is not valid: {password}')
            flash("Password must be at least 4 characters long", "danger")
        else:
            #checking if already user is existed or not
            user_exist = User.find_by_username(username)
            if user_exist:
                logger.error('User already exists')
                flash("User already exists", "danger")
            else:
                #creating user with username and password
                User.create_user(username, password)
                logger.info('User created successfully')
                return redirect(url_for('routes.login'))
    return render_template('register.html')


#login route, 
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not validate_username(username):
            logger.error(f'Username is not valid: {username}')
            flash("Invalid username or password", "danger")
        elif not validate_password(password):
            logger.error(f'Username is not valid: {password}')
            flash("Invalid username or password", "danger")
        else:
            
            #checking if user registered or not
            user = User.find_by_username(username)
            #checking hased password and user enterd password same or not
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity={'username': user.username})
                login_user(user)
                logger.info('Logged In successfully')
                
                #used for if this route called as api if yes showing accesstoken as json format
                if request.args.get('api') == 'true':
                    return jsonify({"access_token": access_token, "message": "login successful"}), 200
                else:
                    return redirect(url_for('routes.render_dashboard'))
            else:
                flash("Invalid credentials", "danger")
                logger.error('Invalid Credentials')
                if request.args.get('api') == 'true':
                    return jsonify({"message": "Invalid credentials"}), 401
    
    return render_template('login.html')


#logout route, to logout logged in user
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    logger.info('User Logged Out successfully !!')
    return redirect(url_for('routes.login'))

#route, just to show Dashboard of estimation tool
@bp.route('/dashboard')
@login_required
def render_dashboard():
    return render_template('dashboard.html')

#tasks route, to enter task for estimation submission
@bp.route('/submit-estimate')
@login_required
def submit_estimate():
    return render_template('tasks.html')

#effort submission and calculation API
@bp.route('/api/submit-estimate', methods=['POST'])
@login_required
def tasks_api():
    response = request.json
    name = response.get('name')
    complexity = response.get('complexity')
    size = response.get('size')
    task_type = response.get('task_type')
    notes = response.get('notes')

    # Create and save the new task
    new_task = Tasks.create_task(name, complexity, size, task_type, notes)
    new_task_id = new_task.inserted_id
    logger.debug(f'Task Created successfully: {name}')
    
    return jsonify({"message": "Task created successfully", "task_id": str(new_task_id)}), 201

@bp.route('/api/est-calculate/name/<name>', methods=['GET'])
@login_required
def task_estimation(name):
    task = Tasks.find_by_name(name)
    if not task:
        logger.error(f'Task Was not found: {name}')
        return jsonify({"message": "Task not found"}), 404

    # Calculate estimation based on historical data
    avg_hours, confidence_level, estimated_range = Tasks.estimate_calculation(name)
    logger.debug(f'Task Estimation Details: averahe-hours - {avg_hours} confidence-level - {confidence_level} estimated-range- {estimated_range}')
    estimation_details = {
        "name": name,
        "average_hours": avg_hours,
        "confidence_level": confidence_level,
        "estimated_range" : estimated_range
    }
    # print(estimation_details)
    return jsonify(estimation_details), 200



