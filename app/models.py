from flask import current_app
from . import mongo, bcrypt
from bson.objectid import ObjectId
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id  
        self.username = username
        self.password = password

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(str(user_data['_id']), user_data['username'], user_data['password'])
        return None

    @staticmethod
    def find_by_id(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data['_id']), user_data['username'], user_data['password'])
        return None

    @staticmethod
    def create_user(username, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = {
            "username": username,
            "password": hashed_password
        }
        result = mongo.db.users.insert_one(new_user)
        return User(str(result.inserted_id), username, hashed_password)

    def get_id(self):
        return self.id
    

# models.py

from . import mongo
from bson.objectid import ObjectId

class Task:
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
        return mongo.db.tasks.find({"name": name})

    @staticmethod
    def create_task(name, complexity, size, task_type, notes):
        new_task = {
            "name": name,
            "complexity": complexity,
            "size": size,
            "task_type": task_type,
            "notes": notes
        }
        result = mongo.db.tasks.insert_one(new_task)
        return new_task

    @staticmethod
    def calculate_estimation(name):
        complexity_mapping = {"high": 8, "medium": 6, "low": 4}
        size_mapping = {"small": 4, "medium": 6, "large": 8}

        total_tasks = mongo.db.tasks.count_documents({"name": name})
        tasks = Task.find_by_name(name)
        total_hours = 0

        for task in tasks:
            complexity_value = complexity_mapping.get(task['complexity'], 0)
            size_value = size_mapping.get(task['size'], 0)
            total_hours += complexity_value * size_value

        if total_tasks > 0:
            average_hours = int(total_hours / total_tasks)
        else:
            average_hours = 0

        confidence_level = "high" if total_tasks > 10 else "medium" if total_tasks > 5 else "low"
        estimated_range = str(average_hours) + "-" + str(average_hours+5)

        return average_hours, confidence_level, estimated_range






     
