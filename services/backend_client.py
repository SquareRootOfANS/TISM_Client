# services/backend_client.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def submit_recon_report(report_data):
    response = requests.post(f"{BASE_URL}/recon_reports", json=report_data)
    response.raise_for_status()
    return response.json()

def get_all_recon_reports():
    response = requests.get(f"{BASE_URL}/recon_reports")
    response.raise_for_status()
    return response.json()

def delete_recon_report(report_id):
    response = requests.delete(f"{BASE_URL}/recon_reports/{report_id}")
    response.raise_for_status()
    return response.status_code == 200
