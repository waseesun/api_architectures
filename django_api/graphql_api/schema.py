import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import User, Character, Location, Episode # Import new models
from .filters import UserFilter, CharacterFilter, LocationFilter, EpisodeFilter

# --- DjangoObjectTypes for our models ---

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "email")
        interfaces = (relay.Node,)

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = ("id", "name", "type", "dimension", "created")
        interfaces = (relay.Node,)
class EpisodeType(DjangoObjectType):
    class Meta:
        model = Episode
        fields = "__all__" # Expose all fields from the Episode model
        interfaces = (relay.Node,)

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character
        fields = "__all__" # Expose all fields from the Character model
        interfaces = (relay.Node,)

# --- Query Class (for reading data) ---

class Query(graphene.ObjectType):
    # User Queries (already existing)
    # all_users = graphene.List(UserType)
    all_users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    get_user = graphene.Field(UserType, id=graphene.ID())

    # Character Queries
    all_characters = DjangoFilterConnectionField(CharacterType, filterset_class=CharacterFilter)
    character = graphene.Field(CharacterType, id=graphene.ID())

    # Location Queries
    all_locations = DjangoFilterConnectionField(LocationType, filterset_class=LocationFilter)
    location = graphene.Field(LocationType, id=graphene.ID())

    # Episode Queries
    all_episodes = DjangoFilterConnectionField(EpisodeType, filterset_class=EpisodeFilter)
    episode = graphene.Field(EpisodeType, id=graphene.ID())

    # --- Resolver Methods ---

    def resolve_all_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_get_user(root, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def resolve_all_characters(root, info, **kwargs):
        return Character.objects.all()

    def resolve_character(root, info, id):
        try:
            return Character.objects.get(id=id)
        except Character.DoesNotExist:
            return None

    def resolve_all_locations(root, info, **kwargs):
        return Location.objects.all()

    def resolve_location(root, info, id):
        try:
            return Location.objects.get(id=id)
        except Location.DoesNotExist:
            return None

    def resolve_all_episodes(root, info, **kwargs):
        return Episode.objects.all()

    def resolve_episode(root, info, id):
        try:
            return Episode.objects.get(id=id)
        except Episode.DoesNotExist:
            return None

# # --- Mutation Classes (for changing data) ---

# # 5.1 Create Character Mutation
# class CreateCharacter(graphene.Mutation):
#     # This class defines the arguments (input) that the mutation accepts
#     class Arguments:
#         name = graphene.String(required=True)
#         species = graphene.String(required=True)
#         status = graphene.String() # Not required
#         type = graphene.String()   # Not required, matches model's 'type' field
#         gender = graphene.String() # Not required
#         imageUrl = graphene.String() # Matches Django's image_url field

#         # For ForeignKey relationships, we typically pass the ID of the related object
#         # Make them optional (nullable) by default if not specified as required=True
#         origin_id = graphene.ID()
#         location_id = graphene.ID()

#         # For ManyToMany relationships, we pass a list of IDs
#         episode_ids = graphene.List(graphene.ID)

#     # This defines the data that the mutation will return (the payload)
#     character = graphene.Field(CharacterType)

#     # The actual logic to perform the mutation
#     @staticmethod
#     def mutate(root, info, name, species, status=None, type=None, gender=None, imageUrl=None,
#                origin_id=None, location_id=None, episode_ids=None):
        
#         # Fetch related Location objects if IDs are provided
#         origin_instance = None
#         if origin_id:
#             try:
#                 origin_instance = Location.objects.get(id=origin_id)
#             except Location.DoesNotExist:
#                 raise Exception(f"Origin Location with ID {origin_id} not found.")

#         location_instance = None
#         if location_id:
#             try:
#                 location_instance = Location.objects.get(id=location_id)
#             except Location.DoesNotExist:
#                 raise Exception(f"Location with ID {location_id} not found.")

#         # Create the character instance
#         character = Character.objects.create(
#             name=name,
#             species=species,
#             status=status,
#             type=type,
#             gender=gender,
#             image_url=imageUrl, # Django model field is snake_case
#             origin=origin_instance,
#             location=location_instance
#         )

#         # Handle ManyToMany relationship for episodes
#         if episode_ids:
#             episodes = Episode.objects.filter(id__in=episode_ids)
#             character.episodes.set(episodes) # .set() method handles adding multiple related objects

#         # Return the mutation instance with the created character
#         return CreateCharacter(character=character)


# # 5.2 Update Character Mutation
# class UpdateCharacter(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True) # ID of the character to update
#         name = graphene.String()
#         species = graphene.String()
#         status = graphene.String()
#         type = graphene.String()
#         gender = graphene.String()
#         imageUrl = graphene.String()

#         origin_id = graphene.ID()
#         location_id = graphene.ID()
#         episode_ids = graphene.List(graphene.ID) # Replace all existing episodes

#     character = graphene.Field(CharacterType)

#     @staticmethod
#     def mutate(root, info, id, **kwargs): # kwargs will contain all other arguments
#         try:
#             character = Character.objects.get(id=id)
#         except Character.DoesNotExist:
#             raise Exception(f"Character with ID {id} not found.")

#         # Update simple fields
#         for field, value in kwargs.items():
#             if field in ['name', 'species', 'status', 'type', 'gender']:
#                 setattr(character, field, value)
#             elif field == 'imageUrl': # Handle camelCase to snake_case conversion
#                 setattr(character, 'image_url', value)

#         # Update ForeignKey relationships
#         if 'origin_id' in kwargs:
#             origin_id = kwargs.get('origin_id')
#             if origin_id is not None:
#                 try:
#                     character.origin = Location.objects.get(id=origin_id)
#                 except Location.DoesNotExist:
#                     raise Exception(f"Origin Location with ID {origin_id} not found.")
#             else:
#                 character.origin = None # Allow setting to null

#         if 'location_id' in kwargs:
#             location_id = kwargs.get('location_id')
#             if location_id is not None:
#                 try:
#                     character.location = Location.objects.get(id=location_id)
#                 except Location.DoesNotExist:
#                     raise Exception(f"Location with ID {location_id} not found.")
#             else:
#                 character.location = None # Allow setting to null

#         character.save() # Save changes to simple fields and ForeignKeys

#         # Update ManyToMany relationship for episodes
#         if 'episode_ids' in kwargs:
#             episode_ids = kwargs.get('episode_ids')
#             if episode_ids is not None:
#                 episodes = Episode.objects.filter(id__in=episode_ids)
#                 character.episodes.set(episodes) # .set() replaces all existing related objects
#             else:
#                 character.episodes.clear() # Allow clearing all related episodes

#         return UpdateCharacter(character=character)


# # 5.3 Delete Character Mutation
# class DeleteCharacter(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)

#     # The payload for a delete operation often just indicates success or the ID of the deleted item
#     success = graphene.Boolean()
#     deleted_id = graphene.ID()

#     @staticmethod
#     def mutate(root, info, id):
#         try:
#             character = Character.objects.get(id=id)
#             character.delete()
#             return DeleteCharacter(success=True, deleted_id=id)
#         except Character.DoesNotExist:
#             return DeleteCharacter(success=False, deleted_id=id) # Indicate failure if not found


# # --- Main Mutation Class (combines all mutations) ---
# class Mutation(graphene.ObjectType):
#     create_character = CreateCharacter.Field() # automatic transformation from snake to camel case
#     update_character = UpdateCharacter.Field()
#     delete_character = DeleteCharacter.Field()

# # --- Define the Schema with both Query and Mutation ---
# schema = graphene.Schema(query=Query, mutation=Mutation)