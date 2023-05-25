const axios = require('axios');
const cheerio = require('cheerio');
const ObjectsToCsv = require('objects-to-csv');
const CronJob = require('cron').CronJob;
const morgan = require('morgan');
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const Job = require('./Models/Jobs');
const job_postings = require('./Routes/job_tracking');
const saved_jobs = require('./Routes/saved_jobs');
//Job.createIndexes({ Title: "text", Company: "text", Location: "text", Job_Tag: "text", Job_Query: "text" },{unique:true});
const app = express();
app.use(cors({
    origin: '*'
}));
connectDB()
app.use(morgan('dev'));
app.use(express.json({ extended: false }));
const PORT = process.env.PORT || 5050;

app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
  });

  app.get('/', (req, res) => {
      res.send('KCP Jobs MicroService Backend Server');
      }
  );


async function get_jobs(job_type) {
    var linkedinJobs = [];
    for (let pageNumber = 0; pageNumber < 100; pageNumber += 10) {
        var req_str = job_type.split(" ").join("%20")
        let url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=${req_str}&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=2931031787&position=1&pageNum=0&start=${pageNumber}`;
        response = await axios(url);
        const html = response.data;
        const $ = await cheerio.load(html);
        const jobs = $('li')
        jobs.each((index, element) => {

            const jobTitle = $(element).find('h3.base-search-card__title').text().trim()
            const company = $(element).find('h4.base-search-card__subtitle').text().trim()
            const location = $(element).find('span.job-search-card__location').text().trim()
            const link = $(element).find('a.base-card__full-link').attr('href')
            const resp_body = {
                'Title': jobTitle,
                'Company': company,
                'Location': location,
                'Link': link,
                "Job_Tag":"Linkedin",
                "Job_Query":job_type,
                "CK":jobTitle+company+location
            }
            //console.log(resp_body)
            linkedinJobs.push(resp_body);
        })
    }
    //console.log(linkedinJobs)
    resp = {
        "data": linkedinJobs
    }
    return resp
}


const Linkedin_Job = new CronJob('* * * * * 2', function() {
    console.log("LinkedIn Cron Job Started");
    const data = get_jobs("Software Engineer");
    data.then(response => {
    let tmp_res = response['data'];
    Job.insertMany(tmp_res,{ordered:false}).then(resp => { console.log("Linkedin Jobs Inserted") }).catch(err => { 

        console.log("Linkedin")
        //onsole.log(err)                           
    })
    }).catch(err => { console.log("There was error") })
    }, null, true, 'America/Los_Angeles');
//console.log(data)

const fetch_adzuna_job = async (job_type) => {
    var req_str = job_type.split(" ").join("%20")
    const config = {
        method: 'get',
        maxBodyLength: Infinity,
        url:`https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=7b3acc2a&app_key=0303f4e0c1aca9c49e5b2565e8ea3503&results_per_page=20&what=${req_str}`,
        headers: { }
        };
        var final_data = []
        
        let res = await axios(config);
        res = res['data']['results']
        res.forEach((ele)=>{
            job_body = {
                'Title':ele['title'],
                'Company':ele['company']['display_name'],
                'Location':ele['location']['display_name'],
                'Link':ele['redirect_url'],
                'Job_Tag':"Adzuna",
                'Job_Query':job_type,
                'CK':ele['title']+ele['company']+ele['location']
            }
            final_data.push(job_body)
        })
        return final_data
}

const Adzuna_Job = new CronJob(' * * * * 2', function() {
    console.log("Adzuna Cron Job Started");
    const data = fetch_adzuna_job("Software Engineer");
    data.then(response => {
    Job.insertMany(response,{ordered:false}).then(resp => { console.log("Adzuna Jobs Inserted") }).catch(err => { 
        console.log("Adzuna")
        //console.log(err)                         
    })
    }).catch(resp => {
    console.log("There was some error");
    })}, null, true, 'America/Los_Angeles');
//console.log(data)

Linkedin_Job.start();
Adzuna_Job.start();

app.use('/api/job_postings',job_postings);
app.use('/api/savejobs',saved_jobs);
