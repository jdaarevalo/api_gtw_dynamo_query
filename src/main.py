import os
import awswrangler as wr
import boto3
from aws_lambda_powertools import Logger

logger = Logger()
boto3_session = boto3.Session()

DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')
REGION_NAME = os.getenv('REGION_NAME', 'staging')
FIELDWORK_QUERY = """
	SELECT
		survey_uuid,
		question_id,
		budget,
		spent_budget
	FROM fieldwork_monitoring.fieldwork_complete_status
	"""

@logger.inject_lambda_context
def lambda_handler(event, context):
     logger.info({"action":"invoke_lambda", "payload":{"event":event}})
     # get data from fieldwork_complete_status
     fieldwork_data_df = wr.athena.read_sql_query(
         sql=FIELDWORK_QUERY, database="formatted_data", boto3_session=boto3_session
     )
     logger.info({"action":"fieldwork_data", "payload":{"len_fieldwork_data":len(fieldwork_data_df)}})
     # write to dynamodb
     process_and_update_dynamodb(fieldwork_data_df)
     logger.info({"action":"write_to_dynamodb_finished"})

def process_and_update_dynamodb(results_df):
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    # Iterate through the DataFrame rows
    for index, row in results_df.iterrows():
        survey_uuid = row['survey_uuid']
        question_id = row['question_id']
        budget = row['budget']
        spent_budget = row['spent_budget']
        
        # Construct the key and update expression for DynamoDB
        response = table.update_item(
            Key={
                'survey_uuid': survey_uuid,
                'question_id': question_id
            },
            UpdateExpression="SET budget = :budget, spent_budget = :spent_budget",
            ExpressionAttributeValues={
                ':budget': str(budget),
                ':spent_budget': str(spent_budget)
            },
            ReturnValues="UPDATED_NEW"
        )
        logger.info({"action": "update_dynamodb_response", "payload": response})
