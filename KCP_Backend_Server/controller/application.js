const application = require('../Models/application');
//const user = require('../models/user');

exports.getApplications = async (req, res, next) => {
  try {
    const applications = await application.find({ User_Id: req.user._id });
    return res.status(200).json({
      applications: applications,
    });
  } catch (err) {
    console.log(err.message);
    res.status(500).send('Server Error');
  }
}
/*
exports.getApplication = async (req, res, next) => {
    try {
        const application = await application.findById(req.params.id);
        res.status(200).json({
        application: application,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }
*/
exports.createApplication = async (req, res, next) => {
    try {
        const { Company_Name, Position, Status, last_update_timestamp, notes } = req.body;
        const newApplication = new application({
        Company_Name,
        Position,
        Status,
        last_update_timestamp,
        notes,
        User_Id: req.user._id,
        });
        await newApplication.save();
        return res.status(201).json({
        msg: 'Successfully Created',
        success: true,
        application: newApplication,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }

exports.updateApplication = async (req, res, next) => {
    try {
        const { Company_Name, Position, Status, last_update_timestamp, notes } = req.body;
        const updatedApplication = await application.findByIdAndUpdate(
        req.params.id,
        {
            Company_Name,
            Position,
            Status,
            last_update_timestamp,
            notes,
        },
        { new: true }
        );
        return res.status(200).json({
        msg: 'Successfully Updated',
        success: true,
        application: updatedApplication,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }
/*
exports.deleteApplication = async (req, res, next) => {
    try {
        await application.findByIdAndDelete(req.params.id);
        res.status(200).json({
        msg: 'Successfully Deleted',
        success: true,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }

exports.deleteAllApplications = async (req, res, next) => {
    try {
        await application.deleteMany({ User_Id: req.user._id });
        res.status(200).json({
        msg: 'Successfully Deleted',
        success: true,
        });
    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }
*/

exports.handle_batch = async (req, res, next) => {
    try {
        const { batch } = req.body;
        for (let i = 0; i < batch.length; i++) {
        const { Company_Name, Position, Status, last_update_timestamp, notes,user_id } = batch[i];
        // check if application exists based on Company_Name and Position
        const existingApplication = await application.findOne({
            Company_Name,
            Position,
            User_Id: user_id,
        });
        if (existingApplication) {
            const updatedApplication = await application.findByIdAndUpdate(
            existingApplication._id,
            {
                Status,
                last_update_timestamp,
                notes,
            },
            { new: true }
            );
        }
        else {
            const newApplication = new application({
            Company_Name,
            Position,
            Status,
            last_update_timestamp,
            notes,
            User_Id: user_id,
            });
            await newApplication.save();
        }
        }
        return res.status(201).json({
        msg: 'Successfully Created',
        success: true,
        });

    } catch (err) {
        console.log(err.message);
        res.status(500).send('Server Error');
    }
    }