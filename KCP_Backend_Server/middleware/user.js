require('dotenv').config();
const jwt = require('jsonwebtoken');

const User = require('../Models/user');

exports.auth = async (req, res, next) => {
  //Get the token from the header
  try {
    const token = req.header('x-auth-token');

    //Check if not token

    if (!token) {
      return res.status(401).json({ msg: 'No token ,authorization denied' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.user.id);
    req.user = user;
    res.locals.user = user;
    next();
  } catch (err) {
    return res.status(401).json({ msg: 'Error decoding token' });
  }
};
