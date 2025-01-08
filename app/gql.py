from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def gql_query(gql_endpoint, gql_string: str, gql_variables: str=None, operation_name: str=None):
  json_data = None
  try:
    gql_transport = RequestsHTTPTransport(url=gql_endpoint)
    gql_client = Client(transport=gql_transport,
                        fetch_schema_from_transport=True)
    json_data = gql_client.execute(gql(gql_string), variable_values=gql_variables, operation_name=operation_name)
  except Exception as e:
    print("GQL query error:", e)
  return json_data