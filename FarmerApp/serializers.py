from rest_framework import serializers
from .models import *

class CropSeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSeeds
<<<<<<< HEAD
        fields = ('id','name','s_type','price','quality','photo')
=======
        fields = ('id','name','s_type','price','quality','photo')
>>>>>>> e0097b4b9c618fd29f500de87f4fbe77b062d91b
