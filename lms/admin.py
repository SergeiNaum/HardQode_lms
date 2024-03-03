from django.contrib import admin


from lms.models import Product, Subscription, Lesson, Group

admin.site.register(Product)
admin.site.register(Subscription)
admin.site.register(Lesson)
admin.site.register(Group)
