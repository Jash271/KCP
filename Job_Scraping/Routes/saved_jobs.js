const express = require('express')
const router = express.Router();

const {getSavedJobs,saveJobs} = require('../controller/Saved_jobs');
const {auth} = require('../middleware/auth');

router.route('/getsavedjobs').post(auth,getSavedJobs);
router.route('/savedjobs').post(auth,saveJobs);
module.exports = router
