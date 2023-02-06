const express = require('express');
const router = express.Router();

const {Signup,Login,GetUserData} = require('../controller/user')
const {auth}  = require('../middleware/user')
router.route('/signup').post(Signup)
router.route('/login').post(Login)
router.route('/user_data').post(auth,GetUserData)
module.exports = router