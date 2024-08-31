from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from .serializers import (UserRegistrationSerializer,UserLoginSerializer,
                          UserProfileSerializer,UserPasswordChangeSerializer,SendPasswordResetEmailSerializer,
                          UserPasswordResetSerializer)
from django.contrib.auth import authenticate
from .renderers import UserRenderer

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
           email = serializer.data.get('email')
           password = serializer.data.get('password')
           user = authenticate(email=email,password=password)
           token = get_tokens_for_user(user)
           if user is not None:
               return Response({'token':token,'msg':'Login Successful'},status=status.HTTP_200_OK)
           else:
               return Response({'errors':{'non_field_errors':['email or password is not valid']}},
                               status=status.HTTP_404_NOT_FOUND)
        

class UserprofileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)  

class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):

        serializer = UserPasswordChangeSerializer(data=request.data,context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed Successfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def post(self,request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link sent.please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    def post(self,request,uid,token):
        serializer = UserPasswordResetSerializer(data=request.data,context = {'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successful'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

