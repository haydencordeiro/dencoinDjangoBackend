from abc import ABCMeta
from re import S, T
import re
from django.db.models.fields import EmailField
from django.db.models.signals import pre_init
from django.shortcuts import render
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import time
from rest_framework.parsers import JSONParser
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth
import requests
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
from django.db.models import Sum
import collections
import json
from django.contrib.auth.models import User
from django.db.models import Count, Sum
import datetime
from datetime import datetime, timedelta, date
from django.db.models.functions import TruncMonth, TruncYear
import requests
import json
import random
from django.db.models import Q
import requests
import json
import uuid
from hashlib import new, sha256


@ api_view(('POST',))
def RegisterNewUserUser(request):
    temp = request.data.copy()
    if len(User.objects.filter(email=temp['email'])) > 0:
        return Response({'Error': 'Already Registered with this email'}, status=status.HTTP_400_BAD_REQUEST)
    if len(User.objects.filter(username=temp['username'])) > 0:
        return Response({'Error': 'This username already exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        tempUser = User(
            username=temp['username'],
            first_name=temp['first_name'],
            last_name=temp['last_name'],
            email=temp['email'],
        )
        tempUser.set_password(temp['password'])
        tempUser.save()
        tempCustomerProfile = UserProfile(
            user=tempUser,
            totalCoins=0
        )
        tempCustomerProfile.save()
    except:
        return Response(temp, status=status.HTTP_400_BAD_REQUEST)
    return Response(UserProfileSerializer(tempCustomerProfile).data, status=status.HTTP_201_CREATED)


@ api_view(('GET',))
@ permission_classes([IsAuthenticated])
def LoggedInUsersDetails(request):
    temp = UserProfile.objects.filter(user=request.user).first()
    return Response(UserProfileSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def CreateTransaction(request):
    findUser = User.objects.filter(email=request.data["receiveremail"]).first()
    temp = Transaction(
        sender=UserProfile.objects.filter(user=request.user).first(),
        receiver=UserProfile.objects.filter(user=findUser).first(),
        amount=float(request.data["amount"])

    )
    temp.save()
    temp.sender.totalCoins -= temp.amount
    temp.receiver.totalCoins += temp.amount
    temp.sender.save()
    temp.receiver.save()
    return Response(TransactionSerializer(temp).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
def AllPendingTransaction(request):
    temp = Transaction.objects.filter(block=None)
    return Response(TransactionSerializer(temp, many=True).data, status=status.HTTP_200_OK)


@ api_view(('POST',))
@ permission_classes([IsAuthenticated])
def MineBlock(request):

    prevBlock = Block.objects.last()
    # check if the nonce is corrent
    nonce = request.data["nonce"]
    newBlockHash = sha256((request.data["tobehashed"] +
                           str(nonce)).encode("ascii")).hexdigest()
    if (newBlockHash.startswith("00")) == False:
        return Response({'Error': 'Incorrect Nonce'}, status=status.HTTP_400_BAD_REQUEST)
    trans = Transaction.objects.filter(block=None)
    # create the block
    newBlock = Block(
        nonce=float(request.data["nonce"]),
        hashPre=prevBlock.hashCur,
        hashCur=newBlockHash,
        reward=prevBlock.reward-0.25,
        mined_by=UserProfile.objects.filter(user=request.user).first()

    )
    newBlock.save()
    # add all pending transactions to the block
    for i in trans:
        i.block = newBlock
        i.save()
    # reward
    # tempuser=UserProfile.objects.filter(user=request.user).first()
    # tempuser
    newBlock.mined_by.totalCoins = newBlock.mined_by.totalCoins + newBlock.reward
    newBlock.mined_by.save()
    return Response(BlockSerializer(Block.objects.all(), many=True).data, status=status.HTTP_200_OK)


@ api_view(('GET',))
# @ permission_classes([IsAuthenticated])
def MineBlockDetails(request):
    prevBlock = Block.objects.last()
    temp = ""
    temp += str(prevBlock.id)+" "
    for i in Transaction.objects.filter(block=None):
        temp += (i.sender.getFullName()+" send " +
                 i.receiver.getFullName()+" Rs. "+str(i.amount))
    temp += " "+str(prevBlock.hashCur)

    return Response({'tobehashed': temp}, status=status.HTTP_400_BAD_REQUEST)
