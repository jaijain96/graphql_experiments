from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString
from graphql import graphql_sync

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name="RootQueryType",
        fields={
            "hello": GraphQLField(GraphQLString, resolve=lambda obj, info: "world")
        },
    )
)

query = '{ hello }'

print(graphql_sync(schema, query))
