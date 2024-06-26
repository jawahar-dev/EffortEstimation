import os

#configuration for mongoDB and for JWT authentication
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGO_URI = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/estimationdb')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
