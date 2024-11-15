from .models import TWO_IMG2IMG
from django.db.models import fields
from rest_framework import serializers

class TWO_IMG2IMGSerializers(serializers.ModelSerializer):
    class Meta:
        model = TWO_IMG2IMG
        fields = '__all__'