from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import pycountry
from operator import itemgetter

#these are model abstracts from django extensions
from django_extensions.db.models import (
    TimeStampedModel,
	ActivatorModel 
)

country_list = sorted(
        [(country.name, country.name) 
        for country in list(pycountry.countries)], key=itemgetter(0))

country_list.insert(0, ("*Select Country", "*Select Country"))

#(('United Kingdom', 'United Kingdom'), ('France', 'France').....)
COUNTRIES = country_list

class UserProfile(TimeStampedModel,ActivatorModel,models.Model):
    '''
    users.UserProfile
    Stores a single user profile entry related to :model:`auth.User`
    '''
    class Meta:
        verbose_name_plural = 'User profiles'
        ordering = ["id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(verbose_name="Contact telephone number", max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True)
    county = models.CharField(verbose_name="County",max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Zip/Post Code",max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True, choices=COUNTRIES)

    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)

    avatar = models.ImageField(default='default_avatar.jpg', upload_to='avatar', null=True, blank=True) # this is our new avatar filed

    @property
    def country_alpha_2(self):
        '''
        Used to return the selected countries alpha 2 repr i.e. England == GB
        '''
        if self.country:
            return pycountry.countries.get(name = self.country).alpha_2
        else:
            return None

    def full_name(self):
        '''
        Return full name or email
        '''
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}'
        if self.user.email:
            return self.user.email
        return self.user.email

    def __str__(self):
        return self.full_name()