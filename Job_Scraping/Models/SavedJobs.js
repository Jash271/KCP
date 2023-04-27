require('dotenv').config();
const mongoose = require('mongoose');

const SavedJobSchema = new mongoose.Schema({
    User_Id: {
        type: mongoose.Schema.ObjectId,
        required: true,
    },
    Job_Id:{
        type: mongoose.Schema.ObjectId,
        required: true,
        ref: 'job' 
    }
},
    {
        toJSON: { virtuals: true },
        toObject: { virtuals: true },
    }
);


SavedJobSchema.virtual('Job', {
    ref: 'job',
    localField: 'Job_Id',
    foreignField: '_id',
    justOne: true
});

module.exports = mongoose.model('savedjob', SavedJobSchema);