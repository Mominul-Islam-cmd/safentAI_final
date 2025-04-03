from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safenet_ai.settings')
django.setup()

# Create superuser
username = 'admin'
email = 'admin@safenet.ai'
password = 'Admin@123'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
    else:
        print(f"Superuser '{username}' already exists.")
except Exception as e:
    print(f"Error creating superuser: {e}")