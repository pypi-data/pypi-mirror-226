import os
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR

def detect_django():
    project_location = os.environ.get(f'{SWIFTLY_PROJECT_LOCATION_VAR}')
    
    # If the project location is not set, return False
    if not project_location:
        return False
    
    # Check if 'manage.py' exists in the project location
    manage_py_path = os.path.join(project_location, 'manage.py')
    if not os.path.exists(manage_py_path):
        return False
    
    # Check contents of 'manage.py' for Django-specific code
    with open(manage_py_path, 'r') as file:
        contents = file.read()
        if "DJANGO_SETTINGS_MODULE" not in contents or "from django.core.management import execute_from_command_line" not in contents:
            return False

    return True


def run_check(arg=None):
    if arg is None:
        return True
    
    if 'manage.py' in arg:
        return True
    
    else:
        return False
