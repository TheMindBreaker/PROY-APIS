import graphene
from graphene_django import DjangoObjectType
from .models import User
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import create_refresh_token, get_token
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, token=token, refresh_token=refresh_token)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    # ... other mutations ...
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
