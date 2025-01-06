"""_summary_
"""

from pprint import pp

from graphql import (
    GraphQLArgument,
    GraphQLField,
    GraphQLInt,
    GraphQLObjectType,
    GraphQLOutputType,
    GraphQLSchema,
    GraphQLString,
    get_introspection_query,
    graphql_sync,
)

# schema = GraphQLSchema(
#     query=GraphQLObjectType(
#         name="some",
#         fields={"hello": GraphQLField(GraphQLString, resolve=lambda obj, info: "world")},
#     )
# )

# query = "{ hello }"
# # query = """
# # {
# #     __typename {
# #         __schema {
# #             __type
# #         }
# #     }
# # }
# # """

# print(graphql_sync(schema, query))


TYPE_SYSTEM = """
type system we are implementing

type Query{
    transport_vehicle (number_of_tyres: Int!): Vehicle
}

type Vehicle{
    vehicle_type: String
    owner: String
}
"""


def owner_resolver(number_of_tyres, *args, **kwargs):
    """_summary_

    Returns:
        _type_: _description_
    """
    print("inside owner_resolver")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    if number_of_tyres == 0:
        return "bhola"
    if number_of_tyres == 1:
        return "golu"
    if number_of_tyres == 2:
        return "tillu"
    if number_of_tyres == 3:
        return "nonu"
    if number_of_tyres == 4:
        return "kaka"


def vehicle_kind_resolver(number_of_tyres, *args, **kwargs):
    """_summary_

    Returns:
        _type_: _description_
    """
    print("inside vehicle_type_resolver")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    if number_of_tyres == 0:
        # return 1 / 0
        return "on foot"
    if number_of_tyres == 1:
        return "unicycle"
    if number_of_tyres == 2:
        return "scooter"
    if number_of_tyres == 3:
        return "tuk-tuk"
    if number_of_tyres == 4:
        return "car"


def vehicle_resolver(*args, number_of_tyres, **kwargs):
    """_summary_

    Returns:
        _type_: _description_
    """
    print("inside vehicle_resolver")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    # the return value of a resolver for an ObjectType is not "returned" in the traditional
    # sense, instead, it gets passed onto the resolvers of each field of the ObjectType so
    # it can be used for context or other decision making
    # the final values of the output json we are returning are assembled at the leaves
    # of the every ObjectType, where fields are ScalarTypes and resolver finally map to
    # concrete data values
    return number_of_tyres


vehicle_type = GraphQLObjectType(
    name="Vehicle",
    fields={
        "vehicle_kind": GraphQLField(GraphQLString, resolve=vehicle_kind_resolver),
        "owner": GraphQLField(GraphQLString, resolve=owner_resolver),
    },
)

# root_type = GraphQLObjectType(name="root", fields={"transport": GraphQLField(vehicle_type, resolve=lambda *x: x)})
# root_type = GraphQLObjectType(name="root", fields={"transport": vehicle_type})
root_type = GraphQLObjectType(
    name="root",
    fields={
        "transport_vehicle": GraphQLField(
            vehicle_type, args={"number_of_tyres": GraphQLArgument(GraphQLInt)}, resolve=vehicle_resolver
        )
    },
)

schema = GraphQLSchema(query=root_type)

CLIENT_QUERY = """
{
    # __typename
    transport_vehicle (number_of_tyres: 0) {
        __typename
        vehicle_kind
        owner
    }
}
"""

# print(graphql_sync(schema, CLIENT_QUERY))

introspection_query = get_introspection_query(descriptions=False)
exec_res = graphql_sync(schema, introspection_query)
# print(exec_res)
pp(exec_res.data)
