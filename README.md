# Implementation Thoughts

## Assumptions
1. The application is designed as a batch processing system.
2. All data provided is expected to be valid JSON format, despite potential data quality issues.
3. The data size is assumed to be reasonable and manageable on a local machine.
4. It is okay to replace duplicate data on the Postgres table
5. Assume the project set up is done

## Application Walk Through
This read message application consists of the following components:
1. Reading messages from the queue
2. Flattening JSON format data
3. Masking PII data
4. Collecting data and converting it into pd dataframe
5. Connecting to PostgreSQL and loading data into it

### Read messages from the queue
To read messages from the queue, the application utilizes the boto3 SQS client to establish a connection to the SQS queue. Messages are retrieved one by one, and the response body from each message is extracted.
```python
sqs = boto3.client(
    "sqs",
    endpoint_url="http://localstack:4566",
    region_name="us-east-1",
    aws_access_key_id="fakeAccessKeyId",
    aws_secret_access_key="fakeSecretAccessKey",
)
response = sqs.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=10
        )
```

### Data structures are used
For this project, Python is chosen as the primary language. With the example dataset, JSON and list data structures are sufficient for processing. Additionally, when loading data into PostgreSQL, a table-like data structure similar to a Pandas DataFrame is used.
```python
for message in response["Messages"]:
                body = json.loads(message["Body"])

                # process message
                processed_msg = process_message(body)
                
def process_message(msg: dict):

    masked_device_id = mask_string(msg["device_id"])
    masked_ip = mask_string((msg["ip"]))

    msg["masked_device_id"] = masked_device_id
    msg["masked_ip"] = masked_ip
    msg["create_date"] = str(date.today())
    del msg["device_id"]
    del msg["ip"]

    return msg
```

### Masked the PII data so that duplicate values can be identified
PII data is masked using the SHA256 hashing algorithm from the hashlib library. This ensures that duplicate values can still be identified without exposing sensitive information.
```python
def mask_string(msg):
    
    sha256_hash = hashlib.sha256()
    sha256_hash.update(msg.encode("utf-8"))
    hash_hex = sha256_hash.hexdigest()
    return hash_hex
```

### Connected and wrote to PostgreSQL?
The strategy involves initially processing data using a table-like data structure, such as a Pandas DataFrame, and then loading it into PostgreSQL. This is achieved using SQLAlchemy library for database connectivity and operations.
```python 
def load_to_postgres(data: pd.DataFrame):

    engine = create_engine("postgresql://postgres:postgres@postgres:5432/postgres")
    data.to_sql("user_logins", engine, if_exists="replace", index=False)
```

