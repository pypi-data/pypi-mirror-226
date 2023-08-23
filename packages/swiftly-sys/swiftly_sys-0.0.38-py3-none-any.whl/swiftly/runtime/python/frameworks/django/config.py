from swiftly.runtime.python.frameworks.django.main import detect_django

FRAMEWORK_CONFIG = {
    "name": "django",
    "type": "web",
    
    # a python function that detects if runtime is the current runtime (in this case, detect if it's a python runtime)
    "detect": detect_django,
    
    # a list of custom functions. "command": "shell/bat function name"
    "custom": [],
    "framework_commands" : ['makeapp', 'run']
}