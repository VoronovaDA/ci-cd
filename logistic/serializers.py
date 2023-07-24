from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position in positions:
            StockProduct.objects.create(**position, stock=stock)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        pos = list(instance.positions.all())
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        for position in positions:
            p = pos.pop(0)
            p.product = position.get('product', p.product)
            p.quantity = position.get('quantity', p.quantity)
            p.price = position.get('price', p.price)
            p.save()
        return instance
