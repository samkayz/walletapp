from django.shortcuts import render
from function import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from web.models import *
from rest_framework import status
from rest_framework.response import Response
import random
import string
from datetime import datetime
from monify import *

# Create your views here.
MyClass = Main()
User = get_user_model()
mon = Monnify()

ex = 100

@api_view(['POST'])
@permission_classes([])
def signup(request):
    email = request.data.get('email')
    mobile = request.data.get('mobile')
    pwd = request.data.get('pwd')
    role = request.data.get('role')

    if User.objects.filter(mobile=mobile).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Mobile number is a register member"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif len(mobile) > 11 or len(mobile) < 11:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Wrong Mobile Number Format"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif mobile[0] != '0':
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Wrong Mobile Number Formats"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif len(pwd) > 4:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Pin Can't be more than 4 digit"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        MyClass.Signup(email, mobile, pwd, role)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "reason": "Account created"
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request, mobile):
    try:
        bal = MyClass.GetWalletBall(mobile)

        data = {
            "code": status.HTTP_200_OK,
            "bal": f'{bal.bal}',
            "acctNo": f'{bal.acctno}',
            "bank": f'{bal.bank}'
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    except:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request, mobile):
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    amount = request.data.get('amount')
    rec = request.data.get('reciever')
    pin = request.data.get('pin')
    checkPin = MyClass.CheckPin(mobile, pin)
    if checkPin == True:
        checkbal = MyClass.CheckBal(mobile, amount)
        if checkbal == True:
            if User.objects.filter(mobile=rec).exists():
                if mobile == rec:
                    data = {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "status": "fail",
                        "reason": "You can't send money to yourself"
                    }
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    amt = float(amount)
                    MyClass.SendMoney(amount, mobile, rec)
                    MyClass.CreateLog(mobile, rec, txt_id, amt, now, status="PAID", desc="Wallet Transfer")
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "reason": f'{amt} was sent to {rec}'
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": "User not found"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accountVerify(request):
    acctno = request.data.get('accountNumber')
    bcode = request.data.get('bankCode')

    verify = mon.VerifyAccount(acctno, bcode)
    stat = verify['requestSuccessful']
    if stat == True:
        body = verify['responseBody']
        acct = body['accountNumber']
        acctname = body['accountName']
        bankCode = body['bankCode']

        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "accountNumber": acct,
            "accountName": acctname,
            "bankCode": bankCode,

        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    else:
        msg = verify['responseMessage']
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": msg
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def btranfer(request, mobile):
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    txn = str(res)
    txt_id = "TX" + txn
    base_date_time = datetime.now()
    now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M %p"))
    amount = request.data.get('amount')
    rec = request.data.get('accountNumber')
    bcode = request.data.get('bankCode')
    pin = request.data.get('pin')
    desc = "USSD"
    stat = "PAID"
    checkPin = MyClass.CheckPin(mobile, pin)
    if User.objects.filter(mobile=mobile).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Account doestn't exist within the system"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif checkPin == True:
        ammt = (float(ex) + float(amount))
        checkbal = MyClass.CheckBal(mobile, ammt)
        if checkbal == True:
            trans = mon.BankTransfer(amount, txt_id, desc, bcode, rec )
            statrep = trans['requestSuccessful']
            if statrep == True:
                body = trans['responseBody']
                fee = float(body['totalFee'])
                amt = (fee + float(amount))
                MyClass.BankTransfer(mobile, amt)
                MyClass.CreateLog(mobile, rec, txt_id, amount, now, stat, desc, fee)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "sucess",
                    "amount": amount,
                    "fee": fee,
                    "reason": f'You have sent {float(amount)} to {rec}'
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                msg = trans['responseMessage']
                data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "status": "fail",
                    "reason": msg
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "status": "fail",
                "reason": "Insufficient balance"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "status": "fail",
            "reason": "Invalid Transaction Pin"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


