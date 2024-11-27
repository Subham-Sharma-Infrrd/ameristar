import requests

url = 'http://127.0.0.1:5000/submit'
data = {
    "Address": "123 Main St",
    "City": "New York",
    "State": "NY",
    "County": "New York County",
    "Owner Name": "John Doe",
    "Job ID": "JOB12345",
    "Order ID": "ORD67890"
}

response = requests.post(url, json=data)
print(response.json())
