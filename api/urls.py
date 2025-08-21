from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('hospital/', views.getHospitals),
    path('hospital/<str:pk>/', views.getHospitalProfile, name="hospital-profile"),
    path('patients/', views.getPatients, name="patients"),
    path('patients/<str:pk>/', views.getPatientProfile, name="patient-profile"),
    path('patients/login/', views.patientLogin, name="patient-login"),
    path('doctors/', views.getDoctors, name="doctors"),
    path('hospitals/search/', views.searchHospitals, name="search-hospitals"),
    path('sslcommerz/patients/', views.getSSLCommerzPatients, name="sslcommerz-patients"),
    path('pharmacies/', views.getPharmacies, name="pharmacies"),
    path('pharmacies/payment/', views.pharmacyPayment, name="pharmacy-payment"),
    path('chat/messages/', views.getChatMessages, name="chat-messages"),
    path('chat/send/', views.sendChatMessage, name="send-chat-message"),
    path('video-call/start/', views.startVideoCall, name="start-video-call"),
]
