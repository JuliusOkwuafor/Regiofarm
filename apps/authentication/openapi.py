from drf_yasg import openapi
from user.enums import TextChoices

role = openapi.Parameter(
    "role",
    openapi.IN_QUERY,
    description="Role of the user",
    type=openapi.TYPE_STRING,
    enum=TextChoices.choices,
)
