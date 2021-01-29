import requests
import json
from requests.auth import HTTPBasicAuth



username = "MK_TEST_8UBXGKTFSB"
password = "ENRC4FDYKSTUYQKA53YPXBFLUFXWYHG2"
contract = "2917634474"
baseurl = "https://sandbox.monnify.com"
walletId = "654CAB2118124760A659C787B2AA38E8"

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
    
    def ReserveAccount(self,email, mobile):
        url = f'{baseurl}/api/v1/bank-transfer/reserved-accounts'
        key = Auth()
        payload = {
            "accountReference": mobile,
            "accountName": mobile,
            "currencyCode": "NGN",
            "contractCode": contract,
            "customerEmail": email, 
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

    
    def VerifyAccount(self, acctno, bcode):
        url = f'{baseurl}/api/v1/disbursements/account/validate?accountNumber={acctno}&bankCode={bcode}'

        payload = {}
        headers= {}

        response = requests.request("GET", url, headers=headers, data = payload)

        r_dict = json.loads(response.text)
        return r_dict

    
    def BankTransfer(self, amount, txnid, desc, bcode, acctno):
        url = f'{baseurl}/api/v1/disbursements/single'

        payload = {
            'amount': amount,
            'reference': txnid,
            'narration': desc,
            'bankCode': bcode,
            'accountNumber': acctno,
            'currency': 'NGN',
            'walletId': walletId
            }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, data = json.dumps(payload))

        r_dict = json.loads(response.text)
        return r_dict