require('dotenv').config();

const mongoose = require('mongoose');

const db = process.env.MongoURI;
const mongodb = mongoose.connection;

const connectDB = async () => {
  try {
    await mongoose.connect(db, {
        useNewUrlParser: true,
        //useCreateIndex: true,
        //useFindAndModify: true,
        useUnifiedTopology: true,
        // authenticationDatabase: process.env.AUTHENTICATION_DATABASE,
        // ssl: process.env.DATABASE_SSL,
    });
    console.log('Mongodb Connected ....');
  } catch (err) {
    console.log(err.message);
    process.exit(1);
  }
};

module.exports = { connectDB, mongodb };