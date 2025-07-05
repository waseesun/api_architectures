import django_filters
from .models import User, Character, Location, Episode


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "name": ["exact", "icontains"],
            "email": ["exact", "icontains"],
        }
        
class CharacterFilter(django_filters.FilterSet):
    class Meta:
        model = Character
        fields = {
            "name": ["exact", "icontains"],
            "species": ["exact", "icontains"],
            "status": ["exact", "icontains"],
            "gender": ["exact", "icontains"],
        }
        
class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            "name": ["exact", "icontains"],
            "type": ["exact", "icontains"],
            "dimension": ["exact", "icontains"],
        }
        
class EpisodeFilter(django_filters.FilterSet):
    class Meta:
        model = Episode
        fields = {
            "name": ["exact", "icontains"],
            "episode": ["exact", "icontains"],
            "air_date": ["exact", "icontains"],
        }