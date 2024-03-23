#!/bin/bash
LOCATION=europe-west1
LOGGER_DOMAIN=""

function print_usage {
  echo "Usage: bash install.sh -p project_id -d db_password [-l location -u data-logger-domain]"
}

while getopts 'p:l:d:u:' flag; do
  case "${flag}" in
    p) PROJECT_ID="${OPTARG}" ;;
    l) LOCATION="${OPTARG}" ;;
    d) DB_PASSWORD="${OPTARG}" ;;
    u) LOGGER_DOMAIN="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

gcloud config set project $PROJECT_ID
gcloud services enable artifactregistry.googleapis.com

gcloud artifacts repositories create data-logger \
    --project=$PROJECT_ID \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/data-logger/data-logger:latest ./modules/data-logger/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/data-logger/data-logger:latest

gcloud artifacts repositories create message-consumer \
    --project=$PROJECT_ID \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/message-consumer/message-consumer:latest ./modules/message-consumer/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/message-consumer/message-consumer:latest

gcloud artifacts repositories create information-system \
    --project=$PROJECT_ID \
    --repository-format=docker \
    --location=$LOCATION

docker build -t $LOCATION-docker.pkg.dev/$PROJECT_ID/information-system/information-system:latest ./modules/information-system/
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/information-system/information-system:latest

terraform init
terraform apply \
-var project_id=$PROJECT_ID \
-var region=$LOCATION \
-var db_password=$DB_PASSWORD \
-var data-logger_domain=$LOGGER_DOMAIN
