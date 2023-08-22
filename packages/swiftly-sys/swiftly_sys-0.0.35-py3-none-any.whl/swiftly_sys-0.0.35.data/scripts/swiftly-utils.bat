@echo off
setlocal

:read_cli_result
    REM Get the system's temporary directory using Python
    for /f %%i in ('python -c "import tempfile; print(tempfile.gettempdir())"') do set temp_dir=%%i

    set result_file_path="%temp_dir%\swiftly_cli_result.txt"
    
    REM Check if the result file exists
    if not exist %result_file_path% (
        echo Error: Result file not found!
        exit /b 1
    )
    
    REM Read the result
    for /f "delims=" %%a in (%result_file_path%) do set result=%%a
    
    REM Remove the temporary file
    del %result_file_path%
    
    REM Return the result
    echo %result%
goto :eof

:is_sourced
    REM Batch scripts don't have an interactive mode like Bash, so this function is not directly translatable.
    REM However, you can use a workaround by setting an environment variable before sourcing the script.
    if defined IS_SOURCED (
        echo true
    ) else (
        echo false
    )
goto :eof
