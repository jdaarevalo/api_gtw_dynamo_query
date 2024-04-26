#!/bin/bash

if ! [[ $1 ]]; then
  echo "use: $0 <ENVIRONMENT {production, staging}>"
  exit 1
fi

# Variables
export AWS_REGION=eu-west-1
export ENVIRONMENT="staging"
export AWS_PROFILE="channels-${ENVIRONMENT}"

rm -rf .aws-sam/

STACK_NAME="api-gtw-dynamodb-query"

template_file=$(pwd)/template.yaml
if [[ -f $template_file ]]; then
  sam build -t $template_file

  sam deploy \
    --no-fail-on-empty-changeset \
    --profile=${AWS_PROFILE} \
    --stack-name "${STACK_NAME}-${ENVIRONMENT}" \
    --region "${AWS_REGION}" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Environment=${ENVIRONMENT} \
    --s3-prefix ${STACK_NAME} \
    --resolve-s3 \
    --resolve-image-repos \
    --force-upload --debug
else
  echo "No SAM template found for deployment".
fi
