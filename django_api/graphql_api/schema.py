import graphene
from graphene_django import DjangoObjectType
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "email")

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    get_user = graphene.Field(UserType, id=graphene.ID())

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_get_user(root, info, id):
        return User.objects.get(id=id)

schema = graphene.Schema(query=Query)