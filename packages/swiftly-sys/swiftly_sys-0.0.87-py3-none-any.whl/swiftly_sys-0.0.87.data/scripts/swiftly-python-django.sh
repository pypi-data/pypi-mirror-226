add_framework_django(){
    echo "adding django"
}

run_python_django(){
    echo "running django"
}

makeapp_python_django(){
    echo "making a django app"
}

# Check if a function exists and call it, otherwise call the custom function
if declare -f "$1" > /dev/null; then
    "$@"
fi
