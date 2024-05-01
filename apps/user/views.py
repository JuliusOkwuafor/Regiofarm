from rest_framework.views import APIView

# Create your views here.
from utils.response import APIResponse


class UserView(APIView):
    def get(self, request):
        return APIResponse(data={"message": "Hello World!"})
