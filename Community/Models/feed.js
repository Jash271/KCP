require('dotenv').config();
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
//const application  = require('./application');
const FeedSchema = new mongoose.Schema({
    User_Id: {
        type: mongoose.Schema.ObjectId,
        required: true,
        ref: 'user'
    },
    title:{
        type: String,
        required: true
    },
    post: {
        type: String,
        required: true
    },
    tags:{
        type: Object
    },
    timestamp:{
        type: Date,
        default: Date.now
    },
    image:{
        type: String
    },
  },
    {
        toJSON: { virtuals: true },
        toObject: { virtuals: true },
      }
);

// see this
// FeedSchema.virtual('Feed', {
//     ref: 'job',
//     localField: 'Job_Id',
//     foreignField: '_id',
//     justOne: true
// });

FeedSchema.virtual('user_data', {
    ref: 'user',
    localField: 'User_Id',
    foreignField: '_id',
    justOne: true
});


module.exports = mongoose.model('feed', FeedSchema);