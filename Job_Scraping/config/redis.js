require('dotenv').config();
const Redis = require("ioredis");


const redis = new Redis({
    port: process.env.PORT,
    host: process.env.HOST, // Redis host
    password: process.env.PASSWORD
    });

module.exports = redis;