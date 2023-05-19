#!/bin/bash

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

sudo apt install docker-compose -y

# nvm install 16
# echo "Node Installed"
git clone https://github.com/Jash271/KCP.git
# echo :"folder cloned"
cd KCP/
sudo docker-compose up
# echo "In folder"
# npm install
# echo "dep installed"
# node index.js
# echo "server started!"