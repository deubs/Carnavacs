import requests

url = 'http://192.168.40.102:8080/'

response = requests.get(url)
print(response.status_code)
print(response.text)