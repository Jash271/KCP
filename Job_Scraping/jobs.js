var axios = require('axios');

async function get_data_adzuna(config) {
    var final_data = []
    let res = await axios(config);
    res = res['data']['results']
    res.forEach((ele)=>{
        job_body = {
            'Title':ele['title'],
            'Company':ele['company']['display_name'],
            'Location':ele['location']['display_name'],
            'Link':ele['redirect_url']
        }
        final_data.push(job_body)
    })
    return final_data
}

async function get_data_muse(config) {
    var final_data = []
    let res = await axios(config);
    res = res['data']['results']
    res.forEach((ele)=>{
        job_body = {
            'Title':ele['categories'][0]['name'],
            'Company':ele['company']['name'],
            'Location':ele['locations'][0]['name'],
            'Link':ele['refs']['landing_page']
        }
        final_data.push(job_body)
    })
    return final_data
}
// adzuna
var adzuna = {
    method: 'get',
    maxBodyLength: Infinity,
    url: 'https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=7b3acc2a&app_key=0303f4e0c1aca9c49e5b2565e8ea3503&results_per_page=20&what=software%20engineer',
    headers: { }
    };
var config = {
    method: 'get',
    maxBodyLength: Infinity,
    url: 'https://www.themuse.com/api/public/jobs?api_key=b9c1e4d07be7190935f7d5b745fdc2a5c6034de0caea6fea11767c5b9d791b75&page=10&categories=Software%Engineer',
    headers: { }
    };    
// get_data_adzuna(adzuna).then(res=>{
//     console.log(res);
// }).catch(e=>{
//     console.log(e);
// });
get_data_muse(config).then(res=>{
    console.log(res);
}).catch(e=>{
    console.log(e);
});