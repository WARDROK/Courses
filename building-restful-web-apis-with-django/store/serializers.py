from rest_framework import serializers

from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = ShoppingCartItem
        fields = ("product", "quantity")


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.DecimalField(
        read_only=True, max_digits=None, decimal_places=2
    )
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    price = serializers.DecimalField(
        min_value=1.00,
        max_value=100000,
        max_digits=None,
        decimal_places=2,
    )
    # price = serializers.FloatField(min_value=1.00, max_value=100000)
    sale_start = serializers.DateTimeField(
        required=False,
        input_formats=["%I:%M %p %d %B %Y"],
        format=None,
        allow_null=True,
        help_text="Accepted format is '12:01 PM 16 April 2019'",
        style={"input_type": "text", "placeholder": "12:01 PM 28 July 2019"},
    )
    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=["%I:%M %p %d %B %Y"],
        format=None,
        allow_null=True,
        help_text="Accepted format is '12:01 PM 16 April 2019'",
        style={"input_type": "text", "placeholder": "12:01 PM 28 July 2019"},
    )
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "sale_start",
            "sale_end",
            "is_on_sale",
            "current_price",
            "cart_items",
            "photo",
            "warranty",
        )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    def update(self, instance, validated_data):
        warranty_file = validated_data.pop("warranty", None)
        instance = super().update(instance, validated_data)

        if warranty_file:
            instance.description += "\n\nWarranty Information:\n"
            instance.description += b"; ".join(
                warranty_file.readlines()
            ).decode()
            instance.save()

        return instance

    def create(self, validated_data):
        validated_data.pop("warranty", None)
        return super().create(validated_data)


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )
