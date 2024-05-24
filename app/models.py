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
    

class Task:
    def __init__(self, task_id, name, complexity, size, task_type, notes):
        self.task_id = task_id
        self.name = name
        self.complexity = complexity
        self.size = size
        self.task_type = task_type
        self.notes = notes

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
        return Task(str(result.inserted_id), name, complexity, size, task_type, notes)

    @staticmethod
    def find_all():
        tasks = mongo.db.tasks.find()
        return [Task(str(task['_id']), task['name'], task['complexity'], task['size'], task['task_type'], task['notes']) for task in tasks]

    @staticmethod
    def find_by_id(task_id):
        task_data = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if task_data:
            return Task(str(task_data['_id']), task_data['name'], task_data['complexity'], task_data['size'], task_data['task_type'], task_data['notes'])
        return None

    @staticmethod
    def update_task(task_id, name, complexity, size, task_type, notes):
        mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {
                "name": name,
                "complexity": complexity,
                "size": size,
                "task_type": task_type,
                "notes": notes
            }}
        )

    @staticmethod
    def delete_task(task_id):
        mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})






     
