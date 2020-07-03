from rest_framework import serializers
from .models import *

class CropSeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSeeds
        fields = ('id','name','s_type','price','quality','photo')