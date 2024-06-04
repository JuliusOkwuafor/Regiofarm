from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from user.models import User

from .models import Favorite, Order
from .serializers import OrderSerializer


class FavoriteUtils:
    @staticmethod
    def create_favorite(self, user: User, content_type_data: str, object_id: str):
        if not content_type_data or not object_id:
            return Response(
                {"error": "Missing content_type or object_id in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(content_type_data)
        app_label = content_type_data.split(".")[0]
        model = content_type_data.split(".")[-1]
        # print(ContentType.objects.filter(model="Product"))
        try:
            # import pdb;pdb.set_trace()
            content_type = ContentType.objects.get_by_natural_key(
                app_label=app_label, model=model
            )
            model = content_type.model_class()
            print(model)
            get_object_or_404(model, pk=object_id)
            # model.objects.get(
            #     pk=object_id
            # )  # Raise DoesNotExist if product doesn't exist
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content_type or object_id provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Favorite.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        ).exists():
            return Response(
                {"error": "You already favorited this item"},
                status=status.HTTP_409_CONFLICT,
            )

        favorite = Favorite.objects.create(
            user=user, content_type=content_type, object_id=object_id
        )
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_favorite(pk, user):
        try:
            favorite = Favorite.objects.get(pk=pk, user=user)
        except Favorite.DoesNotExist:
            return Response(
                {"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Delete the favorite object
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_object(self):
        return get_object_or_404(
            Order, pk=self.kwargs.get("pk"), owner=self.request.user
        )

