
import io
import random
import string
import boto3
import time
import pandas as pd
import psycopg2

class df_to_rs:
    def __init__(self, region_name, s3_bucket, aws_access_key_id, aws_secret_access_key, redshift_c):
        """
        region_name: AWS region name, e.g., 'ap-south-1'.
        s3_bucket: Name of the S3 bucket to upload CSV files.
        aws_access_key_id: AWS access key ID.
        aws_secret_access_key: AWS secret access key.
        redshift_c: psycopg2 connection object to Redshift, e.g.,
        redshift_c = psycopg2.connect(dbname='more', host="hostname.ap-south-1.redshift.amazonaws.com", port=1433, user='ankit.goel', password='xxxx')
        redshift_c.set_session(autocommit=True)
        """
        self.region_name = region_name
        self.s3_bucket = s3_bucket
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.redshift_c = redshift_c

    def upload_to_redshift(self, df, dest):
        """
        Uploads the given DataFrame to the specified destination in Redshift.
        df: pandas DataFrame to be uploaded.
        dest: Redshift destination table, including schema, e.g., 'analytics.ship_pen'.
        """
        start_time = time.time()
        print("Generating randomized CSV filename...")
        csv_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.csv'
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        start_time = time.time()
        print("Converting DataFrame to CSV in-memory...")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        start_time = time.time()
        print(f"Uploading CSV to S3 bucket '{self.s3_bucket}'...")
        s3 = boto3.resource('s3', region_name=self.region_name, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        s3.Object(self.s3_bucket, csv_filename).put(Body=csv_buffer.getvalue())
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        start_time = time.time()
        print("Preparing Redshift COPY command...")
        columns = ','.join(df.columns)
        copy_query = f"""
        COPY {dest} ({columns})
        FROM 's3://{self.s3_bucket}/{csv_filename}'
        ACCESS_KEY_ID '{self.aws_access_key_id}'
        SECRET_ACCESS_KEY '{self.aws_secret_access_key}'
        DELIMITER ','
        IGNOREHEADER 1
        REGION '{self.region_name}';
        """
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        start_time = time.time()
        print("Executing Redshift COPY command...")
        self.redshift_c.cursor().execute(copy_query)
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        start_time = time.time()
        print(f"Deleting CSV file '{csv_filename}' from S3...")
        s3.Object(self.s3_bucket, csv_filename).delete()
        print(f"Time taken: {int(time.time() - start_time)} seconds")

        print("Upload to Redshift completed successfully.")