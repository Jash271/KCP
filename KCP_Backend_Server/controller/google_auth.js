const {authenticate} = require('@google-cloud/local-auth');
const {google} = require('googleapis');
const User = require('../Models/user')

const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];
const oauth2Client = new google.auth.OAuth2(
    '564790885481-7d0fdgi7jirh5mke5u4r3v2dqvbj8ba9.apps.googleusercontent.com',
    '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',
    'http://localhost:5000/api/google_auth/oauth2callback'
  );

exports.Generate_Url = async (req,res,next)=>{
    try{
    const client_id = process.env.CLIENT_ID
    const user_id = req.user.id
    let old_url = process.env.REDIRECT_URI
    old_url = encodeURIComponent(old_url)
    const new_url = `https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id=${client_id}&redirect_uri=${old_url}&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=${user_id}&access_type=offline&service=lso&o2v=1&flowName=GeneralOAuthFlow`
    return res.status(200).json({
        "Msg":"Success",
        "data":new_url
    })
    }catch(e){
        console.log(e)
        return res.status(500).json({
            "Msg":"Internal Server Error"
        })
    }
}

exports.oauth2callback = async (req,res,next)=>{
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


}