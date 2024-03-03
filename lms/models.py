from math import ceil

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False, db_index=True)
    date_start = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    min_group_size = models.IntegerField()
    max_group_size = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', 'author'])
        ]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subscribed_products')

    def __str__(self):
        return self.product.name

    class Meta:
        indexes = [
            models.Index(fields=['user', 'product']),
        ]


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255, unique=True, blank=False, null=False, db_index=True)
    video = models.FileField(upload_to='videos/', default=None, blank=True, null=True, verbose_name="Видео")

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['product', 'name']),
        ]


class GroupManager(models.Manager):

    def add_user_to_group(self, user, product):
        """
        Distribution by max. value
        """
        groups = list(self.filter(product=product))
        if not groups:
            self.create_groups(product)
            groups = list(self.filter(product=product))

        groups.sort(key=lambda x: x.users.count())
        group = groups[0]
        if group.users.count() < product.max_group_size:
            group.users.add(user)
        else:
            raise Exception("All groups are full")

    def create_groups(self, product):
        """ Creates groups for the product """

        groups_count = ceil(product.max_users / product.max_group_size)

        for i in range(groups_count):
            name = f'{product.name} Group {i + 1}'
            self.create(name=name, product=product)

    def distribute_users(self, user, product):
        """ Distribution with deviation +/- 1"""

        groups = list(self.filter(product=product))

        sorted_groups = []

        for user in product.subscriptions.all():
            if not sorted_groups:
                sorted_groups = [groups[0]]
                sorted_groups[0].users.add(user)
            else:
                group = min(sorted_groups, key=lambda x: x.users.count())

                if len(sorted_groups) == 1 or abs(max(sorted_groups, key=lambda x: x.users.count()).users.count() - group.users.count()) <= 1:
                    group.users.add(user)
                else:
                    break

        self.add_user_to_group(user, product)


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    users = models.ManyToManyField(User, related_name='users_groups')
    name = models.CharField(max_length=255, db_index=True)

    objects = GroupManager()

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['product']),
        ]
