import os
import sys
import subprocess
import re

import questionary
import importlib

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config, get_frameworks, get_runtime
from swiftly.utils.cli import clireturn
from swiftly.utils.do import add_to_config
from swiftly.utils.check import is_swiftly, is_online, is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR, SWIFTLY_PROJECT_NAME_VAR

"""
ACTIVATE:
"""

def check_swiftly():
    """check if it's swiftly project, and tell what to do next"""
    if not is_swiftly():
        answer = questionary.confirm("This is not a swiftly project. Do you want to convert it to a swiftly project?").ask()
        if answer:
            clireturn("init")
        else:
            clireturn("exit")
    else:
        clireturn("continue")

        
def update_swiftly(show_load=True):
    """Update and install the latest version of swiftly-sys."""
    if not is_online():
        return
    
    loader = Loader()
    
    # Determine the appropriate python command based on the platform
    python_command = "python3" if os.name == "posix" else "python"
    
    # Start the loader with a message
    if show_load:
        loader.start("Checking swiftly")
    
    try:
        # Execute pip install to update swiftly-sys and check for errors
        subprocess.run([python_command, "-m", "pip", "install", "swiftly-sys", "--upgrade", "--break-system-packages"], check=True, stdout=subprocess.PIPE)
        if show_load:
            loader.end("Checked swiftly")
        
    except subprocess.CalledProcessError:
        if show_load:
            loader.end("Failed to update swiftly", failed=True)


"""
INIT
"""


def init(name=None):
    """Initialize the project."""
    # Get or confirm project name
    if name is None:
        name = questionary.text("Enter the name of the project:").ask()
    else:
        name = questionary.text("Confirm or edit the project name:", default=name).ask()

    # Get the directory of the currently executing file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the runtime directory
    runtime_dir = os.path.join(current_dir, 'runtime')
    runtimes = os.listdir(runtime_dir)
    runtime = questionary.select(
        "Choose a runtime:",
        choices=runtimes
    ).ask()

    # Navigate to the frameworks directory for the selected runtime
    framework_dir = os.path.join(runtime_dir, runtime, 'frameworks')
    available_frameworks = os.listdir(framework_dir)
    frameworks = questionary.checkbox(
        "Select frameworks (choose one or more, or none):",
        choices=available_frameworks
    ).ask()

    print(name, runtime, frameworks)

"""
MAKEAPP
"""

def makeapp(name=None):
    """Create a new app."""
    # Get runtime and frameworks
    runtime_name = get_runtime()
    frameworks = get_frameworks()

    execute = [runtime_name]

    # For each framework, get the FRAMEWORK_CONFIG
    for framework in frameworks:
        module_name = f"swiftly.runtime.{runtime_name}.frameworks.{framework}.config"
        config_module = importlib.import_module(module_name)
        FRAMEWORK_CONFIG = getattr(config_module, "FRAMEWORK_CONFIG", None)

        if FRAMEWORK_CONFIG and "makeapp" in FRAMEWORK_CONFIG.get("framework_commands", []):
            execute.append(framework)
            
    # Ask for app name if not provided or confirm if provided
    if name:
        name = questionary.text("Confirm or modify the app name:", default=name).ask()
    else:
        name = questionary.text("Enter the name of the app:").ask()


    executionList = []

    # Depending on the size of the execute list, prompt user accordingly
        # Depending on the size of the execute list, prompt user accordingly
    choices = ["run makeapp", "customize makeapp"]
    
    if len(execute) > 1:
        choice = questionary.select(
            "How to execute:",
            choices=choices
        ).ask()

        if choice == choices[0]:
            executionList.extend(execute)
        elif choice == choices[1]:
            # Ensure at least one option is selected
            while True:
                custom_choices = questionary.checkbox(
                    "Select what to makeapp with:",
                    choices=execute,
                    validate=lambda x: True if len(x) > 0 else "You must select at least one option!"
                ).ask()
                if custom_choices:
                    break
            executionList.extend(custom_choices)
    else:
        executionList.append(execute[0])


    # Modify executionList to include runtime name for frameworks
    executionList = [f"{runtime_name}-{item}" if item != runtime_name else item for item in executionList]

    # Print the final execution list
    clireturn(",".join(executionList))


def install():
    """Install the necessary dependencies."""
    # Logic for installing dependencies goes here
    pass

def uninstall():
    """Uninstall the project."""
    # Logic for uninstalling the project goes here
    pass

def run(arg=None):
    """Run the project."""
    # Get runtime and frameworks
    runtime_name = get_runtime()
    frameworks = get_frameworks()

    run = []

    # Check if "run" is supported by the runtime
    runtime_module_name = f"swiftly.runtime.{runtime_name}.config"
    runtime_config_module = importlib.import_module(runtime_module_name)
    RUNTIME_CONFIG = getattr(runtime_config_module, "RUNTIME_CONFIG", None)

    if RUNTIME_CONFIG:
        run_check_function = RUNTIME_CONFIG.get("run_check")
        if run_check_function and run_check_function(arg):
            run.append(runtime_name)

    # Check if "run" is in each framework's config
    for framework in frameworks:
        module_name = f"swiftly.runtime.{runtime_name}.frameworks.{framework}.config"
        config_module = importlib.import_module(module_name)
        FRAMEWORK_CONFIG = getattr(config_module, "FRAMEWORK_CONFIG", None)

        if FRAMEWORK_CONFIG and "run" in FRAMEWORK_CONFIG.get("framework_commands", []):
            run_check_function = FRAMEWORK_CONFIG.get("run_check")
            if run_check_function and run_check_function(arg):
                run.append(framework)

    # If the run list has more than one item, ask the user which runtime/framework they want to use
    if len(run) > 1:
        choice = questionary.select(
            "What do you wanna run your code with:",
            choices=run
        ).ask()
    else:
        choice = run[0] if run else None
        
    if choice == None:
        clireturn("exit")
        return

    # Format the choice to return as runtime or runtime-framework
    clireturn(choice if choice == runtime_name else f"{runtime_name}-{choice}")



def add_framework():
    """Add a new framework to the project."""
    # Logic for adding a new framework goes here
    pass

def custom():
    """Handle custom operations."""
    # Logic for custom operations goes here
    pass

def get_git_name(link):
    # Regular expression to match the repository name in a git URL
    pattern = r".*/(.+?)\.git$"
    match = re.search(pattern, link)
    return match.group(1) if match else None