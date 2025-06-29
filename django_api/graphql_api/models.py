from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True, null=True)
    dimension = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Episode(models.Model):
    name = models.CharField(max_length=255)
    air_date = models.CharField(max_length=100, blank=True, null=True)
    episode_code = models.CharField(max_length=50, unique=True) # e.g., S01E01
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.episode_code}: {self.name}"

class Character(models.Model):
    STATUS_CHOICES = [
        ('Alive', 'Alive'),
        ('Dead', 'Dead'),
        ('unknown', 'unknown'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Genderless', 'Genderless'),
        ('unknown', 'unknown'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unknown')
    species = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='unknown')
    image_url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # Relationships
    # A character has an origin location
    origin = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='origin_characters',
        blank=True,
        null=True
    )
    # A character has a last known location
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='current_characters',
        blank=True,
        null=True
    )
    # A character can appear in many episodes, and an episode can have many characters
    episodes = models.ManyToManyField(Episode, related_name='characters')

    def __str__(self):
        return self.name