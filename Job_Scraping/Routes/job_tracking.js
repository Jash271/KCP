const express = require('express')
const router = express.Router();
const {getJobs} = require('../controller/job_posting'); 


router.route('/getjobs').post(getJobs)
module.exports = router