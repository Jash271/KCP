require('dotenv').config();
const mongoose = require('mongoose');
//const jwt = require('jsonwebtoken');

const JobSchema = new mongoose.Schema({
    Title: {
        type: String,
        required: true
    },
    Company: {
        type: String,
        required: true,
    },
    Location: {
        type: String,
        required: true,
    },
    Link: {
        type: String,
        required: true,
    },
    Date: {
        type: Date,
        default: Date.now
    },
    Job_Tag: {
        type: String,
        required: true,
    },
    Job_Query: {
        type: String,
        required: true,
    },
    CK: {
        type: String,
        required: true,
        unique: true,
    }

},
{
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

module.exports = mongoose.model('Job', JobSchema);

