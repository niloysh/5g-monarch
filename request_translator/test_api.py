import requests
import argparse
import json
import os
from dotenv import load_dotenv

load_dotenv()
MONARCH_REQUEST_TRANSLATOR_URI = os.getenv("MONARCH_REQUEST_TRANSLATOR_URI", "http://127.0.0.1:5000")


def test_submit(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, "r") as file:
        json_data = json.load(file)

    submit_url = f"{MONARCH_REQUEST_TRANSLATOR_URI}/api/monitoring-requests"

    # Send the POST request to the endpoint
    response = requests.post(submit_url, json=json_data)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


def list_kpis():
    list_kpis_url = f"{MONARCH_REQUEST_TRANSLATOR_URI}/api/supported-kpis"
    response = requests.get(list_kpis_url)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


def list_monitoring_requests():
    # Send the GET request to list all monitoring requests
    list_url = f"{MONARCH_REQUEST_TRANSLATOR_URI}/api/monitoring-requests"
    response = requests.get(list_url)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


def delete_monitoring_request(request_id):
    # Construct the URL for deleting a specific monitoring request
    delete_url = f"{MONARCH_REQUEST_TRANSLATOR_URI}/api/monitoring-requests/delete/{request_id}"

    # Send the DELETE request to delete the specified monitoring request
    response = requests.delete(delete_url)

    # Print the response from the server
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the monitoring endpoint of the Flask API")
    parser.add_argument(
        "action",
        choices=["submit", "list", "kpis", "delete"],
        help="Action to perform: submit, list, delete, kpis (list supported KPIs)",
    )
    parser.add_argument(
        "--json_file", default="requests/request_nf.json", help="Path to the JSON file (only for submit action)"
    )
    parser.add_argument("--request_id", help="ID of the request to delete (only for delete action)")

    args = parser.parse_args()

    if args.action == "submit":
        test_submit(f"{args.json_file}")
    elif args.action == "list":
        list_monitoring_requests()
    elif args.action == "kpis":
        list_kpis(args.url)
    elif args.action == "delete":
        if args.request_id:
            delete_monitoring_request(args.request_id)
        else:
            print("Error: --request_id is required for delete action")
