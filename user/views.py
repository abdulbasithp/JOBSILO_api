from rest_framework.viewsets import ViewSet
from .models import Account
from .serializers import SignUpSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .token import create_jwt_pair_tokens
from seeker.models import SeekerProfile
from recruiter.models import RecruiterProfile


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        role = request.data.get('role')
        email = request.data.get('email')

        if serializer.is_valid():
            serializer.save()
            if role == 'seeker':
                user = Account.objects.get(email=email)
                SeekerProfile.objects.create(seeker=user)
            elif role == 'recruiter':
                user = Account.objects.get(email=email)
                RecruiterProfile.objects.create(recruiter=user)
            else:
                print('user role supplied is not seeker of recruiter but base user created!')
            response = {
                'message': "User Created Successfully",
            }
        
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request:Request):
        """using email and password post request will return response tokens for authentication:
                request :   email & password,response :  access & refresh"""
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get("role")

        user = authenticate(email=email, password=password)

        if user is not None:
            user_role = Account.objects.get(email=email).role
            print(user_role)
            if role == 'seeker' and role != user_role:
                response= {
                    "message": "You have seeker Account, You are not allowed here!"
                }
            elif role == 'recruiter' and role!= user_role:
                response ={
                    'message': "You have recruiter Account, You are not allowed here!"
                }

            else:    
                tokens = create_jwt_pair_tokens(user)
                response = {
                    "message":"Login successfull",
                    "token": tokens,
                    "user" :{
                        "user_id":user.id,
                        "email":user.email,
                        "role":user.role
                    }

            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "message": "Invalid email or password!"
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request):
        content = {
            "user": str(request.user)
        }
        return Response(content, status=status.HTTP_200_OK)



