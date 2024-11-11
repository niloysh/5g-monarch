#!/bin/bash

print_header() {
    echo -e "\n\e[1;34m############################### $1 ###############################\e[0m"
}

print_subheader() {
    echo -e "\e[1;36m--- $1 ---\e[0m"
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

# Endpoint URLs
HEALTH_URL="http://localhost:30700/api/health"
KPIS_URL="http://localhost:30700/api/supported-kpis"

print_header "Testing Request Translator (Monarch Core [5/5])"
print_subheader "Performing health check for Request Translator"
print_info "Checking health status of the service..."
health_response=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL")

if [ "$health_response" -eq 200 ]; then
    print_success "Service health check passed! The service is up and running."
else
    print_error "Service health check failed with status code: $health_response."
    exit 1
fi

print_subheader "Checking supported KPIs"
print_info "Fetching supported KPIs..."
kpis_response=$(curl -s "$KPIS_URL")

if [ -z "$kpis_response" ]; then
    print_error "Failed to fetch supported KPIs or received an empty response."
    exit 1
fi

# Display the supported KPIs in a formatted way
print_success "Supported KPIs retrieved successfully:"
echo "$kpis_response"