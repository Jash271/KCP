const express = require('express')
const router = express.Router();
const {getJobs} = require('../controller/job_posting'); 
const {auth} = require('../middleware/auth')

router.route('/getjobs').post(auth,getJobs)
module.exports = router