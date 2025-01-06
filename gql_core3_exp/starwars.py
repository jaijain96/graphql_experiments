from enum import Enum

from graphql import (
    GraphQLArgument,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    graphql_sync,
)
from starwars_resolvers import *

"""
enum Episode { NEWHOPE, EMPIRE, JEDI }

interface Character {
  id: String!
  name: String
  friends: [Character]
  appearsIn: [Episode]
}

type Human implements Character {
  id: String!
  name: String
  friends: [Character]
  appearsIn: [Episode]
  homePlanet: String
}

type Droid implements Character {
  id: String!
  name: String
  friends: [Character]
  appearsIn: [Episode]
  primaryFunction: String
}

type Query {
  hero(episode: Episode): Character
  human(id: String!): Human
  droid(id: String!): Droid
}
"""

# one way to define the Episode enum type, using gql enum type
episode_enum = GraphQLEnumType(
    "Episode",
    {
        "NEWHOPE": GraphQLEnumValue(4, description="Released in 1977."),
        "EMPIRE": GraphQLEnumValue(5, description="Released in 1980."),
        "JEDI": GraphQLEnumValue(6, description="Released in 1983."),
    },
    description="One of the films in the Star Wars Trilogy",
)


# another way to define the Episode enum type, but we make it more pythonic using a python class that inherits from
# builtin python enum.Enum class
class EpisodeEnum(Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


episode_enum = GraphQLEnumType("Episode", EpisodeEnum, description="One of the films in the Star Wars Trilogy")

# we can also use the a simple python dictionary here
episode_enum = GraphQLEnumType(
    "Episode",
    {"NEWHOPE": 4, "EMPIRE": 5, "JEDI": 6},
    description="One of the films in the Star Wars Trilogy",
)


# we define the Character interface like so
character_interface = GraphQLInterfaceType(
    "Character",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLString), description="The id of the character."),
        "name": GraphQLField(GraphQLString, description="The name of the character."),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the character," " or an empty list if they have none.",
        ),
        "appearsIn": GraphQLField(GraphQLList(episode_enum), description="Which movies they appear in."),
        "secretBackstory": GraphQLField(GraphQLString, description="All secrets about their past."),
    },
    resolve_type=get_character_type,
    description="A character in the Star Wars Trilogy",
)
"""
We did not pass the dictionary of fields to the GraphQLInterfaceType directly, but by using a lambda function (a so-called “thunk”). This is necessary because the fields are referring back to the character interface that we are just defining. Whenever we have such recursive definitions in GraphQL-core, we need to use thunks. Otherwise, we can pass everything directly.
"""

# we define a Human and a Droid type, which both implement the Character interface
human_type = GraphQLObjectType(
    "Human",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLString), description="The id of the human."),
        "name": GraphQLField(GraphQLString, description="The name of the human."),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the human," " or an empty list if they have none.",
            resolve=get_friends,
        ),
        "appearsIn": GraphQLField(GraphQLList(episode_enum), description="Which movies they appear in."),
        "homePlanet": GraphQLField(
            GraphQLString,
            description="The home planet of the human, or null if unknown.",
        ),
        "secretBackstory": GraphQLField(
            GraphQLString,
            resolve=get_secret_backstory,
            description="Where are they from" " and how they came to be who they are.",
        ),
    },
    interfaces=[character_interface],
    description="A humanoid creature in the Star Wars universe.",
)

droid_type = GraphQLObjectType(
    "Droid",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLString), description="The id of the droid."),
        "name": GraphQLField(GraphQLString, description="The name of the droid."),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the droid," " or an empty list if they have none.",
            resolve=get_friends,
        ),
        "appearsIn": GraphQLField(GraphQLList(episode_enum), description="Which movies they appear in."),
        "secretBackstory": GraphQLField(
            GraphQLString,
            resolve=get_secret_backstory,
            description="Construction date and the name of the designer.",
        ),
        "primaryFunction": GraphQLField(GraphQLString, description="The primary function of the droid."),
    },
    interfaces=[character_interface],
    description="A mechanical creature in the Star Wars universe.",
)

# we can define the root Query type for our schema now:
query_type = GraphQLObjectType(
    "Query",
    lambda: {
        "hero": GraphQLField(
            character_interface,
            args={
                "episode": GraphQLArgument(
                    episode_enum,
                    description=(
                        "If omitted, returns the hero of the whole saga."
                        " If provided, returns the hero of that particular episode."
                    ),
                )
            },
            resolve=get_hero,
        ),
        "human": GraphQLField(
            human_type,
            args={"id": GraphQLArgument(GraphQLNonNull(GraphQLString), description="id of the human")},
            resolve=get_human,
        ),
        "droid": GraphQLField(
            droid_type,
            args={"id": GraphQLArgument(GraphQLNonNull(GraphQLString), description="id of the droid")},
            resolve=get_droid,
        ),
    },
)

schema = GraphQLSchema(query_type)
# schema = GraphQLSchema(
#     query=GraphQLObjectType(
#         name="RootQueryType",
#         fields={
#             "hello": GraphQLField(GraphQLString, resolve=lambda obj, info: "world")
#         },
#     )
# )

query = """
{
    human (id : "1002") {
        name
    }
}
"""

print(graphql_sync(schema, query))
