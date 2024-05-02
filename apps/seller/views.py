from rest_framework import generics
from .serializers import SellerProfileSerializer
from seller.models import SellerProfile
from utils.permissions import IsUserORAdmin
# Create your views here.

class SellerProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellerProfileSerializer
    queryset = SellerProfile.objects.all()
    lookup_field = "pk"
    permission_classes = [IsUserORAdmin]