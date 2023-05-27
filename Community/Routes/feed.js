const express = require('express')
const router = express.Router();
const {auth} = require('../middleware/auth');
const {createPost} = require('../controller/feed');
const {getFeed} = require('../controller/feed');
// const {auth} = require('../middleware/auth');

// router.route('/createpost').post(auth, createPost)

router.route('/createpost').post(auth,createPost);
router.route('/discuss').get(getFeed);
module.exports = router