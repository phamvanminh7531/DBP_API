from .models import TWO_IMG2IMG, TWO_IMG2IMG_WITH_PROMT
from django.db.models import fields
from rest_framework import serializers

class TWO_IMG2IMGSerializers(serializers.ModelSerializer):
    class Meta:
        model = TWO_IMG2IMG
        fields = '__all__'

class TWO_IMG2IMG_WITH_PROMTSerializers(serializers.ModelSerializer):
    class Meta:
        model = TWO_IMG2IMG_WITH_PROMT
        fields = '__all__'