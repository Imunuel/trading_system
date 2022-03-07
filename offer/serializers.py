from rest_framework import serializers

from .models import SimpleOffer, PremiumOffer, Trade
from shares.models import Share
from users.serializers import UserSerializer


class ActivateAllOfferSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'name',
        )

class SimpleOfferSerializer(serializers.ModelSerializer):
    share = ShareSerializer()

    class Meta:
        model = SimpleOffer
        fields = (
            'id',
            'share',
            'count',
            'current_count',
            'order_type',
            'is_active',
        )

class PremiumOfferSerializer(serializers.ModelSerializer):
    share = ShareSerializer()

    class Meta:
        model = PremiumOffer
        fields = (
            'id',
            'share',
            'count',
            'current_count',
            'price',
            'order_type',
            'is_active',
        )


class CreateSimpleOfferSerialiazer(serializers.ModelSerializer):
    share = ShareSerializer()

    class Meta:
        model = SimpleOffer
        fields = (
            'share',
            'count',
            'order_type',
            'is_active'
        )


class CreatePremiumOfferSerialiazer(serializers.ModelSerializer):
    share = ShareSerializer()
    
    class Meta:
        model = PremiumOffer()
        fields = (
            'share',
            'count',
            'price',
            'order_type',
            'is_active'
        )


class UpdateMySimpleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleOffer
        fields = (
            'order_type',
            'is_active'
        )


class UpdateMyPremiumOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumOffer
        fields = (
            'price',
            'order_type',
            'is_active'
        )


class DeleteSimpleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleOffer
        fields = ('id',)


class DeletePremiumOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumOffer
        fields = ('id',)


class TradeSerializer(serializers.ModelSerializer):
    share = ShareSerializer()
    buyer = UserSerializer()
    seller = UserSerializer()
    class Meta:
        model = Trade
        fields = (
            'share',
            'quantity',
            'cost',
            'buyer',
            'seller'
        )