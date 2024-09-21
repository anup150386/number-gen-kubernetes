@echo off
REM This script sets up a Django project with Django REST Framework and creates an app.

REM Check if project name and app name are provided as arguments
IF "%1"=="" (
    echo Usage: create_django_rest_app.bat project_name app_name
    exit /b 1
)

IF "%2"=="" (
    echo Usage: create_django_rest_app.bat project_name app_name
    exit /b 1
)

SET project_name=%1
SET app_name=%2

REM Create a virtual environment (optional, recommended)
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install Django and Django REST Framework
echo Installing Django and Django REST Framework...
pip install django djangorestframework

REM Start a new Django project
echo Creating Django project: %project_name%...
django-admin startproject %project_name%

REM Navigate into the project folder
cd %project_name%

REM Create a new Django app
echo Creating Django app: %app_name%...
python manage.py startapp %app_name%

REM Update settings.py to include the new app and Django REST Framework
echo Configuring settings...
CALL :add_settings

REM Create initial migrations
echo Running migrations...
python manage.py migrate

REM Script complete
echo Django REST project and app setup is complete.

REM Activate the virtual environment for future use
echo To activate the virtual environment, run: venv\Scripts\activate

GOTO :EOF

:add_settings
REM Append the app and REST framework to INSTALLED_APPS in settings.py
SET settings_file=%project_name%\settings.py

REM Add the app and rest_framework to INSTALLED_APPS
(
    echo.
    echo # Adding REST Framework and the new app
    echo INSTALLED_APPS += [
    echo     'rest_framework',
    echo     '%app_name%',
    echo ]
)>> %settings_file%

GOTO :EOF
