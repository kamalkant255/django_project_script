import os
import subprocess

# Project and app names
project_name = 'grassroot_index'
app_name = 'v1'
api_folder = 'api'

# Environment variables for MySQL database configuration
env_vars = {
    'DB_ENGINE': 'django.db.backends.mysql',
    'DB_NAME': 'cpcl_new_test',        # Replace with your database name
    'DB_USER': 'root',        # Replace with your database username
    'DB_PASSWORD': 'triazine@123',    # Replace with your database password
    'DB_HOST': 'localhost',         # Replace with your database host
    'DB_PORT': '3306',              # Replace with your database port
    'ALLOWED_HOSTS': 'localhost,127.0.0.1,[::1]',
}

# Step 1: Create Django project
subprocess.run(['django-admin', 'startproject', project_name])

# Navigate into the project directory
os.chdir(project_name)

# Step 2: Create API folder and Django app inside it
os.makedirs(os.path.join(api_folder, app_name), exist_ok=True)
subprocess.run(['python3', 'manage.py', 'startapp', app_name, os.path.join(api_folder, app_name)])

# Step 3: Install required packages
subprocess.run(['pip', 'install', 'mysqlclient', 'djangorestframework', 'drf-yasg', 'djangorestframework-simplejwt', 'python-dotenv'])

# Step 4: Create requirements.txt
requirements = [
    'Django>=3.2,<4.0',
    'mysqlclient',
    'djangorestframework',
    'drf-yasg',
    'djangorestframework-simplejwt',
    'python-dotenv'
]

with open('requirements.txt', 'w') as req_file:
    req_file.write('\n'.join(requirements))

# Step 5: Create .env file
with open('.env', 'w') as env_file:
    for key, value in env_vars.items():
        env_file.write(f"{key}={value}\n")

# Step 6: Create db.py for database configuration
db_path = os.path.join(project_name, 'db.py')
with open(db_path, 'w') as db_file:
    db_file.write("import os\n")
    db_file.write("from dotenv import load_dotenv\n")
    db_file.write("\n")
    db_file.write("load_dotenv()\n")
    db_file.write("\n")
    db_file.write("DATABASES = {\n")
    db_file.write("    'default': {\n")
    db_file.write("        'ENGINE': os.getenv('DB_ENGINE'),\n")
    db_file.write("        'NAME': os.getenv('DB_NAME'),\n")
    db_file.write("        'USER': os.getenv('DB_USER'),\n")
    db_file.write("        'PASSWORD': os.getenv('DB_PASSWORD'),\n")
    db_file.write("        'HOST': os.getenv('DB_HOST'),\n")
    db_file.write("        'PORT': os.getenv('DB_PORT'),\n")
    db_file.write("    }\n")
    db_file.write("}\n")

# Step 7: Configure settings.py
settings_path = os.path.join(project_name, 'settings.py')

with open(settings_path, 'r') as settings_file:
    settings_content = settings_file.read()

# Remove SQLite database configuration
settings_content = settings_content.replace(
    "DATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.sqlite3',\n        'NAME': BASE_DIR / 'db.sqlite3',\n    }\n}\n",
    ""
)

# Write back to settings.py
with open(settings_path, 'w') as settings_file:
    settings_file.write(settings_content)

# Append custom settings
with open(settings_path, 'a') as settings_file:
    settings_file.write("\n# Load environment variables\n")
    settings_file.write("import os\n")
    
    settings_file.write("from dotenv import load_dotenv\n")
    settings_file.write("load_dotenv()\n")
    settings_file.write("\n")
    settings_file.write("# Database configuration\n")
    settings_file.write("from .db import DATABASES\n")

    # Allowed hosts
    settings_file.write("\nALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')\n")

    # Swagger settings
    settings_file.write("\nSWAGGER_SETTINGS = {\n")
    settings_file.write("    'SECURITY_DEFINITIONS': {\n")
    settings_file.write("        'api_key': {\n")
    settings_file.write("            'type': 'apiKey',\n")
    settings_file.write("            'in': 'header',\n")
    settings_file.write("            'name': 'Authorization',\n")
    settings_file.write("        }\n")
    settings_file.write("    }\n")
    settings_file.write("}\n")

    # REST framework settings
    settings_file.write("\nREST_FRAMEWORK = {\n")
    settings_file.write("    'DEFAULT_AUTHENTICATION_CLASSES': [\n")
    settings_file.write("        'rest_framework_simplejwt.authentication.JWTAuthentication',\n")
    settings_file.write("    ],\n")
    settings_file.write("}\n")

# Step 8: Update INSTALLED_APPS in settings.py
with open(settings_path, 'r') as settings_file:
    settings_content = settings_file.read()

index = settings_content.find('INSTALLED_APPS = [')
end_index = settings_content.find(']', index) + 1

installed_apps_content = settings_content[index:end_index]
new_installed_apps = [
    "'rest_framework',",
    "'drf_yasg',",
    "'rest_framework_simplejwt',",
    "'{}.{}',".format(api_folder, app_name),
]
new_installed_apps_content = installed_apps_content[:-1] + '\n    ' + '\n    '.join(new_installed_apps) + '\n]'

updated_settings_content = settings_content[:index] + new_installed_apps_content + settings_content[end_index:]

with open(settings_path, 'w') as settings_file:
    settings_file.write(updated_settings_content)

# Step 9: Create app's urls.py and integrate it with the project urls.py
app_urls_path = os.path.join(api_folder, app_name, 'urls.py')
with open(app_urls_path, 'w') as app_urls_file:
    app_urls_file.write("from django.urls import path, include\n")
    app_urls_file.write("from rest_framework.routers import DefaultRouter\n")
    app_urls_file.write("from .views import HelloWorldViewSet\n")
    app_urls_file.write("\n")
    app_urls_file.write("router = DefaultRouter()\n")
    app_urls_file.write("router.register(r'hello', HelloWorldViewSet, basename='hello')\n")
    app_urls_file.write("\n")
    app_urls_file.write("urlpatterns = [\n")
    app_urls_file.write("    path('', include(router.urls)),\n")
    app_urls_file.write("]\n")

project_urls_path = os.path.join(project_name, 'urls.py')
with open(project_urls_path, 'a') as project_urls_file:
    project_urls_file.write("\nfrom django.urls import include, path\n")
    project_urls_file.write("from rest_framework import permissions\n")
    project_urls_file.write("from drf_yasg.views import get_schema_view\n")
    project_urls_file.write("from drf_yasg import openapi\n")
    project_urls_file.write("\n")
    project_urls_file.write("schema_view = get_schema_view(\n")
    project_urls_file.write("   openapi.Info(\n")
    project_urls_file.write("      title='API',\n")
    project_urls_file.write("      default_version='v1',\n")
    project_urls_file.write("      description='Test description',\n")
    project_urls_file.write("   ),\n")
    project_urls_file.write("   public=True,\n")
    project_urls_file.write("   permission_classes=(permissions.AllowAny,),\n")
    project_urls_file.write(")\n")
    project_urls_file.write("\n")
    project_urls_file.write("urlpatterns += [\n")
    project_urls_file.write("    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),\n")
    project_urls_file.write("    path('api/', include('api.{}.urls')),\n".format(app_name))
    project_urls_file.write("]\n")

# Step 10: Implement a simple view in the app
views_path = os.path.join(api_folder, app_name, 'views.py')
with open(views_path, 'w') as views_file:
    views_file.write("from rest_framework import viewsets\n")
    views_file.write("from rest_framework.response import Response\n")
    views_file.write("\n")
    views_file.write("class HelloWorldViewSet(viewsets.ViewSet):\n")
    views_file.write("    def list(self, request):\n")
    views_file.write("        return Response({'message': 'Hello, world!'})\n")
    
# Step 11: Update app configuration
apps_path = os.path.join(api_folder, app_name, 'apps.py')
with open(apps_path, 'w') as apps_file:
    apps_file.write("from django.apps import AppConfig\n")
    apps_file.write("\n")
    apps_file.write("class {}Config(AppConfig):\n".format(app_name.capitalize()))
    apps_file.write("    default_auto_field = 'django.db.models.BigAutoField'\n")
    apps_file.write("    name = '{}.{}'\n".format(api_folder, app_name))
