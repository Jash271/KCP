const express = require('express');
const router = express.Router();

const {Generate_Url,oauth2callback} = require('../controller/google_auth')
const {auth} = require('../middleware/user')
router.route('/get_signin_url').get(auth,Generate_Url)
router.route('/oauth2callback').get(oauth2callback)

module.exports = router