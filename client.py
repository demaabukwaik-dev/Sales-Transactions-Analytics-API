import requests
import json

class Client:
    def __init__(self, url="http://127.0.0.1:8001"):
        self.url = url

    def health_check(self):
        response = requests.get(self.url + "/")
        print(response.json())

    def send_raw_data(self, json_file):
        with open(json_file,"r") as f:
            data = json.load(f)
        response = requests.post(self.url + "/orders", json=data)
        print(response.json())

    def clean_orders(self):
        response = requests.post(self.url + "/process_orders")
        print(response.json())

    def get_summary(self):
        response = requests.get(self.url + "/analytics_summary")
        print(response.json())