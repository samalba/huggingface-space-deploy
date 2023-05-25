#!/bin/bash

docker buildx build \
    --push \
    --platform linux/arm64/v8,linux/amd64 \
    --tag ghcr.io/samalba/huggingface-space-deploy:latest \
    .
