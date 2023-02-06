require('dotenv').config();
const User = require('../Models/user')
const bcrypt = require('bcryptjs');

exports.Signup = async (req, res) => {
    const { name, email, password } = req.body;
    try {
      const user = await User.findOne({ email });
      console.log(1);
      if (user) {
        res.status(400).json({ message: 'User already exists', success: false });
      } else {
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);
        const newUser = new User({
          name,
          email,
          password: hash
        });
        v_token = newUser.Gen_Token()
        await newUser.save();
        console.log(2);
  
        token = newUser.GetJwt();
        
        return res.status(201).json({
          msg: 'Successfully Registered',
          success: true,
          token: token,
          user: newUser,
        });
      }
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
    }
  };
  
  exports.Login = async (req, res, next) => {
    try {
      const { email, password } = req.body;
      let user = await User.findOne({ email: email }).select('+password');
      if (!user) {
        return res.status(400).json({ msg: 'Authentication Error' });
      }
      const compare = await bcrypt.compare(password, user.password);
      if (!compare) {
        return res.status(400).json({ msg: 'Authentication Error' });
      }
      const token = user.GetJwt();
      return res.status(200).json({
        msg: 'Successfully Logged In',
        success: true,
        token: token,
        user: user,
      });
    } catch (error) {
      console.log(err.message);
      return res.status(500).json({ msg: 'Internal Server Error' });
    }
  };
  
  exports.hello = async(req,res,next)=>{
    return res.status(500).json({
        msg:'Hello'
    })

  }
  
exports.GetUserData = (req,res,next)=>{
    console.log(req.user._id,req.user.name)
    return res.status(201).json({
        'user_data':req.user
    })
}
