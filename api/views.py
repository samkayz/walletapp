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
from monify import *

# Create your views here.
MyClass = Main()
User = get_user_model()
mon = Monnify()



@api_view(['POST'])
@permission_classes([])
def signup(request):
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
        MyClass.Signup(mobile, pwd, role)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "reason": "Account created"
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
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
