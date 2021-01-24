import requests
import json
from requests.auth import HTTPBasicAuth



username = "MK_TEST_8UBXGKTFSB"
password = "ENRC4FDYKSTUYQKA53YPXBFLUFXWYHG2"
contract = "2917634474"
baseurl = "https://sandbox.monnify.com"

def Auth():
    response = requests.post(f'{baseurl}/api/v1/auth/login', 
    auth=HTTPBasicAuth(username, password))

    response_dict = json.loads(response.text)
    h = []
    for i in response_dict:
        data = response_dict[i]
        h.append(data)
    e = []
    for r in h[3]:
        toke = h[3][r]
        e.append(toke)
    a = "Bearer"+ " " + e[0]
    return a
__name__ == "__main__"


class Monnify:
    
    def ReserveAccount(self, mobile):
        url = f'{baseurl}/api/v1/bank-transfer/reserved-accounts'
        key = Auth()
        payload = {
            "accountReference": mobile,
            "accountName": mobile,
            "currencyCode": "NGN",
            "contractCode": contract,
            "customerEmail": 'system@gmail.com', 
            "customerName": mobile 
            }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': key
            }

        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

        #print(response.text.encode('utf8'))
        r_dict = json.loads(response.text)
        resv = []
        for j in r_dict:
            data = r_dict[j]
            resv.append(data)
        res = resv[3]
        stat = resv[0]
        # print(r_dict)
        return res, stat