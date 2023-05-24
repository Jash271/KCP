const express = require('express')
const router = express.Router();

const {createPost} = require('../controller/feed');
const {getFeed} = require('../controller/feed');
// const {auth} = require('../middleware/auth');

// router.route('/createpost').post(auth, createPost)

router.route('/createpost').post(createPost);
router.route('/discuss').get(getFeed);
module.exports = router