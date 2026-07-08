from rest_framework import serializers
from .models import BudgetCategory, UserProfile, ExpenseCategory, Expense
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.password_validation import validate_password


class ExpenseSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=ExpenseCategory.objects.all(),
        slug_field="name",
        required=False,
        allow_null=True
    )

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )


class ExpensePromptSerializer(serializers.Serializer):

    prompt = serializers.CharField(
        max_length=500
    )


class UserProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:

        model = UserProfile

        fields = (
            "username",
            "email",
            "currency",
            "monthly_target",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


# create both user and userprofile automatically when registering a new user
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    monthly_target = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = serializers.CharField()


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value
    
    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password",
            "monthly_target",
            "currency",
        )

    def create(self, validated_data):

        monthly_target = validated_data.pop("monthly_target")
        currency = validated_data.pop("currency")

        user = User.objects.create_user(**validated_data)

        UserProfile.objects.create(
            user=user,
            monthly_target=monthly_target,
            currency=currency
        )

        return user


class BudgetCategorySerializer(serializers.ModelSerializer):

    category = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = BudgetCategory
        fields = "__all__"
        read_only_fields = ("user",)