from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lms.models import Product, Subscription, Lesson, Group

# admin.site.register(UserAdmin)
admin.site.register(Product)
admin.site.register(Subscription)
admin.site.register(Lesson)
admin.site.register(Group)
