from rest_framework import serializers
from .models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User 
        fields = ['email','name','password','password2','tc']
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('password and confirm password do no match')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','email','name','tc']


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)

    class Meta:
            fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('password and confirm password do no match')
        user.set_password(password)
        user.save()
        return attrs
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)

    class Meta:
        fields = ['email',]

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)

            token = PasswordResetTokenGenerator().make_token(user)

            print('password reset token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link',link)
            body = 'welcome to ephraim and ephraim  softwares limited,click the following link to reset your password'+link
            data = {
                'subject':'reset your password',
                'body':body,
                'to_email':user.email
            }
            util.send_email(data)
            return attrs
        else:
            raise ValidationErr('you are not a registered user')
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)

    class Meta:
            fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('password and confirm password do no match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs       
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('token is not valid or expired')
