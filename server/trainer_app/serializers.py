from rest_framework import serializers

from .models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = ["id", "email", "password", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_token(self, trainer):
        return trainer.auth_token.key

    def create(self, validated_data):
        return Trainer.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        trainer = super().update(instance, validated_data)
        if password:
            trainer.set_password(password)
            trainer.save()
        return trainer
