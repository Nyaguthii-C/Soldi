from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    monthly_target = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=10,
        default="KES"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class ExpenseCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Expense(models.Model):

    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    description = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expense_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    month = models.PositiveSmallIntegerField()

    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"



class BudgetCategory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budget_categories"
    )

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE
    )

    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"    