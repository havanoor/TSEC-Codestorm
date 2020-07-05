from rest_framework import serializers
from .models import *




class CropSeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSeeds
        fields = ('p_id','name','s_type','price','quality','image')
