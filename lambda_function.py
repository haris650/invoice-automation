import boto3
import datetime
import urllib.parse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Invoices')

def clean_filename(name):
    n = urllib.parse.unquote_plus(name)
    if n.lower().endswith('.pdf'):
        n = n[:-4]
    n = n.replace('+', '_').replace(' ', '_')
    import re
    n = re.sub(r'[^A-Za-z0-9_\-]', '', n)
    return n.lower()

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    invoice_id = clean_filename(file_key)
    upload_time = datetime.datetime.utcnow().isoformat()

    item = {
        "invoice_no": invoice_id,
        "file": file_key,
        "upload_time": upload_time,
        "status": "uploaded",
        "source_bucket": bucket,
        "amount": "unknown",
        "vendor": "unknown"
    }

    table.put_item(Item=item)

    return {
        "status": "success",
        "invoice_no": invoice_id,
        "file": file_key
    }
