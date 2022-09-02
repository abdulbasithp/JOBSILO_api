from rest_framework import serializers
from .models import Account
from rest_framework.validators import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Account
        fields = ['first_name', 'middle_name', 'last_name', 'role', 'email', 'password']

    def validate(self, attrs):
        """"email validation"""
        email_exist = Account.objects.filter(email=attrs['email']).exists()

        if email_exist:
            raise ValidationError('The email is already exist')

        return super().validate(attrs)

    def create(self, validated_data):
        """hashing password"""
        password = validated_data.pop('password')

        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user












# class UserAccountSerializer(ModelSerializer):
#     class Meta:
#         model = Account
#         fields = '__all__'
#         extra_kwargs = { 'password':{'write_only':True}}

    # def create(self, validated_data):
    #     password = validated_data.pop('password',None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance