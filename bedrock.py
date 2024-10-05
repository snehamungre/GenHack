# Use the Converse API to send a text message to Llama 2 Chat 13B.
import boto3
from botocore.exceptions import ClientError
import json
# from dotenv import load_dotenv

# load_dotenv(".env")

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID, e.g., Titan Text Premier.
model_id = "us.meta.llama3-2-1b-instruct-v1:0"

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id="ASIAWAG62HN2PXFDK6CX",
    aws_secret_access_key="5YrjtmDCn2qNfFb5vR9nNgOgiEuDnW/J/SXTeTVr",
    aws_session_token="IQoJb3JpZ2luX2VjEKn//////////wEaCXVzLWVhc3QtMSJHMEUCIQDySMixwG5jqQSFWJ9gdGl3OGZEWmF251Jq1BZHwWCHBQIgWctKLB+VYn1tuUyuA5y20jeeD1QQvygDjENVmkPvRNQqogII8f//////////ARABGgw0MTI3ODQxNDczMTYiDKBgZCSSl+V5/8cp1yr2ARJa/iPVRO65zP4FMI7IeajZuLgGzGHVsEKhuns97KQkAOEkq+JwX/Hd07TcZOGOMjydAV2Xy0riGYnHsjetEX4oRPais60Cy3UJ90DvhbZd196E0j5apLgrqgA4U86g/VGj405ckybnH/+KNArgIt2aPkf9Tm7QzEwLxXoYuOEddkT2TUwPgG+M2AipU9TpTGxASl+PrHglccdXJLtrjAFUBqX0mLPF81UE4fwAwgPvNcqbQTRfMQ+j0+uFH3Wb7yochNm3XnDRf5NJBtonoFfpe0CvABIbFFWgqLQUQAZUodE/vabCqg5e4Cth0hwLbPlBEK6CQTDzyoW4BjqdAWHYVUX++wedIRBZk7AM/3SC4vA9r+bpOBZ306F7VPV5cGb+05GwpdTZIT5srXQWcFIx/A80opCA+6swfpFQ5sMEGtLVgnOVoe4TXzBmhWxPvJ+u9sqefIbUIy3l9vqnHXtupz+r9yvL8fgOydWRTNx0a7ZjkVDRlL22NYw20IPT0iRvHcl0JZhgjp/f4isQatsMJmEO/HVO6wG4DkI="
)

def invoke(prompt, temperature, max_tokens):
    prompt_config = {
        "prompt": f'\n\nHuman: {prompt} \n\nAssistant:',
        "max_tokens_to_sample": max_tokens,
        "temperature": temperature
    }

    response = bedrock_runtime.invoke_model(
        body=json.dumps(prompt_config),
        modelId="us.meta.llama3-2-1b-instruct-v1:0"
    )

    response_body = json.loads(response.get("body").read())

    return response_body.get("completion")