from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init, pre_init
import requests


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    totalCoins = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def getFullName(self):
        return self.user.first_name + " " + self.user.last_name


class Block(models.Model):
    nonce = models.FloatField(default=0)
    hashPre = models.CharField(max_length=500)
    hashCur = models.CharField(max_length=500)
    reward = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    mined_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True)


class Transaction(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, related_name="trans_sender")
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True)
    amount = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    block = models.ForeignKey(
        Block, on_delete=models.CASCADE, blank=True, null=True)
