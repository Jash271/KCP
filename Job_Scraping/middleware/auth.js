const axios = require('axios');
require('dotenv').config();

exports.getUserId = async (req,res,next) =>{
    try{
        const token = req.header('x-auth-token');
        const config = {
            method: 'post',
            maxBodyLength: Infinity,
            url:'http://ec2-3-227-114-48.compute-1.amazonaws.com:3000/api/user/user_data',
            headers: {"x-auth-token":token }
        };
        let res = await axios(config);
        const user = res.data.user_data;
        req.user = user;
        console.log(user);
        console.log("Middleware succ")
        next();
    }
    catch(err){
        console.log(err.message);
        return res.status(401).json({ msg: 'Error decoding token' });
    }
};

  
