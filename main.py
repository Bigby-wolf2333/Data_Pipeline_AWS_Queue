import boto3
from datetime import date
import hashlib
import json
import pandas as pd

from sqlalchemy import create_engine
import traceback

# The URL of the SQS queue
queue_url = "http://localstack:4566/000000000000/login-queue"

sqs = boto3.client(
    "sqs",
    endpoint_url="http://localstack:4566",
    region_name="us-east-1",
    aws_access_key_id="fakeAccessKeyId",  # Fake credentials for local usage
    aws_secret_access_key="fakeSecretAccessKey",
)

# store processed message
processed_msg_list = []


def handle_messages():
    try:
        # Receive messages from the SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=10
        )

        # Check if 'Messages' is in the response
        if "Messages" in response:
            for message in response["Messages"]:
                body = json.loads(message["Body"])

                # process message
                processed_msg = process_message(body)
                processed_msg_list.append(processed_msg)

                # OPTIONAL - FOR FUN!
                # Delete the message from the queue after processing

                # receipt_handle = message['ReceiptHandle']
                # sqs.delete_message(
                #     QueueUrl=queue_url,
                #     ReceiptHandle=receipt_handle
                # )
                # print('Message deleted successfully')
        else:
            print("No messages available")

    except Exception as e:
        print("Error receiving message:", e)
        traceback.print_exc()


def process_message(msg: dict):

    masked_device_id = mask_string(msg["device_id"])
    masked_ip = mask_string((msg["ip"]))

    msg["masked_device_id"] = masked_device_id
    msg["masked_ip"] = masked_ip
    msg["create_date"] = str(date.today())
    del msg["device_id"]
    del msg["ip"]

    return msg


def mask_string(msg):
    """
    Returns a SHA-256 hash of the input string. This hash can be used to identify duplicates
    without revealing the original string.
    """
    # Create a new SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    sha256_hash.update(msg.encode("utf-8"))

    # Get the hexadecimal representation of the hash
    hash_hex = sha256_hash.hexdigest()

    return hash_hex


def load_to_postgres(data: pd.DataFrame):
    # ideally we would read these param from a parameter store

    engine = create_engine("postgresql://postgres:postgres@postgres:5432/postgres")

    # Load DataFrame into PostgreSQL
    data.to_sql("user_logins", engine, if_exists="replace", index=False)


if __name__ == "__main__":

    # Call the function to read messages
    handle_messages()

    # Convert data to pandas dataframe and load to postgres
    df = pd.DataFrame(processed_msg_list)
    load_to_postgres(df)
