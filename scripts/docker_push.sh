#!/bin/bash

set -e

echo $GCLOUD_SERVICE_KEY | base64 -d | docker login -u _json_key --password-stdin https://eu.gcr.io

export TAG=$TRAVIS_BUILD_ID"-"$TRAVIS_BRANCH

echo "Building with tags [$TAG]"

docker build -t eu.gcr.io/census-int-ci/census-rh-ui:$TAG .

docker push eu.gcr.io/census-int-ci/census-rh-ui:$TAG
