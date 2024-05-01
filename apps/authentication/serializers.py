from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=4, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=6)
    username = serializers.CharField(max_length=255, min_length=1)
    first_name = serializers.CharField(max_length=255, min_length=1)
    last_name = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"Email": "Email taken"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"Username": "Username taken"})
        return super().validate(args)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=42)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        return user
