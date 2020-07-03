<<<<<<< HEAD
from rest_framework import serializers
from .models import *

class CropSeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSeeds
        fields = ('id','name','s_type','price','quality','photo')
=======
from rest_framework import serializers
from .models import *

class CropSeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSeeds
        fields = ('id','name','s_type','price','quality','photo')
>>>>>>> bcc54e9f47c0b444148c8487b1b68bf7a09fc3f8
