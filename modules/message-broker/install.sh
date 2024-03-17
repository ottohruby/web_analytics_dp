#!/bin/bash
LOCATION=europe-west1
PROJECT_ID=otto-hruby-dp2

function print_usage {
  echo "Usage: bash install.sh -p project_id [-l location]"
}

while getopts 'p:l:' flag; do
  case "${flag}" in
    p) PROJECT_ID="${OPTARG}" ;;
    l) LOCATION="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

gcloud artifacts repositories create data-logger \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/data-logger/data-logger:latest ./modules/data-logger/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/data-logger/data-logger:latest

gcloud artifacts repositories create message-consumer \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/message-consumer/message-consumer:latest ./modules/message-consumer/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/message-consumer/message-consumer:latest

gcloud artifacts repositories create information-system \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/information-system/information-system:latest ./modules/information-system/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/information-system/information-system:latest

terraform init

