const express = require('express')
const router = express.Router();


const {getPosts} = require('../controller/user');
// const {auth} = require('../middleware/auth');

router.route('/getpost').get(getPosts);

module.exports = router