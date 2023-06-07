require('dotenv').config();
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
//const application  = require('./application');
const UserSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    Gmail_Access:{
        type: Object
    },
    last_scan_timestamp:{
        type: String,
        default: '1641024000'
    },
    user_activity:{
        type: Object

    },
    avatar: {
        type: String
    },
  },
    {
        toJSON: { virtuals: true },
        toObject: { virtuals: true },
      }
);
UserSchema.methods.GetJwt = function () {
    payload = {
      user: {
        id: this._id,
      },
    };
    
    return jwt.sign(payload, process.env.JWT_SECRET, {
      expiresIn: 3600,
    });
  };

UserSchema.methods.Gen_Token = function(){
  payload = {
    user:{
      id:this._id
    }
  }
  return jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: 300,
  });
}

module.exports = mongoose.model('user', UserSchema);