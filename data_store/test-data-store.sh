#!/bin/bash
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

print_subheader() {
    echo -e "\e[1;36m--- $1 ---\e[0m"
}

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Set environment variables from .env file
print_header "Testing Data Store (Monarch Core [1/5])"
set -o allexport
source "$SCRIPT_DIR/../.env"
set +o allexport

# Check if the necessary environment variables are set
if [ -z "$MONARCH_MINIO_ENDPOINT" ] || [ -z "$MONARCH_MINIO_ACCESS_KEY" ] || [ -z "$MONARCH_MINIO_SECRET_KEY" ]; then
    print_error "One or more required environment variables are missing (MONARCH_MINIO_ENDPOINT, MONARCH_MINIO_ACCESS_KEY, MONARCH_MINIO_SECRET_KEY). Please check the .env file."
    exit 1
fi

# Add MinIO binary directory to the PATH
export PATH=$PATH:$HOME/minio-binaries/

# Set the MinIO alias and perform a health check
mc alias set myminio http://$MONARCH_MINIO_ENDPOINT $MONARCH_MINIO_ACCESS_KEY $MONARCH_MINIO_SECRET_KEY

# Check MinIO admin info
print_subheader "Fetching MinIO admin info"
admin_info=$(mc admin info myminio)

if [ -n "$admin_info" ]; then
    print_success "Successfully retrieved MinIO admin info."
    print_info "$admin_info"
else
    print_error "Failed to fetch MinIO admin info."
    exit 1
fi

# List contents of the monarch-thanos bucket
print_subheader "Listing contents of 'monarch-thanos' bucket"
bucket_contents=$(mc ls myminio/monarch-thanos)

if [ -n "$bucket_contents" ]; then
    print_success "Successfully listed contents of 'monarch-thanos' bucket."
    print_info "$bucket_contents"
else
    print_info "Failed to list contents of 'monarch-thanos' bucket. It may be empty. S3 objects are uploaded every 2 hours."
    exit 1
fi