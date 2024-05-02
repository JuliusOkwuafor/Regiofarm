from rest_framework.views import APIView
from utils.permissions import IsUserORAdmin
from rest_framework import  generics
from rest_framework.response import Response

# Create your views here.
from utils.response import APIResponse

from .serializers import UserSerializer
from user.models import User


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"
    permission_classes = [IsUserORAdmin]

