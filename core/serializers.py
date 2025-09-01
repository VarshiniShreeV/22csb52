# shortener/serializers.py
import re
from rest_framework import serializers
from .models import ShortURL


class ShortURLCreateSerializer(serializers.ModelSerializer):
    validity = serializers.IntegerField(required=False, min_value=1, default=30)
    shortcode = serializers.CharField(required=False, allow_blank=True, max_length=15)

    class Meta:
        model = ShortURL
        fields = ('original_url', 'shortcode', 'validity')

    def validate_shortcode(self, value):
        if value:
            if not re.match(r'^[A-Za-z0-9_-]+$', value):
                raise serializers.ValidationError("Shortcode may only contain letters, numbers, '-' and '_'")
            if ShortURL.objects.filter(shortcode=value).exists():
                raise serializers.ValidationError("Shortcode already in use.")
        return value

    def create(self, validated_data):
        validity = validated_data.pop('validity', 30)
        shortcode = validated_data.pop('shortcode', None) or ''
        return ShortURL.objects.create(
            original_url=validated_data['original_url'],
            shortcode=shortcode,
            validity_minutes=validity
        )
