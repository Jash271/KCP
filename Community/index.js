require('dotenv').config();
const axios = require('axios');
const morgan = require('morgan');
const cheerio = require('cheerio');
const { connectDB, mongodb } = require('./config/db');
const express = require('express');
const cors = require('cors');

const User = require('./Routes/user');

const feed = require('./Routes/feed')

const app = express();
app.use(cors());

app.use(morgan('dev'));
connectDB()
app.use(express.json({ extended: false }));
const PORT = process.env.PORT || 6969;

app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
  });

app.get('/', (req, res) => {
      res.send('Feed Started');
      }
  );

app.use('/feed',feed)
// app.use('/feed')
app.use('/user',User)
