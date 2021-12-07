#!/bin/bash
mkdir my-lambda-layer && cd my-lambda-layer
mkdir -p aws-layer/python/lib/python3.7/site-packages

# Install libraries 
pip3 install -r ../requirements.txt  --target aws-layer/python/lib/python3.7/site-packages

# Create a zip file for the layer to upload
cd aws-layer
zip -r9 lambda-layer.zip .


# Create Lambda layer
aws lambda publish-layer-version \
    --layer-name Data-Preprocessing \
    --description "My Python layer" \
    --zip-file fileb://lambda-layer.zip \
    --compatible-runtimes python3.7