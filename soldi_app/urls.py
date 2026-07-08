from .views import (
    register, get_profile, update_profile, get_budget,
    update_budget, category_summary,
    delete_expense, update_expense, get_expense, list_expenses, todays_expenses,
    log_expense, monthly_summary
)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("register/", register,  name="register"),

    path ("profile/", get_profile, name="get_profile"),
    path ("profile/update/", update_profile, name="update_profile"),

    path ("budget/", get_budget, name="get_budget"),
    path ("budget/update/", update_budget, name="update_budget"),

    path ("expenses/", list_expenses, name="list_expenses"),
    path ("expenses/today/", todays_expenses, name="todays_expenses"),
    path ("expenses/<int:pk>/", get_expense, name="get_expense"),
    path ("expenses/<int:pk>/update/", update_expense, name="update_expense"),
    path ("expenses/<int:pk>/delete/", delete_expense, name="delete_expense"),
    path ("expenses/log/", log_expense, name="log_expense"),

    path ("summary/monthly/", monthly_summary, name="monthly_summary"),
    path ("summary/categories/", category_summary, name="category_summary"),
]