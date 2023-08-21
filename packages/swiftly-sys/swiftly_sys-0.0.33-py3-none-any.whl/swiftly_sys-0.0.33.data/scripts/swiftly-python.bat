@echo off
@REM setlocal

@REM :activate_python
@REM     REM Get the project name from the environment variable
@REM     set project_name=%SWIFTLY_PROJECT_NAME%

@REM     REM Check if the virtual environment exists
@REM     if not exist "venv%project_name%" (
@REM         echo Error: Virtual environment 'venv%project_name%' not found.
@REM         exit /b 1
@REM     )

@REM     REM Source the virtual environment's activate script
@REM     call venv%project_name%\Scripts\activate

@REM     REM install and keep swiftly up-to-date
@REM     python -m pip install --upgrade pip >nul 2>&1
@REM     python -m pip install swiftly-sys --upgrade >nul 2>&1

@REM     REM Install the requirements using the Python function
@REM     python -c "from swiftly.runtime.python.main import install_requirements; install_requirements()"
@REM goto :eof

@REM :deactivate_python
@REM     REM Check if the virtual environment is activated
@REM     if "%VIRTUAL_ENV%"=="" (
@REM         echo Error: No virtual environment is currently activated.
@REM         exit /b 1
@REM     )

@REM     REM Call the deactivate function from the activate file
@REM     call "%VIRTUAL_ENV%\Scripts\deactivate.bat"
@REM goto :eof

@REM :run_python
@REM     echo running python
@REM goto :eof

@REM :makeapp_python
@REM     REM Placeholder for makeapp_python function
@REM goto :eof

@REM :custom
@REM     echo Running python custom function with arguments: %*
@REM     REM Add your custom command handling logic here
@REM goto :eof

@REM REM Check if a function exists and call it, otherwise call the custom function
@REM call :%1
@REM if errorlevel 1 (
@REM     REM Check if there's more than one argument
@REM     if not "%~2"=="" (
@REM         call :custom %*
@REM     )
@REM )
