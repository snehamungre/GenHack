import argparse
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
import os
from requests_aws4auth import AWS4Auth
import time
import re

# Retrieve arguments from command line
parser = argparse.ArgumentParser(description="Help", 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--opensearch-endpoint", help="opensearch endpoint url (Example: https://abc123.us-east-1.aoss.amazonaws.com", required=True)
parser.add_argument("--vector-index", help="vector index", required=True)

args = parser.parse_args()

service = 'aoss'
credentials = boto3.Session().get_credentials()
region = os.environ.get('AWS_REGION')
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

#Remove http or https prefixes with regex
opensearch_vector_endpoint = re.sub(r'^https?://', '', args.opensearch_endpoint)
opensearch_vector_port = 443
opensearch_vector_field="vector_field"
opensearch_vector_index = args.vector_index

opensearch_client = OpenSearch(
   hosts = [{'host': opensearch_vector_endpoint, 'port': opensearch_vector_port}],
   http_auth = awsauth,
   use_ssl = True,
   verify_certs = True,
   http_compress = True,
   connection_class = RequestsHttpConnection
)

index_body = {
  'settings': {
    "index.knn": True
  },
  "mappings": {
    "properties": {
      "vector_field": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "engine": "faiss",
          "name": "hnsw",
          "space_type": "l2"
        }
      }
    }
  }
}

# Create index if it doesn't exist
exists = opensearch_client.indices.exists(opensearch_vector_index)
if not exists:
    response = opensearch_client.indices.create(opensearch_vector_index, body=index_body)