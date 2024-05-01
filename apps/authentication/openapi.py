from drf_yasg import openapi

role = openapi.Parameter(
    "role",
    openapi.IN_QUERY,
    description="Role of the user",
    type=openapi.TYPE_STRING,
    enum=("user", "admin"),
)
registered_response = {
    201: openapi.Response(
        description="User created successfully",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_201_CREATED"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error creating user",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "msg": openapi.Schema(
                            type=openapi.TYPE_OBJECT, description="Error creating user"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                    },
                )
            }
        },
    ),
}

registered_seller_response = {
    201: openapi.Response(
        description="Seller created successfully",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_201_CREATED"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error creating seller",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "msg": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Error creating seller",
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                    },
                )
            }
        },
    ),
}

verify_email_response = {
    202: openapi.Response(
        description="Email confirmation successful",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_202_ACCEPTED"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Invalid token or user not found",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                    },
                )
            }
        },
    ),
}

login_response = {
    200: openapi.Response(
        description="User logged in successfully",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="User data based on your serializer definition",
                        ),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_200_OK"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error during login",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "msg": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Error during login",
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                    },
                )
            }
        },
    ),
}


request_email_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["email"],
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's email address"
        )
    },
)

request_email_response = {
    200: openapi.Response(
        description="Password reset email sent",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_200_OK"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error descriptions",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                    },
                )
            }
        },
    ),
    500: openapi.Response(
        description="Error descriptions",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="HTTP_500_INTERNAL_SERVER_ERROR",
                        ),
                    },
                )
            }
        },
    ),
}

check_reset_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["email", "otp"],
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's email address"
        ),
        "otp": openapi.Schema(
            type=openapi.TYPE_STRING, description="One-Time Password"
        ),
    },
)

check_reset_response = {
    200: openapi.Response(
        description="Valid OTP",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_200_OK"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error descriptions",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                    },
                )
            }
        },
    ),
}

reset_password_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["email", "otp", "password"],
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's email address"
        ),
        "otp": openapi.Schema(
            type=openapi.TYPE_STRING, description="One-Time Password"
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="New password",
        ),
    },
)

reset_password_response = {
    200: openapi.Response(
        description="Password reset successful",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_200_OK"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error descriptions",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                    },
                )
            }
        },
    ),
}

change_password_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["old_password", "new_password"],
    properties={
        "old_password": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's current password"
        ),
        "new_password": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="New password meeting complexity requirements",
        ),
    },
)

change_password_response = {
    200: openapi.Response(
        description="Password changed successfully",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Success message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Success code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_200_OK"
                        ),
                    },
                )
            }
        },
    ),
    400: openapi.Response(
        description="Error descriptions",
        content={
            "application/json": {
                "schema": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(type=openapi.TYPE_OBJECT, default={}),
                        "msg": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Error message"
                        ),
                        "code": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Error code"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, default="HTTP_400_BAD_REQUEST"
                        ),
                    },
                )
            }
        },
    ),
}
