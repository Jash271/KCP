const Redis = require("ioredis");

const redis = new Redis({
    port: 15443, // Redis port
    host: "redis-15443.c16.us-east-1-3.ec2.cloud.redislabs.com", // Redis host
    password: 'omMRz97Tmk7rLPL8LsNQJBIUi8XINYov'
    });
/*
const work = async() => {
    try {
        await redis.setex("foo",1 ,"bar");
        const result = await redis.get("foo");
        console.log(result);
      } catch (error) {
        console.error(error);
      } finally{
        redis.disconnect();
      }
}
*/

const get_data = async() => {
    try {
        // remove key from redis 
        await redis.del(1);
        await redis.del(2);
}finally{
    redis.disconnect();
}
}
//work();
get_data();
