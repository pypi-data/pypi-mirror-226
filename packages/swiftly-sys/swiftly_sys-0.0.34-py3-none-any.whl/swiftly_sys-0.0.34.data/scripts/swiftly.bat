@echo off
setlocal

REM Source swiftly-utils.sh
call swiftly-utils.bat

:activate
    REM Check if the script is sourced
    if not defined IS_SOURCED (
        echo run this command as 'source swiftly activate'
        exit /b 1
    )

    REM Check if the project is already activated
    if "%SWIFTLY_ACTIVATED%"=="true" (
        echo Swiftly project already activated.
        exit /b 0
    )

    REM Run check_swiftly from swiftly.core.main.py
    for /f %%i in ('python -c "from swiftly.core.main import check_swiftly; check_swiftly()"') do set result=%%i

    REM Handle the result
    if "%result%"=="init" (
        call :init
        exit /b 0
    ) else if "%result%"=="exit" (
        exit /b 0
    ) else if "%result%"=="continue" (
        REM Continue with the rest of the script
    ) else (
        echo Unexpected result from check_swiftly: %result%
        exit /b 1
    )

    REM update swiftly
    python -c "from swiftly.core.main import update_swiftly; update_swiftly()"

    REM get swiftly project name
    for /f %%i in ('python -c "from swiftly.utils.get import get_name; print(get_name())"') do set project_name=%%i
    set SWIFTLY_PROJECT_NAME=%project_name%
    set SWIFTLY_PROJECT_LOCATION=%cd%

    REM Modify the shell prompt
    REM Note: Batch doesn't support dynamic prompts like Bash does, so this step is omitted.

    REM git pull
    python -c "from swiftly.utils.git import git_pull; git_pull()"

    REM get swiftly project runtime
    for /f %%i in ('python -c "from swiftly.utils.get import get_runtime; print(get_runtime())"') do set runtime=%%i

    REM Source the appropriate script and run the activate function
    call "swiftly-%runtime%.bat"
    call "activate_%runtime%"

    set SWIFTLY_ACTIVATED=true
goto :eof

:deactivate
    REM Check if the script is sourced
    if not defined IS_SOURCED (
        echo run this command as 'source swiftly deactivate'
        exit /b 1
    )

    REM Check if the project is not activated
    if "%SWIFTLY_ACTIVATED%" NEQ "true" (
        echo Swiftly project is not activated.
        exit /b 0
    )

    REM Get the runtime
    for /f %%i in ('python -c "from swiftly.utils.get import get_runtime; print(get_runtime())"') do set runtime=%%i

    REM Source the appropriate script and run the deactivate function
    call "swiftly-%runtime%.bat"
    call "deactivate_%runtime%"

    REM Unset the SWIFTLY_ACTIVATED variable
    set SWIFTLY_ACTIVATED=
    REM Unset SWIFTLY specific variables
    set SWIFTLY_PROJECT_NAME=
    set SWIFTLY_PROJECT_LOCATION=
goto :eof

:init
    echo Running init function
    REM Add your complex init command here
goto :eof

:makeapp
    echo Running makeapp function
goto :eof

:run
    echo Running run function
    REM Add your complex run command here
goto :eof

:install
    echo Running install function
    REM Add your complex install command here
goto :eof

:uninstall
    echo Running uninstall function
    REM Add your complex uninstall command here
goto :eof

:add_framework
    echo Running add-framework function
    REM Add your complex add-framework command here
goto :eof

:custom
    echo Running custom function with arguments: %*
    REM Add your custom command handling logic here
goto :eof

REM Check if a function exists and call it, otherwise call the custom function
call :%1
if errorlevel 1 (
    REM Check if there's more than one argument
    if not "%~2"=="" (
        call :custom %*
    )
)
