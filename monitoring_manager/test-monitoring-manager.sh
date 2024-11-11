#!/bin/bash

print_subheader() {
    echo -e "\e[1;36m--- $1 ---\e[0m"
}

print_header() {
    echo -e "\n\e[1;34m############################### $1 ###############################\e[0m"
}

print_success() {
    echo -e "\e[1;32m$1\e[0m"
}

print_error() {
    echo -e "\e[1;31mERROR: $1\e[0m"
}

print_info() {
    echo -e "\e[1;33mINFO: $1\e[0m"
}



print_header "Testing Monitoring Manager (Monarch Core [4/5])"

print_subheader "Performing health check for Monitoring Manager"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:30600/api/health)

if [ "$response" -eq 200 ]; then
    print_success "Health check passed! Monitoring Manager is healthy."
else
    print_error "Health check failed with status code: $response. Please check the Monitoring Manager logs for details."
fi

# Get the list of monitoring directives
print_subheader "Fetching the list of monitoring directives"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:30600/api/monitoring-directives)

# Check if the list of directives was successfully retrieved
if [ "$response" -eq 200 ]; then
    print_success "Successfully retrieved the list of monitoring directives."
    
    # Fetch the actual directives list content
    directives=$(curl -s http://localhost:30600/api/monitoring-directives)
    
    # Check if the list is empty
    if [ -z "$directives" ] || [ "$directives" == "[]" ]; then
        print_info "The list of monitoring directives is empty. No directives found."
    else
        echo "List of monitoring directives retrieved successfully."
        echo "$directives"
    fi
else
    print_error "Failed to fetch the list of monitoring directives. Status code: $response."
fi