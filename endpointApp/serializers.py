
from rest_framework import serializers
from .models import *
from datetime import datetime
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(UserProfileSerializer,
                    self).to_representation(instance)
        for i in instance.user._meta.fields:
            if i.name != "password":
                rep["user"+str(i.name)] = getattr(instance.user, str(i.name))

        try:
            rep["last_login"] = instance.user.last_login.strftime(
                '%y-%m-%d %a %I:%M:%S')
        except:
            pass
        return rep


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(TransactionSerializer, self).to_representation(instance)
        rep["sender"] = instance.sender.user.first_name + " " +\
            instance.sender.user.last_name
        rep["receiver"] = instance.receiver.user.first_name + " " + \
            instance.receiver.user.last_name
        return rep


class BlockSerializer(serializers.ModelSerializer):
    depth = 1

    class Meta:
        model = Block
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(BlockSerializer, self).to_representation(instance)
        rep["nonce"] = int(instance.nonce)
        rep["mined_by"] = instance.mined_by.user.first_name + " " + \
            instance.mined_by.user.last_name
        return rep
