# your_app_name/schema.py

import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Location, Episode, Character

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__" # Expose all fields

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = "__all__"

class EpisodeType(DjangoObjectType):
    class Meta:
        model = Episode
        fields = "__all__"

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character
        fields = "__all__"