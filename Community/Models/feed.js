require('dotenv').config();
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
//const application  = require('./application');
const FeedSchema = new mongoose.Schema({
    User_Id: {
        // type: mongoose.Schema.ObjectId,
        type: String,
        required: true
        // ref: 'user'
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
    }
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

module.exports = mongoose.model('feed', FeedSchema);