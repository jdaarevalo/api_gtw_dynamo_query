import os
from aws_lambda_powertools import Logger

logger = Logger()

DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')
REGION_NAME = os.getenv('REGION_NAME', 'staging')

@logger.inject_lambda_context
def lambda_handler(event, context):
	logger.info({"action":"invoke_lambda", "payload":{"event":event}})
