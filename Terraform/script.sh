#!/bin/bash

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 16
echo "Node Installed"
git clone https://github.com/Jash271/kcp_Node_Server.git
echo :"folder cloned"
cd kcp_Node_Server
echo "In folder"
npm install
echo "dep installed"
node index.js
echo "server started!"