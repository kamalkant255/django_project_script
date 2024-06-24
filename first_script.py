import os
import subprocess

# Project and app names
project_name = 'grassroot'
app_name = 'v1'
api_folder = 'api'

# MySQL database configuration
database_config = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cpcl_new_test',           # Replace with your database name
    'USER': 'root',           # Replace with your database username
    'PASSWORD': 'triazine@123',       # Replace with your database password
    'HOST': 'localhost',            # Replace with your database host
    'PORT': '3306',                 # Replace with your database port
}
# Allowed hosts
allowed_hosts = ['localhost', '127.0.0.1', '[::1]']

# Swagger settings
swagger_settings = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }
    }
}

# Step 1: Create Django project
subprocess.run(['django-admin', 'startproject', project_name])

# Navigate into the project directory
os.chdir(project_name)

# Step 2: Create API folder and Django app inside it
os.makedirs(os.path.join(api_folder, app_name), exist_ok=True)
subprocess.run(['python3', 'manage.py', 'startapp', app_name, os.path.join(api_folder, app_name)])

# Step 3: Install required packages
subprocess.run(['pip', 'install', 'mysqlclient', 'djangorestframework', 'drf-yasg', 'djangorestframework-simplejwt'])

# Step 4: Configure settings.py
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
    settings_file.write("\n# Custom settings for MySQL and Swagger\n")

    # MySQL database configuration
    settings_file.write("\nDATABASES = {\n")
    settings_file.write("    'default': {\n")
    settings_file.write("        'ENGINE': '{}',\n".format(database_config['ENGINE']))
    settings_file.write("        'NAME': '{}',\n".format(database_config['NAME']))
    settings_file.write("        'USER': '{}',\n".format(database_config['USER']))
    settings_file.write("        'PASSWORD': '{}',\n".format(database_config['PASSWORD']))
    settings_file.write("        'HOST': '{}',\n".format(database_config['HOST']))
    settings_file.write("        'PORT': '{}',\n".format(database_config['PORT']))
    settings_file.write("    }\n")
    settings_file.write("}\n")

    # Allowed hosts
    settings_file.write("\nALLOWED_HOSTS = {}\n".format(allowed_hosts))

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

# Step 5: Update INSTALLED_APPS in settings.py
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

# Step 6: Create app's urls.py and integrate it with the project urls.py
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

# Step 7: Implement a simple view in the app
views_path = os.path.join(api_folder, app_name, 'views.py')
with open(views_path, 'w') as views_file:
    views_file.write("from rest_framework import viewsets\n")
    views_file.write("from rest_framework.response import Response\n")
    views_file.write("\n")
    views_file.write("class HelloWorldViewSet(viewsets.ViewSet):\n")
    views_file.write("    def list(self, request):\n")
    views_file.write("        return Response({'message': 'Hello, world!'})\n")

# Step 8: Update app configuration
apps_path = os.path.join(api_folder, app_name, 'apps.py')
with open(apps_path, 'w') as apps_file:
    apps_file.write("from django.apps import AppConfig\n")
    apps_file.write("\n")
    apps_file.write("class {}Config(AppConfig):\n".format(app_name.capitalize()))
    apps_file.write("    default_auto_field = 'django.db.models.BigAutoField'\n")
    apps_file.write("    name = '{}.{}'\n".format(api_folder, app_name))

print("Django project and app created successfully with MySQL database and Swagger configured.")
