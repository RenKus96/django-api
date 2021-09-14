from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, required=True)
    country = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

        return instance

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=150, required=True)
    publisher = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    year = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.year = validated_data.get('year', instance.year)
        instance.save()

        return instance

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
