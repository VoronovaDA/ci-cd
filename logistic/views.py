from django_filters import rest_framework as filter

from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockFilter(filter.FilterSet):
    products = filter.CharFilter(field_name='products__title', lookup_expr='icontains')

    class Meta:
        model = Stock
        fields = ['products']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.prefetch_related('positions').all()
    serializer_class = StockSerializer
    filter_backends = [filter.DjangoFilterBackend]
    filterset_class = StockFilter


@api_view(['GET'])
def test_page(request):
    return Response('Проверка автоматического деплоя')
