from rest_framework import serializers
from user.api.v1.serializers import CustomUserSerializer
from user.models import CustomUser
from django.utils.timezone import now
from ...models import Category, Event
from datetime import timedelta

class CategorySerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ("id","creator","title")
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class EventsSerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "creator",
	    "title",
            "category",
            "category_id",
            "create_date",
            "deadline",
            "send_email",
            "when_send_email",
        ]
        read_only_fields = ["id","create_date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["category_id"].queryset = Category.objects.filter(
                creator=request.user
            )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        send_email = attrs.get("send_email")
        when_send_email = attrs.get("when_send_email")
        deadline = attrs.get("deadline")

        if deadline and deadline <= now():
            raise serializers.ValidationError({
                "deadline" : "deadline has to be in the future"
            })

        if send_email:
            if when_send_email is None:
                raise serializers.ValidationError({
                    "when_send_email": "This field is required when send_email is true."
                })

            if when_send_email <= 0:
                raise serializers.ValidationError({
                    "when_send_email": "Must be a positive number of hours."
                })

            send_time = deadline - timedelta(hours=when_send_email)

            if send_time <= now():
                raise serializers.ValidationError({
                    "when_send_email": (
                        "Email send time has already passed. "
                        "Increase when_send_email or change deadline."
                    )
                })
        else:
            if when_send_email not in (None, 0):
                raise serializers.ValidationError({
                    "when_send_email": (
                        "Must be null or 0 when send_email is false."
                    )
                })

        return attrs
