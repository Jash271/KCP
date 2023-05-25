require('dotenv').config();
const mongoose = require('mongoose');
const user = require('./user');
const ApplicationSchema = new mongoose.Schema({
    User_Id: {
        type: mongoose.Schema.ObjectId,
        required: true,
        ref: 'user'
    },
    Company_Name: {
        type: String,
        //required: true
    },
    Position:{
        type: String,
        //required: true
    },
    Status:{
        type: [String],
    },
    last_update_timestamp:{
        type: String,
    },
    notes:{
        type:String
    }
},
{
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
    }
);

ApplicationSchema.virtual('User', {
    ref: 'user',
    localField: 'User_Id',
    foreignField: '_id',
    justOne: true
});

module.exports = mongoose.model('application', ApplicationSchema);


     
        
        