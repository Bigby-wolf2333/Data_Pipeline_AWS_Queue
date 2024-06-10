# Implementation Thoughts

## Introduction
This README provides an overview of the implementation considerations and decisions for a message processing application.

### How will you read messages from the queue?
To read messages from the queue, the application utilizes the boto3 SQS client to establish a connection to the SQS queue. Messages are retrieved one by one, and the response body from each message is extracted.

### What type of data structures should be used?
For this project, Python is chosen as the primary language. With the example dataset, JSON and list data structures are sufficient for processing. Additionally, when loading data into PostgreSQL, a table-like data structure similar to a Pandas DataFrame is used.

### How will you mask the PII data so that duplicate values can be identified?
PII data is masked using the SHA256 hashing algorithm from the hashlib library. This ensures that duplicate values can still be identified without exposing sensitive information.

### What will be your strategy for connecting and writing to PostgreSQL?
The strategy involves initially processing data using a table-like data structure, such as a Pandas DataFrame, and then loading it into PostgreSQL. This is achieved using SQLAlchemy library for database connectivity and operations.

### Where and how will your application run?
The application is designed to run on any local machine. Refer to the "Steps to Run" section for instructions on running the application locally.

### How would you deploy this application in production?
Deployment strategies depend on the desired processing approach. For continuous processing, the application can be packaged into a Docker image and deployed on a Kubernetes cluster. For batch processing, a scheduling tool like Apache Airflow can trigger the application at set intervals, also deployed on a Kubernetes cluster.

### What other components would you want to add to make this production-ready?
Additional components for production readiness include:
- Data audit/validation component to identify and handle data errors before they propagate downstream.
- Monitoring component to track task performance metrics and system health.

### How can this application scale with a growing dataset?
The application can scale by deploying multiple consumers of the message queue to process messages concurrently, thus accommodating a growing dataset.

### How can PII be recovered later on?
While hashing PII data makes it non-recoverable, maintaining a mapping of original data to hashed data can facilitate recovery if needed. However, this mapping is not implemented in the current solution.

### Assumptions
1. The application is designed as a batch processing system.
2. All data provided is expected to be valid JSON format, despite potential data quality issues.
3. The data size is assumed to be reasonable and manageable on a local machine.

## Steps to Run
1. Clone this repository and navigate to the project folder.
2. Run `docker compose up`.
3. Install dependencies by running `pip install -r requirements.txt`.
4. Execute `python main.py` to start the application.

## Next Steps
To further enhance the application:
1. Allow the application to be deployed as individual consumers of the SQS queue for scalability.
2. Implement auditing and monitoring components for improved data integrity and system performance.
3. Set up CI/CD pipelines for automated testing, building Docker images, and deploying to production environments.
4. It is okay to replace duplicate data on the Postgres table
5. Assume the project set up is done
