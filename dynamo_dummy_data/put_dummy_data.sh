#!/bin/bash
# This script inserts sample data into the DynamoDB table

items=("item_1.json" "item_2.json")

for item in "${items[@]}"
do
  echo "Inserting $item"
  aws dynamodb put-item --table-name fielwork_monitoring --item file://$item --endpoint-url http://localhost:8000
done
echo "Done"
exit 0
