from rest_framework import serializers
from django.db.models import Count
from django.contrib.auth.models import User

from lms.models import Product, Subscription, Lesson, Group


class ProductSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_author_name(self, obj):
        return obj.author.get_full_name()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ProductStatisticsSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "students_count",
            "groups_fill_percentage",
            "purchase_percentage",
        ]

    def get_students_count(self, obj):
        return obj.groups.aggregate(total=Count("users"))["total"]

    def get_groups_fill_percentage(self, obj):
        total_users_in_groups = obj.groups.aggregate(total=Count("users"))["total"]
        groups_count = obj.groups.count()
        if groups_count:
            avg_fill = (
                total_users_in_groups / (obj.max_group_size * groups_count)
            ) * 100
            return avg_fill
        return 0

    def get_purchase_percentage(self, obj):
        total_subscriptions = obj.subscribed_products.count()
        total_users = User.objects.count()
        if total_users:
            return (total_subscriptions / total_users) * 100
        return 0
