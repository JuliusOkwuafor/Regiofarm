from rest_framework import generics
from .serializers import SellerSerializer
from seller.models import Seller
from utils.permissions import IsUserORAdmin
# Create your views here.

class SellerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = "pk"
    permission_classes = [IsUserORAdmin]