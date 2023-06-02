#!/bin/bash

# Download SAM checkpoint if not already downloaded
if [ ! -d "opendream/checkpoints" ]; then
    mkdir -p opendream/checkpoints
fi
if [ ! -f "opendream/checkpoints/sam_vit_h_4b8939.pth" ]; then
    wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P opendream/checkpoints/
fi


# Start uvicorn server
pip install -r requirements.txt && uvicorn opendream.server:app --reload &

# Change directory to webapp/opendream-ui and start npm
cd webapp/opendream-ui && npm install && npm run start &

wait