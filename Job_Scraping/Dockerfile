FROM node:12.18.1
 
WORKDIR /job
 
COPY package.json package.json
COPY package-lock.json package-lock.json
 
RUN npm install
 
COPY . .

EXPOSE 5050

CMD [ "node", "server.js" ]