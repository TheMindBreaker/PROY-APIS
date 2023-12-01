import graphene
from graphene_django import DjangoObjectType
from .models import CustomUser
import graphql_jwt
from graphql_jwt.shortcuts import get_token
import predict.schema as second_schema


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        # Asegúrate de manejar aquí las autorizaciones si es necesario
        return CustomUser.objects.all()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()

        token = get_token(user)
        
        return CreateUser(user=user, token=token)

class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# Aquí es donde integras la clase AuthMutation con la clase Mutation
class Mutation(second_schema.Mutation, AuthMutation, graphene.ObjectType):
    create_user = CreateUser.Field()
    # Aquí puedes añadir otras mutaciones si las necesitas

schema = graphene.Schema(query=Query, mutation=Mutation)
