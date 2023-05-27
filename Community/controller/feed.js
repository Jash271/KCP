const { debug } = require('request');
const feed = require('../Models/feed');


exports.getFeed = async (req, res, next) => {
  try {
    // const discuss = await feed.find().sort({Date: -1}).skip(startIndex).limit(limit);
    const discuss = await feed.find().sort({timestamp: -1}).populate('user_data', ['name', 'email', 'avatar']);
      return res.status(200).json({
        discuss: discuss
      });
    } catch (err) {
      console.log(err.message);
      res.status(500).send('Server Error');
  }
}

exports.createPost = async (req, res, next) => {
  try {
    const usr = req.user.id
    const { title, post, tags } = req.body;
    console.log(req.body);
    const newPost = new feed({
      // User_Id: req.user._id,
      User_Id: usr,
      title: title,
      post: post,
      tags: tags
    });
    console.log(newPost);
    await newPost.save();
    return res.status(201).json({
      msg: 'Successfully Created',
      success: true,
      feed: newPost,
    });
  } catch (err) {
    console.log(err.message);
    res.status(500).send('Server Error');
  }
}