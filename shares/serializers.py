from rest_framework import serializers

from .models import InventoryShare, Share


class FullShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'name',
            'full_name',
            'current_price',
            'past_price'
        )

class ShortShare(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = (
            'name',
            'full_name',
        )


class InventoryShareSerializer(serializers.ModelSerializer):
    share = ShortShare()
    class Meta:
        model = InventoryShare
        fields = (
            'share',
            'count'
        )