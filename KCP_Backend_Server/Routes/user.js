const express = require('express');
const router = express.Router();

const {Signup,Login,GetUserData,UpdateLastScanTime} = require('../controller/user')
const {auth}  = require('../middleware/user')
router.route('/signup').post(Signup)
router.route('/login').post(Login)
router.route('/user_data').post(auth,GetUserData)
router.route('/update_last_scan_time').put(auth,UpdateLastScanTime)
module.exports = router