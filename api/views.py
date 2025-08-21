from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate

from ChatApp.models import ChatMessages
from hospital.models import Hospital_Information, Patient, User 
from doctor.models import Doctor_Information
from .serializers import HospitalSerializer, ChatMessageSerializer, DoctorSerializer, PharmacySerializer, SSLCommerzPatientSerializer
from pharmacy.models import Pharmacy
from sslcommerz.models import SSLCommerzPatient


@api_view(['GET'])
def getRoutes(request):
    # Specify which urls (routes) to accept
    
    routes = [
        {'GET': '/api/hospital/'},
        {'GET': '/api/hospital/id'},

        # to test built-in authentication - JSON web tokens have an expiration date
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

# @permission_classes([IsAuthenticated]) # set up a restricted route

@api_view(['GET'])
def getHospitals(request):
    hospitals = Hospital_Information.objects.all() # query the database (get python object)
    serializer = HospitalSerializer(hospitals, many=True) # convert python object to JSON object
    # many=True because we are serializing a list of objects
    return Response(serializer.data)


@api_view(['GET'])
def getHospitalProfile(request, pk):

    hospitals = Hospital_Information.objects.get(hospital_id=pk)
    serializer = HospitalSerializer(hospitals, many=False) # many=False for a single object
    return Response(serializer.data)


# Patients API

# Doctor API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDoctors(request):
    queryset = Doctor_Information.objects.all()
    name = request.GET.get('name')
    specialty = request.GET.get('specialty')
    city = request.GET.get('city')
    if name:
        queryset = queryset.filter(name__icontains=name)
    if specialty:
        queryset = queryset.filter(specialty__icontains=specialty)
    if city:
        queryset = queryset.filter(city__icontains=city)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = DoctorSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# Hospital search/listing API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchHospitals(request):
    queryset = Hospital_Information.objects.all()
    name = request.GET.get('name')
    city = request.GET.get('city')
    type_ = request.GET.get('type')
    if name:
        queryset = queryset.filter(name__icontains=name)
    if city:
        queryset = queryset.filter(city__icontains=city)
    if type_:
        queryset = queryset.filter(type__icontains=type_)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = HospitalSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# SSLCommerz patient API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSSLCommerzPatients(request):
    queryset = SSLCommerzPatient.objects.all()
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    if email:
        queryset = queryset.filter(email__icontains=email)
    if phone:
        queryset = queryset.filter(phone__icontains=phone)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = SSLCommerzPatientSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# Pharmacy search/listing/payment API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPharmacies(request):
    queryset = Pharmacy.objects.all()
    name = request.GET.get('name')
    city = request.GET.get('city')
    if name:
        queryset = queryset.filter(name__icontains=name)
    if city:
        queryset = queryset.filter(city__icontains=city)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = PharmacySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# Pharmacy Payment Endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pharmacyPayment(request):
    pharmacy_id = request.data.get('pharmacy_id')
    patient_id = request.data.get('patient_id')
    amount = request.data.get('amount')
    # Here you would integrate with payment gateway (e.g., SSLCommerz)
    # For now, just return a mock response
    return Response({
        'success': True,
        'pharmacy_id': pharmacy_id,
        'patient_id': patient_id,
        'amount': amount,
        'message': 'Payment processed (mock)'
    })
# Serializers (stubs, place in api/serializers.py if not present)
# Chat and Video Call Endpoints

# List chat messages for a patient or doctor
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getChatMessages(request):
    user_id = request.GET.get('user_id')
    doctor_id = request.GET.get('doctor_id')
    queryset = ChatMessages.objects.all()
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    if doctor_id:
        queryset = queryset.filter(doctor_id=doctor_id)
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ChatMessageSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# Send a chat message
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendChatMessage(request):
    user_id = request.data.get('user_id')
    doctor_id = request.data.get('doctor_id')
    message = request.data.get('message')
    chat = ChatMessages.objects.create(user_id=user_id, doctor_id=doctor_id, message=message)
    serializer = ChatMessageSerializer(chat, many=False)
    return Response({'success': True, 'chat': serializer.data})

# Video Call Endpoints (mock)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def startVideoCall(request):
    caller_id = request.data.get('caller_id')
    receiver_id = request.data.get('receiver_id')
    channel_name = request.data.get('channel_name')
    # In a real app, you would generate a token and channel for Agora or similar
    return Response({
        'success': True,
        'caller_id': caller_id,
        'receiver_id': receiver_id,
        'channel_name': channel_name,
        'agora_token': 'MOCK_TOKEN',
        'message': 'Video call started (mock)'
    })
# from rest_framework import serializers
# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor_Information
#         fields = '__all__'
# class PharmacySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pharmacy
#         fields = '__all__'
# class SSLCommerzPatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SSLCommerzPatient
#         fields = '__all__'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatients(request):
    # Filtering
    queryset = Patient.objects.all()
    name = request.GET.get('name')
    email = request.GET.get('email')
    if name:
        queryset = queryset.filter(name__icontains=name)
    if email:
        queryset = queryset.filter(email__icontains=email)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = SSLCommerzPatientSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatientProfile(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
        return Response({'detail': 'Patient not found.'}, status=404)
    serializer = SSLCommerzPatientSerializer(patient, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def patientLogin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is not None and hasattr(user, 'patient'):
        serializer = SSLCommerzPatientSerializer(user.patient, many=False)
        return Response({'success': True, 'patient': serializer.data})
    return Response({'success': False, 'error': 'Invalid credentials'}, status=401)
