import requests

url = "https://httpbin.org/post"
data = {
    "name": "Lia",
    "project": "wifi-locator"
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
