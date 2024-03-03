from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User

from lms.models import Product, Group, Subscription
from lms.serializers import LessonSerializer, ProductSerializer, ProductStatisticsSerializer


class GroupsManagementView(APIView):
    """ Group management """

    def _get_user(self, user_id):
        """
        Private method to retrieve a user by their primary key.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def error_response(self, message):

         return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk=None):
        user_id = int(request.data.get('user_id'))
        # user_id = int(pk)
        user = self._get_user(user_id)
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        action = request.data.get('action')
        product_id = request.data.get('product')
        product = get_object_or_404(Product, pk=product_id)
        subscription = get_object_or_404(Subscription, product=product, user=user)

        if action == 'distribute':
            Group.objects.distribute_users(user, product)
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif action == 'add_user':
            try:
                Group.objects.add_user_to_group(user, product)
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return self.error_response(str(e))

        else:
            return self.error_response('Invalid action')


class ProductList(ListAPIView):
    queryset = Product.objects.annotate(
        lessons_count=Count('lessons')
    ).order_by('-date_start')

    serializer_class = ProductSerializer


class ProductLessons(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        self.check_object_permissions(request, product)

        lessons = product.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response({'lessons': serializer.data})

class ProductStatisticsView(ListAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductStatisticsSerializer