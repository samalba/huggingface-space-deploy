#!/bin/bash

docker buildx build \
    --push \
    --platform linux/arm64/v8,linux/amd64 \
    --tag samalba/hugginface-space-deploy:latest \
    .
