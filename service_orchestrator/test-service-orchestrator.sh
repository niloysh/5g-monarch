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

# Set base URL for the API
BASE_URL="http://localhost:5001"

# Perform health check
print_header "Testing Service Orchestrator (External Component [1/2])"
response=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/api/health)

if [ "$response" -eq 200 ]; then
    print_success "Health check passed! Service Orchestrator is healthy."
else
    print_error "Health check failed with status code: $response. Please check the service logs for details."
    exit 1
fi

# Fetch slice information for slice 1-000001 and capture the response
print_subheader "Fetching slice information for slice 1-000001"
slice_info=$(curl -s $BASE_URL/slices/1-000001)

# Check if the response contains valid data
if [ -n "$slice_info" ]; then
    print_success "Successfully retrieved slice information for slice 1-000001."
    print_info "Slice Information: $slice_info"
else
    print_error "Failed to fetch slice information for slice 1-000001."
    exit 1
fi