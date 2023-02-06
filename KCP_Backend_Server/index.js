require('dotenv').config();
const axios = require('axios');
const morgan = require('morgan');
//const Connectdb = require('./config/db');
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const User = require('.//Models/user')
const user = require('./Routes/user')
const Google_Auth = require('./Routes/google_auth')
const app = express();
app.use(cors());

app.use(morgan('dev'));
//app.use('/api/user',user)
connectDB()
app.use(express.json({ extended: false }));
const PORT = process.env.PORT || 5000;


/*const oauth2Client = new google.auth.OAuth2(
  process.env.CLIENT_ID,process.env.CLIENT_SECRET,process.env.REDIRECT_URI);*/
app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
  });
app.use('/api/user',user)
app.use('/api/google_auth',Google_Auth)
  app.get('/', (req, res) => {
      res.send('KCP Backend Server');
      }
  );

app.get('/oauth2callback',async(req,res)=>{
  try{
    const user_id = req.query['state']
    const {tokens} = await oauth2Client.getToken(req.query['code']);
    const user = await User.findById(user_id)
    user.Gmail_Access = tokens
    await user.save();
    return res.status(200).json({
        "msg":"Success",
        "data":tokens
    })
    }catch(e){
        return res.status(500).json({
            "msg":`There was some error ${e}`
        })
    }
})