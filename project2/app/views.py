from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .emails import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
# Create your views here.

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

                user = CustomUser.objects.filter(email = email)
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


class LoginAPI(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = authenticate(email=email, password=password)
                
                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid Credentials',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not user.is_verified:
                    return Response({
                        'status': 400,
                        'message': 'Your account is not verified',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)

                return Response({
                    'status': 200,
                    'message': 'Login successful',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })

            return Response({
                'status': 400,
                'message': 'Invalid request data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'status': 500,   
                'message': 'Internal Server Error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserProfileSerializer(user)
            return Response({
                'status': 200,
                'message': 'User profile',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            user = request.user
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'User profile updated successfully',
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': 400,
                    'message': 'Invalid data',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)