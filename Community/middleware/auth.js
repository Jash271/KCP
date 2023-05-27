const axios = require('axios');
require('dotenv').config();
const { ObjectId } = require('mongodb');
const { connectDB, mongodb } = require('../config/db');
const jwt = require('jsonwebtoken');
  
exports.auth = async (req, res, next) => {
    //Get the token from the header
    try {
      const token = req.header('x-auth-token');
  
      //Check if not token
  
      if (!token) {
        return res.status(401).json({ msg: 'No token ,authorization denied' });
      }
  
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const userCursor = await mongodb.db.collection('users').find({ _id : ObjectId(decoded.user.id) });
      const users = await userCursor.toArray();
      req.user = users[0];
      //console.log(req);
      res.locals.user = users[0];
      next();
    } catch (err) {
      console.log(err.message);
      return res.status(401).json({ msg: 'Error decoding token' });
    }
  };
  

