from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .emails import *
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = authenticate(email = email, password = password)
                
                if user is None:
                    return Response({
                'status':400,
                'message':'Invalid Credentials!!',
                'data':{}
                })

                if user.is_verified is False:
                    return Response({
                'status':400,
                'message':'your account is not verified',
                'data':{}
                })

                refresh = RefreshToken.for_user(user)

                return Response( {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })

            return Response({
                'status':400,
                'message':'User not created',
                'data':serializer.errors
                })
            
        except Exception as e:
            return Response({
                'status':400,   
                'message':str(e),
                'data':{}
                })  


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                # send email
                send_otp_via_email(data['email'])
                return Response({
                    'status':200,
                    'message':'User created successfully',
                    'data':serializer.data
                    })
            else:
                return Response({
                    'status':400,
                    'message':'User not created',
                    'data':serializer.errors
                    })
            
        except Exception as e:
            return Response({
                'status':400,   
                'message':str(e),
                'data':{}
                })
        

class VerifyOTPAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email = email)
                if not user.exists():
                    return Response({
                    'status':400,
                    'message':'User not created',
                    'data':'Invalid Email!!'
                    })
                
                if user[0].otp != otp:

                    return Response({
                    'status':400,
                    'message':'Something went wrong!',
                    'data':'Invalid otp!!'
                    })
                
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status':200,
                    'message':'Account Verified!!',
                    'data':{}
                    })
            else:
                return Response({
                    'status':400,
                    'message':'User not created',
                    'data':serializer.errors
                    })
            
        except Exception as e:
            return Response({
                'status':400,   
                'message':str(e),
                'data':{}
                })