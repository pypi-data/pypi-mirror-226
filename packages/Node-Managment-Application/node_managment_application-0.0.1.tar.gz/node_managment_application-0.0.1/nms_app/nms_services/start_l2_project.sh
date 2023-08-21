#!/usr/bin/bash
cd /home/ubuntu/L2_App/
sudo chmod 777 createEnvFile.sh
./createEnvFile.sh
sudo docker-compose --env-file alkimiL2Node.env up -d