# seeders.py

import os
import django
import random

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings') # <--- IMPORTANT: Replace 'your_project_name'
django.setup()

from graphql_api.models import User, Location, Episode, Character # <--- IMPORTANT: Replace 'myapp' with your actual app name

print("--- Populating Django Database with Sample Data ---")

# --- 1. Create Sample Users ---
print("\n1. Creating Users...")
user1, created = User.objects.get_or_create(name="Admin User", email="admin@example.com")
if created:
    print(f"  Created user: {user1.name}")
else:
    print(f"  User already exists: {user1.name}")

user2, created = User.objects.get_or_create(name="Test User", email="test@example.com")
if created:
    print(f"  Created user: {user2.name}")
else:
    print(f"  User already exists: {user2.name}")

# --- 2. Create Sample Locations ---
print("\n2. Creating Locations...")
earth_c137, created = Location.objects.get_or_create(
    name="Earth (C-137)",
    type="Planet",
    dimension="Dimension C-137"
)
if created: print(f"  Created location: {earth_c137.name}")
else: print(f"  Location already exists: {earth_c137.name}")

citadel_of_ricks, created = Location.objects.get_or_create(
    name="Citadel of Ricks",
    type="Space station",
    dimension="Dimension C-137"
)
if created: print(f"  Created location: {citadel_of_ricks.name}")
else: print(f"  Location already exists: {citadel_of_ricks.name}")

unknown_location, created = Location.objects.get_or_create(
    name="Unknown",
    type="Unknown",
    dimension="Unknown"
)
if created: print(f"  Created location: {unknown_location.name}")
else: print(f"  Location already exists: {unknown_location.name}")

# --- 3. Create Sample Episodes ---
print("\n3. Creating Episodes...")
episode_data = [
    {"name": "Pilot", "air_date": "December 2, 2013", "episode_code": "S01E01"},
    {"name": "Lawnmower Dog", "air_date": "December 9, 2013", "episode_code": "S01E02"},
    {"name": "Anatomy Park", "air_date": "December 16, 2013", "episode_code": "S01E03"},
    {"name": "Mortynight Run", "air_date": "August 2, 2015", "episode_code": "S02E02"},
    {"name": "The Ricklantis Mixup", "air_date": "September 10, 2017", "episode_code": "S03E07"},
    {"name": "The Vat of Acid Episode", "air_date": "May 17, 2020", "episode_code": "S04E08"},
]

episodes = []
for data in episode_data:
    episode, created = Episode.objects.get_or_create(**data)
    if created:
        print(f"  Created episode: {episode.name}")
    else:
        print(f"  Episode already exists: {episode.name}")
    episodes.append(episode)

# --- 4. Create Sample Characters ---
print("\n4. Creating Characters...")

# Rick Sanchez
rick, created = Character.objects.get_or_create(
    name="Rick Sanchez",
    species="Human",
    status="Alive",
    gender="Male",
    image_url="https://rickandmortyapi.com/api/character/avatar/1.jpeg",
    origin=earth_c137,
    location=citadel_of_ricks
)
if created:
    print(f"  Created character: {rick.name}")
    rick.episodes.set([episodes[0], episodes[1], episodes[2], episodes[4], episodes[5]]) # Assign some episodes
else:
    print(f"  Character already exists: {rick.name}")

# Morty Smith
morty, created = Character.objects.get_or_create(
    name="Morty Smith",
    species="Human",
    status="Alive",
    gender="Male",
    image_url="https://rickandmortyapi.com/api/character/avatar/2.jpeg",
    origin=earth_c137,
    location=earth_c137
)
if created:
    print(f"  Created character: {morty.name}")
    morty.episodes.set([episodes[0], episodes[1], episodes[2], episodes[3], episodes[5]])
else:
    print(f"  Character already exists: {morty.name}")


# Summer Smith
summer, created = Character.objects.get_or_create(
    name="Summer Smith",
    species="Human",
    status="Alive",
    gender="Female",
    image_url="https://rickandmortyapi.com/api/character/avatar/3.jpeg",
    origin=earth_c137,
    location=earth_c137
)
if created:
    print(f"  Created character: {summer.name}")
    summer.episodes.set([episodes[0], episodes[1], episodes[2], episodes[4]])
else:
    print(f"  Character already exists: {summer.name}")

# Birdperson (from another dimension)
birdperson, created = Character.objects.get_or_create(
    name="Birdperson",
    species="Birdperson",
    status="Alive", # Or Dead, depending on when you populate!
    gender="Male",
    image_url="https://rickandmortyapi.com/api/character/avatar/8.jpeg",
    origin=unknown_location, # Example of different origin
    location=unknown_location
)
if created:
    print(f"  Created character: {birdperson.name}")
    birdperson.episodes.set([episodes[3], episodes[4]])
else:
    print(f"  Character already exists: {birdperson.name}")


# Example for a character with unknown origin/location
squanchy, created = Character.objects.get_or_create(
    name="Squanchy",
    species="Alien",
    status="Alive",
    gender="Male",
    image_url="https://rickandmortyapi.com/api/character/avatar/12.jpeg",
    origin=None, # Example of null origin
    location=None # Example of null location
)
if created:
    print(f"  Created character: {squanchy.name}")
    squanchy.episodes.set([episodes[3], episodes[5]])
else:
    print(f"  Character already exists: {squanchy.name}")


print("\n--- Database Population Complete! ---")