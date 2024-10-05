import boto3
from botocore.exceptions import ClientError
import json
import os
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv(".env")

# Create a Bedrock Runtime client in the AWS Region you want to use.
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id="ASIAWAG62HN2PXFDK6CX",
    aws_secret_access_key="5YrjtmDCn2qNfFb5vR9nNgOgiEuDnW/J/SXTeTVr",
    aws_session_token="IQoJb3JpZ2luX2VjEKn//////////wEaCXVzLWVhc3QtMSJHMEUCIQDySMixwG5jqQSFWJ9gdGl3OGZEWmF251Jq1BZHwWCHBQIgWctKLB+VYn1tuUyuA5y20jeeD1QQvygDjENVmkPvRNQqogII8f//////////ARABGgw0MTI3ODQxNDczMTYiDKBgZCSSl+V5/8cp1yr2ARJa/iPVRO65zP4FMI7IeajZuLgGzGHVsEKhuns97KQkAOEkq+JwX/Hd07TcZOGOMjydAV2Xy0riGYnHsjetEX4oRPais60Cy3UJ90DvhbZd196E0j5apLgrqgA4U86g/VGj405ckybnH/+KNArgIt2aPkf9Tm7QzEwLxXoYuOEddkT2TUwPgG+M2AipU9TpTGxASl+PrHglccdXJLtrjAFUBqX0mLPF81UE4fwAwgPvNcqbQTRfMQ+j0+uFH3Wb7yochNm3XnDRf5NJBtonoFfpe0CvABIbFFWgqLQUQAZUodE/vabCqg5e4Cth0hwLbPlBEK6CQTDzyoW4BjqdAWHYVUX++wedIRBZk7AM/3SC4vA9r+bpOBZ306F7VPV5cGb+05GwpdTZIT5srXQWcFIx/A80opCA+6swfpFQ5sMEGtLVgnOVoe4TXzBmhWxPvJ+u9sqefIbUIy3l9vqnHXtupz+r9yvL8fgOydWRTNx0a7ZjkVDRlL22NYw20IPT0iRvHcl0JZhgjp/f4isQatsMJmEO/HVO6wG4DkI="
)

def invoke(prompt, temperature=0.6, max_tokens=2000):
    payload = {
        "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"How can I upcycle a {prompt}?"
                        }
                    ]
                }
            ]
        }
    }

    try:
        # Send the request to the model
        response = bedrock_runtime.invoke_model(
            body=json.dumps(payload["body"]),
            modelId=payload["modelId"],
            contentType=payload["contentType"],
            accept=payload["accept"]
        )
        
        # Print the entire response for debugging
        print("Raw response:", response)

        # Parse and return the response
        response_body = json.loads(response.get("body").read())
        generation = response_body['content'][0]['text']
        print("Parsed response body:", generation)  # Debugging output

        return generation
        # Check the structure of the response body
        completion = response_body.get("completion")
        if completion:
            return completion
        else:
            return "No completion found in the response."

    except ClientError as e:
        return f"ClientError invoking model: {str(e)}"
    except Exception as e:
        return f"Error invoking model: {str(e)}"

# Example usage
# prompt = "cardboard box"  # Replace with your test prompt
# response = invoke(prompt)
# print("Model response:", response)
