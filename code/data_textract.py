
import time
import boto3


class text_extraction:

    def start_textract_job(self, bucket, document_key):
        textract_client = boto3.client('textract', region_name='ap-south-1')
        #s3_client = boto3.client('s3', region_name='ap-south-1')
        response = textract_client.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': document_key}}
        )

        return response['JobId']

    def get_textract_results(self, job_id):
        textract_client = boto3.client('textract', region_name='ap-south-1')
        waiter = textract_client.get_waiter('text-detection-complete')

        waiter.wait(JobId=job_id)

        response = textract_client.get_document_text_detection(JobId=job_id)

        return response

    def wait_for_completion(self, job_id):
        textract_client = boto3.client('textract', region_name='ap-south-1')

        while True:
            response = textract_client.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']

            if status in ['SUCCEEDED', 'FAILED']:
                break

            print(f'Job Status: {status}')
            time.sleep(5)  # Wait for 5 seconds before checking again

        print(f'Job {job_id} completed with status: {status}')
        return response

    def get_result(self):
        s3_bucket = 'dataeaze-intern-space'
        document_key = 'SUMIT/Databricks Spark Syllabus.pdf'

        job_id = text_extraction().start_textract_job(s3_bucket, document_key)

        print(f'Textract Job ID: {job_id}')

        # Retrieve the Textract results
        results = text_extraction().wait_for_completion(job_id)
        # Extract and print the text
        for item in results['Blocks']:
            if item['BlockType'] == 'LINE':
                print(item['Text'])


