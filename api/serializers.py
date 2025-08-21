from rest_framework import serializers
from hospital.models import Hospital_Information, Patient, User 
from doctor.models import Doctor_Information
from pharmacy.models import Pharmacy
from sslcommerz.models import SSLCommerzPatient
from ChatApp.models import ChatMessages

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_Information
        fields = '__all__'

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'

class SSLCommerzPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSLCommerzPatient
        fields = '__all__'
# Serialization --> convert python data (from our database models) to JSON data

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital_Information
        fields = '__all__'


# class ProjectSerializer(serializers.ModelSerializer):
#     owner = ProfileSerializer(many=False)
#     tags = TagSerializer(many=True)
#     reviews = serializers.SerializerMethodField()

#     class Meta:
#         model = Project
#         fields = '__all__'

#     def get_reviews(self, obj):
#         reviews = obj.review_set.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return serializer.data
