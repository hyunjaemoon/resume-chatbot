#!/bin/bash

export GOOGLE_CLOUD_PROJECT='resume-chatbot-generator'
export GOOGLE_CLOUD_REGION='us-central1'
export SERVICE_NAME='mesop-app'

gcloud run deploy $SERVICE_NAME \
    --source . \
    --port=8080 \
    --allow-unauthenticated \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_REGION \
    --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
    --set-env-vars=GOOGLE_CLOUD_REGION=$GOOGLE_CLOUD_REGION
