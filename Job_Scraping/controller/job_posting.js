const jobs = require('../Models/Jobs');
const user = require('../Models/user');
const {BloomFilter} = require('bloom-filters')

const redis_client = require('../config/redis');

/*

Approach : Maintain a list of job ids that the user has already seen.
Vanilla Approach :  Iterate through the list of jobs and check if the job id is present in the list of jobs that the user has already seen.
Time Complexity : O(nm)
Space Complexity : O(n)
m -> number of jobs user has already seen
n -> number of jobs in the database

Bloom Filter Approach : Maintain a bloom filter of the job ids that the user has already seen.
Time Complexity : O(n)
Space Complexity : slightly less than O(n)
Set Membership Test : O(1)
 
Bloom Filter Approach will be meaningful when the number of jobs that the user has already seen is large.
Assume if the user has already seen 1000 jobs
In the vanilla approach,
we will iterate through the batch of jobs which is of length 20, then for each item in the batch we will iterate through the list of jobs that the user has already seen.
So, the time complexity will be O(20*1000) = O(20000)

However, in the bloom filter approach, we will just check if the job id is present in the bloom filter or not.Since Set Membership is O(1), 
the time complexity will be O(20) = O(1)

*/
exports.getJobs = async (req, res, next) => {
    try {
      const page = parseInt(req.query.page);
      const limit = parseInt(req.query.limit);
      const startIndex = (page - 1) * limit;
      const session_activity = req.body.session_activity;
      // check if jobs exist against page no in redis
      let Jobs = [];
      const redis_jobs = await redis_client.get(page);
      if (redis_jobs) {
        console.log('Fetching from Redis')
        Jobs = JSON.parse(redis_jobs);
      } else {
        console.log('Fetching from DB')
        Jobs = await jobs.find().sort({Date: -1}).skip(startIndex).limit(limit);
        redis_client.setex(page, 172800 , JSON.stringify(Jobs));
      }
      const job_len = Jobs.length;
      const usr = await user.findById(req.user.id);
      if (!usr) {
        return res.status(404).json({
          success: false,
          msg: 'User not found',
        });
      }
      if (!usr.user_activity) {
        let filter = new BloomFilter(10000, 10);
        usr.user_activity = filter.saveAsJSON();
        await usr.save();
      }
      const filter = BloomFilter.fromJSON(usr.user_activity);
      for (let i = 0; i < session_activity.length; i++) {
        filter.add(session_activity[i].id);
      }
      usr.user_activity = filter.saveAsJSON();
      await usr.save();
      let old_arr = [];
      let new_arr = [];
      
      for (let i = 0; i < job_len; i++) {
        if (filter.has(Jobs[i].id)) {
          old_arr.push(Jobs[i]);
        } else {
          new_arr.push(Jobs[i]);
        }
      }
      const res_ = new_arr.concat(old_arr);
      return res.status(200).json({
        success: true,
        count: res_.length,
        data: res_
      });
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
    }
  }