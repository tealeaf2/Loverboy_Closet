#!/bin/bash

#Commands to run
npm run build
nohup npm run start > npm.log 2>&1 &
nohup flask run > flask_app.log 2>&1 &