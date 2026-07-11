# Business logic
from datetime import date
from django.db.models import Sum
from .models import (
    Expense,
    BudgetCategory
)


# create one expense
def create_expense(user, expense_data):

    # category = None

    # if expense_data["category"]:

        # category = ExpenseCategory.objects.filter(
        #     name=expense_data["category"]
        # ).first()

    return Expense.objects.create(

        user=user,

        category=expense_data["category"],

        description=expense_data["description"],

        amount=expense_data["amount"],

        expense_date=date.today()
    )



# create multiple expenses
def create_expenses(user, parsed_expenses):

    expenses = []

    for expense_data in parsed_expenses:

        expenses.append(

            create_expense(
                user,
                expense_data
            )

        )

    return expenses


# total spent in a month by a user
def get_month_total(user, year, month):

    return (

        Expense.objects.filter(

            user=user,

            expense_date__year=year,

            expense_date__month=month

        ).aggregate(

            total=Sum("amount")

        )["total"]

        or 0

    )


# category summary
def get_category_summary(user, year, month):

    categories = ExpenseCategory.objects.all()

    summary = []

    for category in categories:

        spent = (

            Expense.objects.filter(

                user=user,

                category=category,

                expense_date__year=year,

                expense_date__month=month

            ).aggregate(

                total=Sum("amount")

            )["total"]

            or 0

        )

        budget = (

            BudgetCategory.objects.filter(

                user=user,

                category=category

            ).first()

        )

        monthly_limit = budget.monthly_limit if budget else None

        remaining = None
        percentage = None

        if monthly_limit:

            remaining = monthly_limit - spent

            percentage = round(

                (spent / monthly_limit) * 100,

                2

            )

        summary.append({

            "category": category.name,

            "spent": spent,

            "budget": monthly_limit,

            "remaining": remaining,

            "percentage_used": percentage

        })

    return summary


# monthly summary
def get_monthly_summary(user, year, month):

    profile = user.profile

    total_spent = get_month_total(
        user,
        year,
        month
    )

    remaining = profile.monthly_target - total_spent

    return {

        "year": year,

        "month": month,

        "currency": profile.currency,

        "monthly_budget": profile.monthly_target,

        "total_spent": total_spent,

        "remaining": remaining,

        "categories": get_category_summary(
            user,
            year,
            month
        )
    }