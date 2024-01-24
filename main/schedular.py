
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .process  import run_process
from django.shortcuts import render,redirect 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def start():
    User = get_user_model()
    current_user = User.objects.first()  
    if current_user:
        username = current_user.username
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_process, 'interval', minutes=5 , args= [username])
        scheduler.start()

if __name__ == "__main__":
    start()