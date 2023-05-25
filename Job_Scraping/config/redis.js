require('dotenv').config();
const Redis = require("ioredis");

const PORT = 15433
const HOST = "redis-15443.c16.us-east-1-3.ec2.cloud.redislabs.com"
const PASSWORD = "omMRz97Tmk7rLPL8LsNQJBIUi8XINYov"
const redis = new Redis({
    port: 16535,
    host: 'redis-16535.c265.us-east-1-2.ec2.cloud.redislabs.com',
    password: 'apwzb1fs66VzatV6as2FuEAvtCmrcqqD'
    });

module.exports = redis;

