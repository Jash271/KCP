const express = require('express')
const router = express.Router();

const {auth} = require('../middleware/auth');

const {getPosts} = require('../controller/user');
// const {auth} = require('../middleware/auth');

router.route('/getpost').get(auth,getPosts);

module.exports = router