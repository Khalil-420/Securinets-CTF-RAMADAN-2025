#!/bin/sh
# entrypoint.sh

# Resolve the IP address of the 'app' service
APP_IP=$(getent hosts app | awk '{ print $1 }')
echo "executing entrypoint"
# Start the bot application (replace this with the actual command to start your bot)
exec node /home/bot/index.js
