import rest_framework

from epilogue import models as epilogue_models, serializers as epilogue_serializers

from django.contrib.auth import password_validation

from passlib.hash import bcrypt

from analytics.models import UserSignupSource


from . import adapters, signals, exceptions as authentication_exceptions, models


class BaseRegistrationSerializer(rest_framework.serializers.Serializer):
    
    def user_create(self , validated_data):
        '''
        Create an instance of epilogue_models.LoginCustomer.
        If the ERPCustomer is present in the request, bind the epilogue_models.LoginCustomer instance to it. Otherwise create ERPCustomer Instance as well.
        '''
        if not getattr(self.context.get("request") , "user").is_anonymous:
            #ERPCustomer Exists
            customer = self.context.get("request").user
            if hasattr(customer , "logincustomer"):
                raise authentication_exceptions.UserAlreadyExists("Account With this email already exists")
            lc = epilogue_models.LoginCustomer.objects.create(
                email = validated_data['email'],
                password = bcrypt.hash(validated_data["password"]),
                customer = self.context['request'].user
            )
            customer.email = validated_data['email']
            customer.save()
            return lc
        else:
            email = validated_data['email']
            c = epilogue_models.Customer.objects.create(
                email = email
            )
            lc = epilogue_models.LoginCustomer.objects.create(
                email = email,
                password = bcrypt.hash(validated_data['password']),
                customer = c
            )
            return lc


class BaseSocialSerializer(rest_framework.serializers.Serializer):

    def create(self , credentials):

        email , first_name , last_name , picture = self.release_attrs(credentials)

        try:
            l = epilogue_models.LoginCustomer.objects.get(email = email)
        except epilogue_models.LoginCustomer.DoesNotExist as e:
            if self.context['request'].user.is_anonymous:
                print(email)
                customer,created = epilogue_models.Customer.objects.get_or_create(email = email)
                customer.image = picture
                customer.save()
                lc = epilogue_models.LoginCustomer.objects.create(
                    email = email,
                    first_name = customer.first_name or first_name,
                    customer = customer,
                                        password = ""
                )
                return lc
            else:
                customer = self.context.get("request").user
                if customer.email  and customer.email != email:
                    raise rest_framework.exceptions.ValidationError("Conflicting Email Addresses")
                customer.image = picture
                customer.email = email
                customer.save()
                lc , created = epilogue_models.LoginCustomer.objects.get_or_create(
                    email = email,
                    first_name = customer.first_name or first_name,
                    customer = customer,
                    password = ""
                )
                return lc
        return l


class RegistrationSerializer(BaseRegistrationSerializer):
    email = rest_framework.serializers.EmailField()
    password = rest_framework.serializers.CharField()

    def create(self , validated_data):
        return super().user_create(validated_data)

    def validate_email(self , email ):
        print("Calling Validate Email")
        l = epilogue_models.LoginCustomer.objects.filter(email = email)
        if l:
            raise authentication_exceptions.UserAlreadyExists("This Email is already Registered")
        return email

    def validate_password(self , password):
        validators = [
            password_validation.NumericPasswordValidator,
            password_validation.MinimumLengthValidator({"min_length" : 7}),
            password_validation.CommonPasswordValidator
        ]
        password_validation.validate_password(password , validators)
        return password

class GoogleLoginSerializer(BaseSocialSerializer):
    email = rest_framework.serializers.EmailField()
    name = rest_framework.serializers.CharField()
    picture = rest_framework.serializers.CharField()

    def release_attrs(self , credentials):
        return credentials['email'] , credentials['name'] ,"" , credentials['picture']

    def validate(self ,attrs):
        adapter = adapters.GoogleAdapter(
            access_token = attrs.get('access_token')
        )
        email = attrs['email']
        name = attrs['name']
        picture = attrs['picture']
        try:
            if not self.context['request'].user.is_anonymous and self.context['request'].user.email  :
                assert email == self.context['request'].user.email , rest_framework.exceptions.ValidationError("Conflicting Email Addresses")
        except Exception as e:
            raise rest_framework.exceptions.ValidationError(e)
        else:
            return attrs


class FacebookLoginSerializer(BaseSocialSerializer):
    access_token = rest_framework.serializers.CharField()

    def release_attrs(self , credentials):
        return credentials['email'] , credentials['first_name'] , credentials['last_name'] , credentials['picture']['data']['url']

    def validate(self , attrs):
        adapter = adapters.FacebookAdapter(
            access_token = attrs['access_token']
        )
        try:
            credentials = adapter.complete_login()
        except Exception as e:
            #Facebook returns an error
            raise rest_framework.exceptions.ValidationError(e)
        else:
            #Facebook Returns the credentials
            if not self.context['request'].user.is_anonymous and self.context['request'].user.email  :
                if not credentials['email'] == self.context['request'].user.email:
                    raise rest_framework.exceptions.ValidationError("Conflicting Email Addresses")
            return credentials

class BatraGoogleSerializer(BaseSocialSerializer):
    email = rest_framework.serializers.EmailField()
    name = rest_framework.serializers.CharField()
    picture = rest_framework.serializers.CharField()
    url = rest_framework.serializers.URLField(required = False , default = "")
    source = rest_framework.serializers.CharField(required = False)
    language = rest_framework.serializers.CharField(required = False , default = "en")

    def validate_language(self , lang):
        if lang not in ("en" , "hi"):
            raise rest_framework.exceptions.ValidationError("Not a valid language")
        return lang

    def release_attrs(self, credentials):
        return credentials['email'], credentials['name'] , '' , credentials['picture']

    def create(self,validated_data):
        created = super().create(validated_data)
        email = validated_data['email']
        language = validated_data['language']

        created.customer.first_name = validated_data['name']
        created.customer.save()
        signupsource = UserSignupSource.objects.create(
            customer = created.customer,
            source = validated_data['source'],
            campaign = "navratri",
            language = language
        )
        #if url:
        #   signals.navratri_signup.send(sender = epilogue_models.LoginCustomer , email = email , url = url , lang = language)
        return created

class DeviceRegistrationSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = models.Devices
        exclude = ["id"]

    def get_serializer(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
