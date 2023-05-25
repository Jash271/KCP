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
        ref: 'Job' 
    },
    date: {
        type: Date,
        default: Date.now,
    },
    last_update_timestamp: {
        type: Date,
        default: Date.now,
    },
    update_at: {
        type: Date,
    },
    random_str:{
        type: String
    }
},
    {
        toJSON: { virtuals: true },
        toObject: { virtuals: true },
    }
);


SavedJobSchema.virtual('Job_data', {
    ref: 'Job',
    localField: 'Job_Id',
    foreignField: '_id',
    justOne: true
});

module.exports = mongoose.model('savedjob', SavedJobSchema);