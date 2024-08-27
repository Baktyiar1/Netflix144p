from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import MyUser
from .serializers import UserRegisterSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import Response, APIView
from rest_framework import generics, permissions
from rest_framework import status


class UserRegistrationView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserRegisterSerializer


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: UserProfileSerializer()})
    def get(self, request):
        user = MyUser.objects.filter(id=request.user.id).first()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={200: UserProfileUpdateSerializer}
    )
    def patch(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
