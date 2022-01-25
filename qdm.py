import os
import click
import requests
import dotenv
import hashlib
import json

from endpoints import MastodonEndpoints


def validate_media(path):
    errors = []
    if not os.path.exists(path):
        errors.append("File does not exist")
    return errors


def validate_toot(content):
    if len(content) > 500:
        return ["Toot too long"]
    return []


def get_headers(content=None):
    headers = {
        'Authorization': f"Bearer {os.environ['API_AUTHORIZATION_TOKEN']}"
    }
    if content is not None:
        idempotency_key = hashlib.sha3_512(bytes(content, 'utf-8')).hexdigest()
        headers['Idempotency-Key'] = idempotency_key
    return headers


# Returns Media ID or None if errors
def post_media_attachment(path):
    ep = MastodonEndpoints.get(MastodonEndpoints.POST_MEDIA)
    headers = get_headers()
    files = {'file': open(path, 'rb')}
    result = requests.post(ep, headers=headers, files=files)
    if result.ok:
        return json.loads(result.text)
    else:
        return None


def post_toot(content, file):
    ep = MastodonEndpoints.get(MastodonEndpoints.POST_TOOT)
    headers = get_headers(content=content)
    data = {
        'status': content
    }
    if file:
        media = post_media_attachment(file)
        if media:
            data['media_ids[]'] = [media['id']]
        else:
            print(f"Error: media could not be attached")
            return
    result = requests.post(ep, headers=headers, data=data)
    if result.ok:
        print("Success!")
    else:
        print(f"Error: {result.reason}")


@click.command()
@click.option("--content", prompt="Content", help="Content of the toot")
@click.option("--file", help="File attached to the toot")
def send(content, file):
    validation_results = validate_toot(content)
    if file:
        file = os.path.expanduser(file)
        validation_results.extend(validate_media(file))
    if len(validation_results) == 0:
        post_toot(content, file)
    else:
        print(f"Invalid Toot: {', '.join(validation_results)}")


if __name__ == "__main__":
    dotenv.load_dotenv()
    send()
