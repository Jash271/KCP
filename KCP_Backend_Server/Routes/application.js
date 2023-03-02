const express = require('express')
const router = express.Router();

const {createApplication,updateApplication,getApplications,handle_batch} = require('../controller/application')
const {auth}  = require('../middleware/user')

router.route('/create_application').post(auth,createApplication)
router.route('/update_application/:id').put(auth,updateApplication)
router.route('/get_applications').get(auth,getApplications)
router.route('/handle_batch').post(handle_batch)

module.exports = router


