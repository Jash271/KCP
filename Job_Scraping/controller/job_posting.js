const jobs = require('../Models/Jobs');

exports.getJobs = async (req, res, next) => {
    try {
      const jobs_1 = await jobs.find();
      return res.status(200).json({
        jobs: jobs_1,
      });
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
    }
  }