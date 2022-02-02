from rest_framework import serializers

from .models import SimpleOffer, PremiumOffer
from shares.models import Share
from users.serializers import UserSerializer



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