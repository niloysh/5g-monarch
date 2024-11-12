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


print_header "Testing NSSDC (Monarch NSS [1/1])"
print_subheader "Performing health check for NSSDC"
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:30095/-/healthy)

if [ "$response" -eq 200 ]; then
    print_success "Health check passed! NSSDC (Prometheus) is healthy."
else
    print_error "Health check failed with status code: $response. Please check the NSSDC (Prometheus) logs for details."
fi


# Fetch and display Prometheus targets
print_subheader "Fetching active targets from API"
response=$(curl -s -X GET "http://localhost:30095/api/v1/targets?state=active")

# Check if the response is empty
if [ -z "$response" ]; then
    print_error "No active targets found. Exiting..."
    exit 1
fi

# Use jq to filter out and display the scrapePool (target group)
print_info "Active scrape pools found:"
echo "$response" | jq -r '.data.activeTargets[] | .scrapePool'