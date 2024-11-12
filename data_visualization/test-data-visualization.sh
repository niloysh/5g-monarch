#!/bin/bash
GRAFANA_URL="http://localhost:32005"
DASHBOARD_UID="f1471646-a245-4f23-a3e1-452baa6558c8"
USERNAME="admin"
PASSWORD="monarch-operator"


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


print_header "Testing Data Visualization (Monarch Core [3/5])"
print_subheader "Checking Monarch Dashboard with UID: $DASHBOARD_UID"
response=$(curl -s -u "$USERNAME:$PASSWORD" \
                -H "Content-Type: application/json" \
                "$GRAFANA_URL/api/search?dashboardUIDs=$DASHBOARD_UID")

# Check if the response is empty or contains dashboard information
if [ -n "$response" ] && [ "$response" != "[]" ]; then
    echo "Dashboard found for UID $DASHBOARD_UID:"
    echo "$response" | jq '.'
else
    echo "No dashboard found with UID: $DASHBOARD_UID."
fi