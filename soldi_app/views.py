from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import UserProfile, Expense
from django.shortcuts import get_object_or_404
from datetime import date
from .parser import parse_expense
from .services import create_expenses, get_category_summary, get_monthly_summary
from .serializers import (
    ExpensePromptSerializer,ExpenseSerializer, UserProfileSerializer,
    ExpenseSerializer, RegisterSerializer
)

# USER ONBOARDING

@swagger_auto_schema(
    method="post",
    operation_summary="Register a new user",
    operation_description="""
Registers a new user and automatically creates their UserProfile.

The request should include:

- username
- email
- password
- monthly_limit
- currency

Returns the newly created user details.
""",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="User registered successfully."
        ),
        400: "Validation Error"
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user together with their profile.
    """

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# USER PROFILE

@swagger_auto_schema(
    method="get",
    operation_summary="Get User Profile",
    operation_description="""
Returns the authenticated user's profile information,
including monthly target and preferred currency.
""",
    responses={
        200: UserProfileSerializer
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):

    profile = request.user.profile

    serializer = UserProfileSerializer(profile)

    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method="patch",
    operation_summary="Update User Profile",
    operation_description="""
Update the authenticated user's profile.

Only the following fields are editable:

- monthly_limit
- currency
""",
    request_body=UserProfileSerializer,
    responses={
        200: UserProfileSerializer,
        400: "Validation Error"
    }
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):

    profile = request.user.profile

    serializer = UserProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# BUDGET

@swagger_auto_schema(
    method="get",
    operation_summary="Get Monthly Budget",
    operation_description="""
Returns the user's monthly spending target.
""",
    responses={
        200: openapi.Response(
            description="Monthly budget."
        )
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_budget(request):

    profile = request.user.profile

    return Response({

        "monthly_limit": profile.monthly_limit,

        "currency": profile.currency

    })



@swagger_auto_schema(
    method="patch",
    operation_summary="Update Monthly Budget",
    operation_description="""
Updates the user's monthly budget target and/or currency.
""",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "monthly_limit": openapi.Schema(
                type=openapi.TYPE_NUMBER
            ),
            "currency": openapi.Schema(
                type=openapi.TYPE_STRING
            )
        }
    ),
    responses={
        200: "Budget Updated"
    }
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_budget(request):

    profile = request.user.profile

    if "monthly_limit" in request.data:
        profile.monthly_limit = request.data["monthly_limit"]

    if "currency" in request.data:
        profile.currency = request.data["currency"]

    profile.save()

    return Response({

        "message": "Budget updated successfully.",

        "monthly_limit": profile.monthly_limit,

        "currency": profile.currency

    })


# EXPENSES


@swagger_auto_schema(
    method="post",
    operation_summary="Log Expenses",
    operation_description="""
Logs one or more expenses from a natural language prompt.

Examples:

Bread 120

Bread 120
Milk 80
Bus fare 100

Netflix 700
""",
    request_body=ExpensePromptSerializer,
    responses={
        201: ExpenseSerializer(many=True),
        400: "Validation Error"
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def log_expense(request):

    serializer = ExpensePromptSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    prompt = serializer.validated_data["prompt"]

    parsed_expenses = parse_expense(prompt)

    if not parsed_expenses:

        return Response(
            {
                "message": "No valid expenses were detected."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    expenses = create_expenses(
        request.user,
        parsed_expenses
    )

    response_serializer = ExpenseSerializer(
        expenses,
        many=True
    )

    return Response(
        {
            "message": f"{len(expenses)} expense(s) logged successfully.",
            "expenses": response_serializer.data
        },
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method="get",
    operation_summary="List Expenses",
    operation_description="""
Returns all expenses belonging to the authenticated user.

Optional query parameters:

- year
- month
- category
""",
    manual_parameters=[
        openapi.Parameter(
            "year",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            "month",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        ),
    ],
    responses={200: ExpenseSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_expenses(request):

    expenses = Expense.objects.filter(user=request.user)

    year = request.GET.get("year")
    month = request.GET.get("month")
    category = request.GET.get("category")

    if year:
        expenses = expenses.filter(
            expense_date__year=year
        )

    if month:
        expenses = expenses.filter(
            expense_date__month=month
        )

    if category:
        expenses = expenses.filter(
            category__iexact=category
        )

    serializer = ExpenseSerializer(expenses, many=True)

    return Response(serializer.data)



@swagger_auto_schema(
    method="get",
    operation_summary="Retrieve  Single Expense",
    responses={200: ExpenseSerializer}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_expense(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user

    )

    serializer = ExpenseSerializer(expense)

    return Response(serializer.data)


@swagger_auto_schema(
    method="patch",
    operation_summary="Update Expense",
    request_body=ExpenseSerializer,
    responses={
        200: ExpenseSerializer,
        400: "Validation Error"
    }
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_expense(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user

    )

    serializer = ExpenseSerializer(

        expense,

        data=request.data,

        partial=True

    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(

        serializer.errors,

        status=status.HTTP_400_BAD_REQUEST

    )


@swagger_auto_schema(
    method="delete",
    operation_summary="Delete Expense",
    responses={
        204: "Expense deleted."
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_expense(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user

    )

    expense.delete()

    return Response(

        {

            "message":"Expense deleted successfully."

        },

        status=status.HTTP_204_NO_CONTENT

    )


@swagger_auto_schema(
    method="get",
    operation_summary="Today's Expenses",
    responses={200: ExpenseSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def todays_expenses(request):

    expenses = Expense.objects.filter(

        user=request.user,

        expense_date=date.today()

    )

    serializer = ExpenseSerializer(

        expenses,

        many=True

    )

    return Response(serializer.data)


# SUMMARY

@swagger_auto_schema(
    method="get",
    operation_summary="Monthly Expense Summary",
    operation_description="""
Returns a summary of spending for a given month.

Example:

/summary/monthly/?year=2026&month=7
""",
    manual_parameters=[
        openapi.Parameter(
            "year",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            "month",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Monthly summary"
        ),
        400: "Invalid Request"
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_summary(request):

    year = request.GET.get("year")
    month = request.GET.get("month")

    if not year or not month:
        return Response(
            {
                "error": "Both year and month are required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return Response(
            {
                "error": "Year and month must be integers."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    summary = get_monthly_summary(
        request.user,
        year,
        month
    )

    return Response(
        summary,
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    method="get",
    operation_summary="Category Spending Summary",
    operation_description="""
Returns the spending summary grouped by category for a given month.

Example:
GET /summary/categories/?year=2026&month=7
""",
    manual_parameters=[
        openapi.Parameter(
            "year",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="Year"
        ),
        openapi.Parameter(
            "month",
            openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=True,
            description="Month (1-12)"
        ),
    ]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_summary(request):

    year = request.GET.get("year")
    month = request.GET.get("month")

    if not year or not month:
        return Response(
            {"error": "Both year and month are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return Response(
            {"error": "Year and month must be integers."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if month < 1 or month > 12:
        return Response(
            {"error": "Month must be between 1 and 12."},
            status=status.HTTP_400_BAD_REQUEST
        )

    summary = get_category_summary(
        request.user,
        year,
        month
    )

    return Response(
        {
            "year": year,
            "month": month,
            "currency": request.user.profile.currency,
            "categories": summary
        },
        status=status.HTTP_200_OK
    )