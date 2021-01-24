from web.models import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as dj_login, logout as s_logout
from django.contrib.auth import user_logged_in
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
User = get_user_model()
import os
import random
import string
import uuid
import datetime
import time
from monify import *


mon = Monnify()


class Main:
    def Signup(self, mobile, pwd, role):
        res = mon.ReserveAccount(mobile)
        
        status = res[1]
        if status == True:
            accountNumber = res[0]['accountNumber']
            bankName = res[0]['bankName']

            user = User.objects.create_user(email="", mobile=mobile, password=pwd, role=role)
            wal = Wallet(mobile=mobile, acctno=accountNumber, bank=bankName)
            user.save()
            wal.save()
            pass

        else:
            print(status)
            pass

    
    def GetWalletBall(self, mobile):
        bal = Wallet.objects.all().get(mobile=mobile)
        return bal