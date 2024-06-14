import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from app.managers import CustomUserManager
# Create your models here.

class Attribute(models.Model):
    attribute_name = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=255)


    def __str__(self):
        return self.attribute_value


class Product(models.Model):
    class RatingChoice(models.IntegerChoices):
        Zero = 0
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(null = True, blank = True)
    rating = models.IntegerField(choices=RatingChoice,default=RatingChoice.Zero.value)
    amount = models.IntegerField(default=1)
    discount = models.IntegerField()
    attribute = models.ManyToManyField('app.Attribute',related_name = 'attributes')
    attribute_value = models.ManyToManyField('app.AttributeValue',)




    @property
    def discount_price(self):
        if self.discount > 0:
            return self.price*(1-self.discount/100)
        return self.price


    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey('app.Product',on_delete=models.CASCADE,related_name='images')


    def __str__(self):
        return self.product.name



class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    adress = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField(null = True,unique=True,default=None)


    def __str__(self):
        return self.name


    # def get_absolute_url(self):
        # return reverse('customer_details',kwargs={'slug': self.slug})





class User(AbstractBaseUser,PermissionsMixin):
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13,validators=[RegexValidator(r'^+\d\d\d\d\d-\d\d\d-\d\d\-\d\d\$')],
                                    verbose_name=('phone number'),
                                    help_text=('format: +99890-123-45-67'),
                                    unique=True,
                                    blank=False,
                                    null=False)

    first_name = models.CharField(max_length=255,null=True,blank=True)
    laser_name = models.CharField(max_length=255,null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True),
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []



