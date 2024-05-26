from flask import current_app
from . import mongo, bcrypt
from bson.objectid import ObjectId
from flask_login import UserMixin

#user model to store user data in mongoDB
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id  
        self.username = username
        self.password = password

    @staticmethod
    def find_by_username(username):
        name = {"username": username}
        user = mongo.db.users.find_one(name)
        if user:
            return User(str(user['_id']), user['username'], user['password'])
        return None

    @staticmethod
    def find_by_id(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(str(user['_id']), user['username'], user['password'])
        return None

    #creating the user with username and password
    @staticmethod
    def create_user(username, password):
        #hashing the password before storing into DB
        secured_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = {
            "username": username,
            "password": secured_password
        }
        out = mongo.db.users.insert_one(new_user)
        return User(str(out.inserted_id), username, secured_password)

    def get_id(self):
        return self.id
    
#Task model to store task for future as historical data
class Tasks:
    def __init__(self, name, complexity, size, task_type, notes):
        self.name = name
        self.complexity = complexity
        self.size = size
        self.task_type = task_type
        self.notes = notes

    @staticmethod
    def find_all():
        return mongo.db.tasks.find()

    @staticmethod
    def find_by_name(name):
        user_name = {"name": name}
        return mongo.db.tasks.find(user_name)

    #creating the task, based on user entered task data
    @staticmethod
    def create_task(name, complexity, size, task_type, notes):
        task = {
            "name": name,
            "complexity": complexity,
            "size": size,
            "task_type": task_type,
            "notes": notes
        }
        out = mongo.db.tasks.insert_one(task)
        return out


    #estimate calculation method, to calculate estimation using historical data
    @staticmethod
    def estimate_calculation(name):
        #mapping the values by assuming their level
        complexity_values = {"high": 8, "medium": 6, "low": 4}
        size_values= {"small": 4, "medium": 6, "large": 8}
        
        #counting the number of tasks in DB
        total_tasks = mongo.db.tasks.count_documents({"name": name})
        print(total_tasks)
        #retriving the tasks using name
        tasks = Tasks.find_by_name(name)
        total_hours = 0

        for task in tasks:
            complexity_out = complexity_values.get(task['complexity'], 0)
            size_out = size_values.get(task['size'], 0)
            total_hours += complexity_out * size_out
        # print("total-hours", total_hours)
        if total_tasks > 0:
            avg_hours = int(total_hours / total_tasks)
        else:
            avg_hours = 0

        confidence_level = "high" if total_tasks > 10 else "medium" if total_tasks > 5 else "low"
        #estimated range calculation
        estimated_range = str(avg_hours - 5) + "-" + str(avg_hours+5)
        return avg_hours, confidence_level, estimated_range






     
