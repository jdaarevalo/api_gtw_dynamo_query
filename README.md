# Query DynamoDB data using API Gateway


# Schedule Lambda to sync Athena with DynamoDB table
This lambda run's with the following cron job expressions, which mean it will run daily at 5:00 am.
```bash
cron(0 5 * * ? *)
```

### Create the virtual environment

```bash
conda create -n "api_gtw_dynamo_query" python=3.10 ipython
```

To activate this environment, use

```bash
conda activate api_gtw_dynamo_query
```

optional, ensure your python path is correct 

```bash
export PATH="/Users/David/opt/anaconda3/envs/api_gtw_dynamo_query/bin:$PATH"
```

### Install Dev requirements

```bash
pip install -r requirements_dev.txt
```

### Initialize DynamoDB 

Initialize the DynamoDB container using Docker Compose

```bash
docker-compose up
```

Check if the table exists

```bash
aws dynamodb list-tables --endpoint-url http://localhost:8000

```

If it is required, create the table with the file `create_dynamodb_table.json`

```bash
aws dynamodb create-table --cli-input-json file://create_dynamodb_table.json --endpoint-url http://localhost:8000
```

#### Delete DynamoDB table

```bash
aws dynamodb delete-table --table-name fielwork_monitoring --endpoint-url http://localhost:8000
```

### Insert Dummy Data in DynamoDB

```bash
cd dynamo_dummy_data
chmod +x put_dummy_data.sh 
./put_dummy_data.sh
```

Check the dummy data with the `scan` command to read every item in the table

```bash
aws dynamodb scan --table-name fielwork_monitoring --endpoint-url http://localhost:8000
```


