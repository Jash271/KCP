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

    exports.GetMetrics = async (req, res, next) => {
        try{
            const applications = await application.find({ User_Id: req.user._id });
            var total = applications.length;
            var applied = 0;
            var interview = 0;
            var offer = 0;
            var rejected = 0;
            
            for (let i = 0; i < applications.length; i++) {
                applied++;
                if(applications[i].Status == "Interview"){
                    interview++;
                }
                else if(applications[i].Status == "Offer"){
                    offer++;
                }
                else if(applications[i].Status == "Rejected"){
                    rejected++;
                }
            }
            const intrvw_rate = interview/total;
            const offer_rate = offer/total;
            const reject_rate = rejected/total;
    
            var last_week = 0;
            for (let i = 0; i < applications.length; i++) {
                if(applications[i].last_update_timestamp > Date.now() - 7*24*60*60*1000){
                    last_week++;
                }
            }
            return res.status(200).json({
                total: total,
                applied: applied,
                interview: interview,
                offer: offer,
                rejected: rejected,
                intrvw_rate: intrvw_rate,
                offer_rate: offer_rate,
                reject_rate: reject_rate,
                applications_last_week: last_week
            });
        }catch(e){
            console.log(e.message);
            res.status(500).send('Server Error');
        }
    }    