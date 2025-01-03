from requests import post

keys = {'key1': 'ed5976ff-2a98-470a-b90e-bf945d25c5c9',
'key2': '840c53ea-0467-4b52-b083-2de869d939a8',
'key3': '2329db1e-95e8-4265-986e-d02114dbf5dc'}

apiurl = "https://boleteria.carnavaldelpais.com.ar/api/Ticket/Validate"
apiurlb = "https://api.carnavaldelpais.com.ar/Ticket/Validate"


def processResponse(response):
    print(response)
    apistatus = response['success']
    apimessage = response['message']
    ticketstatus = response['result']['ticketStatus']
    name = response['result']['ticketStatus']['name']
    ticketId = response['result']['ticketId']
    isValid = response['result']['isValid']
    ticketExists = response['result']['exists']
    return {'code': isValid and ticketExists,'text': apimessage}


def apicall(code):
    apikey = keys['key1']
    header = {
        'X-API-Key': f'{apikey}',
        'Content-Type': "application/json"
    }
    payload = {'code': code}
    try:
        response = post(apiurl, params=payload, headers=header)
        if response.status_code == 200:
            result = processResponse(response.json())
            print(result['code'])
            print(result['text'])
            return response.content
        if response.status_code == 401:
            print(response.content)
            return {'code':401, 'status':401}
    except Exception as e:
        print(e)
        return {'': ''}


if __name__ == "__main__":
    code =  "103225458952"
    apicall(code)


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