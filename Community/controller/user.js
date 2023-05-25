const { debug } = require('request');
const feed = require('../Models/feed');

exports.getPosts = async (req, res, next) => {
    try {
    //   const jobs = await feed.find({ User_Id:req.user.id });
    const posts = await feed.find({ User_Id:req.body.id });
      return res.status(200).json({
        posts: posts
      });
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
    }
  }