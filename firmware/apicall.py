from requests import post, exceptions, Session
from datetime import datetime
keys = {'key1': 'ed5976ff-2a98-470a-b90e-bf945d25c5c9',
'key2': '840c53ea-0467-4b52-b083-2de869d939a8',
'key3': '2329db1e-95e8-4265-986e-d02114dbf5dc'}

apiurlb = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurl = "https://api.carnavaldelpais.com.ar/Ticket/Validate"


def processResponse(response):
    print(response)
    apistatus = response['success']
    m1 = response["result"]['m1']
    m2 = response['result']['m2']
    isValid = response['result']['isValid']
    return {'apistatus': apistatus, 'code': isValid, 'm1': m1, 'm2': m2}

def apicallSession(code):
    apikey = keys['key1']
    header = {
        'X-API-Key': f'{apikey}',
        'Content-Type': "application/json"
    }
    payload = {'code': code}
    s = Session()
    try:
        response = s.post(apiurl, params= payload, headers= header, timeout=1)
        if response.status_code == 200:
            result = processResponse(response.json())
            return result
        elif response.status_code == 401:
            print(response.status_code)
        elif response.status_code == 404:
            print(response.status_code)
        else:
            print('no response')
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}
    except exceptions.Timeout:
        print("The request timed out!")
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}
    except Exception as e:
        print(e)
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}


def apicall(code):
    apikey = keys['key1']
    header = {
        'X-API-Key': f'{apikey}',
        'Content-Type': "application/json"
    }
    payload = {'code': code}
    try:
        response = post(apiurl, params= payload, headers= header, timeout=1)
        if response.status_code == 200:
            result = processResponse(response.json())
            return result
        elif response.status_code == 401:
            print(response.status_code)
        elif response.status_code == 404:
            print(response.status_code)
        else:
            print('no response')
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}
    except exceptions.Timeout:
        print("The request timed out!")
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}
    except Exception as e:
        print(e)
        return {'apistatus': False, 'code': False, 'm1': 'BIENVENIDO', 'm2': 'ADELANTE'}


if __name__ == "__main__":
    code =  "103225458952"
    result = apicallSession(code)
    print(result)
    ticket_string = f'code: {code}, status: {result["code"]}, timestamp: {datetime.now()}, burned: {result["apistatus"]} \n'
    print(ticket_string)



"""
general de la api
Success: api response
message: 
result: 
    "ticketStatus": {type}

"""


#' b'{"success":true,"message":null,"result":{"ticketStatus":{"type":7,"id":7,"name":"NotFound"},"ticketId":0,"isValid":false,"exists":false}}'
# import requests
# url = "https://api.carnavaldelpais.com.ar/Ticket/Validate"
# headers = {
#     "Authorization": "ed5976ff-2a98-470a-b90e-bf945d25c5c9",
#     "Content-Type": "application/json"
# }
# response = requests.post(url, headers=headers)

# print(response.json())