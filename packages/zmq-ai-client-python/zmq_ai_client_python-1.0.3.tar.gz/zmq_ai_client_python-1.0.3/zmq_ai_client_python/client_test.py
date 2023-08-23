import json
from dataclasses import asdict

from .client import LlamaClient
from .schema.completion import ChatCompletion
from .schema.request import Message, Request


def main():
    client = LlamaClient('tcp://localhost:5555')

    messages = [
        Message(role='user', content='What is the capital of france?'),
        Message(role='Assistant', content='The capital of France is Paris'),
        Message(role='user', content='Hello? How are you?')

    ]
    STOP = ["### Assistant:", "### Human:", "###Assistant:", "###Human:"]
    request = Request(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.8,
        n=256,
        stop=STOP,
        user="708bab67-64d2-4e7d-94b6-2b6e043d880n",
        key_values={"session": "6eef38d9-1c7f-4314-9d41-54271ef97f17"}
    )

    json_str = json.dumps(asdict(request), indent=4)
    print(json_str)

    response: ChatCompletion = client.send_request(request)

    json_str = json.dumps(asdict(response), indent=4)
    print(json_str)


if __name__ == "__main__":
    main()
