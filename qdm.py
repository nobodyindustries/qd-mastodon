import os
import click
import requests
import dotenv
import hashlib

from endpoints import MastodonEndpoints


def validate_content(content):
    return len(content) <= 500


def get_headers(content=None):
    headers = {
        'Authorization': f"Bearer {os.environ['API_AUTHORIZATION_TOKEN']}"
    }
    if content is not None:
        idempotency_key = hashlib.sha3_512(bytes(content, 'utf-8')).hexdigest()
        headers['Idempotency-Key'] = idempotency_key
    return headers


def post_toot(content):
    ep = MastodonEndpoints.get(MastodonEndpoints.POST_TOOT)
    headers = get_headers(content=content)
    data = {
        'status': content
    }
    result = requests.post(ep, headers=headers, data=data)
    if result.status_code == 200:
        print("Success!")
    else:
        print(f"Error: {result.reason}")


@click.command()
@click.option("--content", prompt="Content", help="Content of the toot")
def send(content):
    if validate_content(content):
        post_toot(content)


if __name__ == "__main__":
    dotenv.load_dotenv()
    send()
