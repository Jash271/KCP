const express = require('express')
const router = express.Router();

const {getSavedJobs,saveJobs} = require('../controller/Saved_jobs');
const {getUserId} = require('../middleware/auth');

router.route('/getsavedjobs').post(getUserId,getSavedJobs);
router.route('/savedjobs').post(getUserId,saveJobs);
module.exports = router
