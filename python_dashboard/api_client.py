from requests import get, exceptions

apiurl_hello = 'http://localhost:5000/api/hello'
apiurl_pistol = 'http://localhost:5000/api/pistol'
apiurl_status = 'http://localhost:5000/api/status'
apiurl_code = 'http://localhost:5000/api/code'

def apicall(apiurl, payload):
    try:
        response = get(apiurl, params= payload, timeout=3)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print(response.status_code)
        elif response.status_code == 404:
            print(response.status_code)
        else:
            print('no response')
        return {'message': 'Hello, World!'}
    except exceptions.Timeout:
        print("The request timed out!")
        return {'message': 'Hello, World!'}
    except Exception as e:
        print(e)
        return {'message': 'Hello, World!'}
    
from  time import sleep

if __name__ == "__main__":
    name = 'Tango10'
    payload = {'name': name, 'ip': '192.168.40.210'}
    result = apicall(apiurl_hello, payload)
    print(result)
    ip = '192.168.40.210'
    pistol_status = 'On'
    payload = {'pistol': pistol_status, 'ip': ip}
    result = apicall(apiurl_pistol, payload)
    print(result)
    payload = {'ip': ip}
    for i in range(500):
        payload = {'ip': ip, 'status': 'locked'}
        apicall(apiurl_status, payload)
        print(payload)
        sleep(1)
        result = apicall(apiurl_code, payload)
        print(result)
        payload = {'ip': ip, 'status': 'unlocked'}
        apicall(apiurl_status, payload)
        print(payload)
        sleep(2)