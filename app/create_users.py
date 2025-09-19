#!/usr/bin/env python
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create admin superuser"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@eito.com', 'admin123')
        print("Superuser 'admin' created with password: admin123")
    else:
        print("Superuser 'admin' already exists")

def create_normal_user():
    """Create normal user"""
    if not User.objects.filter(username='user').exists():
        User.objects.create_user('user', 'user@eito.com', 'usesr123')
        print("User 'user' created with password: user123")
    else:
        print("User 'user' already exists")

if __name__ == '__main__':
    create_superuser()
    create_normal_user()