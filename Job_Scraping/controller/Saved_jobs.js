const savedjob = require('../Models/SavedJobs');

exports.getSavedJobs = async (req, res, next) => {
    try {
      const jobs = await savedjob.find({ User_Id:req.user.id });
      return res.status(200).json({
        jobs: jobs
      });
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
    }
  }

exports.saveJobs = async (req, res, next) => {
    try {

        const {Job_Id} = req.body;
        console.log(req.user);
        const newSavedJobs = new savedjob({
            Job_Id,
            User_Id : req.user.id
        });
        await newSavedJobs.save();
        return res.status(201).json({
        msg: 'Successfully Created',
        success: true,
        jobs:newSavedJobs,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
}  