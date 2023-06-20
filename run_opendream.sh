#!/bin/bash

# Start uvicorn server
pip install -r requirements.txt && uvicorn opendream.server:app --reload &

# Change directory to webapp/opendream-ui and start npm
cd webapp/opendream-ui && npm install && npm run start &

wait
