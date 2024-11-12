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

# Function to send GET request and handle response
get_stores_data() {
    local url=$1
    response=$(curl -s -X GET "$url")

    # Check if the curl request was successful
    if [ $? -ne 0 ]; then
        print_error "Failed to fetch data from $url"
        exit 1
    fi

    echo "$response"
}
print_header "Testing Data Distribution (Monarch Core [2/5])"
print_subheader "Performing health check for Data Distribution"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:31004/-/healthy)

if [ "$response" -eq 200 ]; then
    print_success "Health check passed! Data Distribution is healthy."
else
    print_error "Health check failed with status code: $response. Please check the Data Distribution logs for details."
fi


print_subheader "Fetching stores data from API"
response=$(get_stores_data "http://localhost:31004/api/v1/stores")

# Check if the response is empty
if [ -z "$response" ]; then
    print_error "Received empty response from the API. Exiting..."
    exit 1
fi

# Check if "sidecar" exists and print its info if found
sidecar_exists=$(echo "$response" | jq -r '.data.sidecar[]')

if [ -z "$sidecar_exists" ]; then
    print_info "Sidecar(s) should be discovered after deploying NSSDC."
else
    print_success "NSSDC Sidecar(s) found:"
    echo "$sidecar_exists" | jq -r '"Endpoint: \(.name), Status: \(.lastError // "null" | if . == "null" then "UP" else "DOWN" end), Cluster: \(.labelSets[0].cluster // "N/A")"'
fi
