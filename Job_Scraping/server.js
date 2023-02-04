const axios = require('axios');
const cheerio = require('cheerio');
const ObjectsToCsv = require('objects-to-csv');
/*
var linkedinJobs = [];
 
for (let pageNumber = 0; pageNumber < 100; pageNumber += 10) {
let url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software%20developer%20internship&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=2931031787&position=1&pageNum=0&start=${pageNumber}`;
axios(url)
.then (response => {
const html = response.data;
const $ = cheerio.load(html);
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
    }
    //console.log(resp_body)
linkedinJobs.push(resp_body)
});

//const csv = new ObjectsToCsv(linkedinJobs)
//csv.toDisk('./linkedInJobs.csv', { append: true })
})
.catch();
}
*/
async function get_jobs() {
    var linkedinJobs = [];
    for (let pageNumber = 0; pageNumber < 100; pageNumber += 10) {

        let url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=software%20developer%20intern&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=2931031787&position=1&pageNum=0&start=${pageNumber}`;
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

const data = get_jobs();
data.then(response => {
    console.log(response);
}).catch(resp => {
    console.log("There was some error");
})
//console.log(data)