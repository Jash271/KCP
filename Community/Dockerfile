FROM node:12.18.1
 
WORKDIR /community
 
COPY package.json package.json
COPY package-lock.json package-lock.json
 
RUN npm install
 
COPY . .

EXPOSE 6969
 
CMD [ "node", "index.js" ]