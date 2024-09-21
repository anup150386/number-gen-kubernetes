@echo off
REM This script sets up a Django project with Django REST Framework, async support, rate limiting, and creates an async app.

REM Check if project name and app name are provided as arguments
IF "%1"=="" (
    echo Usage: create_django_rest_async_app_with_throttling.bat project_name app_name
    exit /b 1
)

IF "%2"=="" (
    echo Usage: create_django_rest_async_app_with_throttling.bat project_name app_name
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

REM Install Django, Django REST Framework, and other async dependencies
echo Installing Django, Django REST Framework, async support, and throttling dependencies...
pip install django djangorestframework asgiref channels

REM Start a new Django project
echo Creating Django project: %project_name%...
django-admin startproject %project_name%

REM Navigate into the project folder
cd %project_name%

REM Create a new Django app
echo Creating Django app: %app_name%...
python manage.py startapp %app_name%

REM Update settings.py to include the new app, Django REST Framework, and Channels for async support
echo Configuring settings with throttling and rate limiting...
CALL :add_settings

REM Create initial migrations
echo Running migrations...
python manage.py migrate

REM Script complete
echo Async Django REST project with throttling setup is complete.

REM Activate the virtual environment for future use
echo To activate the virtual environment, run: venv\Scripts\activate

GOTO :EOF

:add_settings
REM Append the app, rest_framework, and channels to INSTALLED_APPS in settings.py
SET settings_file=%project_name%\settings.py

REM Add the app, rest_framework, channels, and throttling to INSTALLED_APPS
(
    echo.
    echo # Adding REST Framework, the new app, and Channels for async support
    echo INSTALLED_APPS += [
    echo     'rest_framework',
    echo     '%app_name%',
    echo     'channels',
    echo ]
    echo.
    echo # Configure REST Framework Throttling
    echo REST_FRAMEWORK = {
    echo     'DEFAULT_THROTTLE_CLASSES': [
    echo         'rest_framework.throttling.AnonRateThrottle',
    echo         'rest_framework.throttling.UserRateThrottle',
    echo     ],
    echo     'DEFAULT_THROTTLE_RATES': {
    echo         'anon': '10/day',
    echo         'user': '100/hour',
    echo     }
    echo }
)>> %settings_file%

REM Update ASGI configuration for async support
CALL :update_asgi

GOTO :EOF

:update_asgi
REM Update the project ASGI settings to use Channels for async views and websockets
SET asgi_file=%project_name%\asgi.py

(
    echo.
    echo # Adding Channels support for async views
    echo import os
    echo from channels.routing import ProtocolTypeRouter, URLRouter
    echo from django.core.asgi import get_asgi_application
    echo import %app_name%.routing
    echo.
    echo os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%project_name%.settings')
    echo.
    echo application = ProtocolTypeRouter({
    echo     'http': get_asgi_application(),
    echo     'websocket': URLRouter(%app_name%.routing.websocket_urlpatterns),
    echo })
)>> %asgi_file%

GOTO :EOF
