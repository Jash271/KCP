import nltkmodules
from flask import Flask, request

from resume_gen import paraphrase_fn
from similarity_check import get_response

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/upload", methods=['POST'])
def uploadPDF():
    form_data = request.form
    resume_text = form_data['resume_str']
    jd_text = form_data['jd_str']
    f = request.files['resume_pdf']
    client_response = get_response(jd_text, resume=resume_text, resume_obj=f)
    return client_response


@app.route("/resume/paraphrase", methods=['POST'])
def paraphrase():
    form_data = request.form

    p_text = form_data['p_text']
    p_out = paraphrase_fn(p_text)

    return p_out


@app.route("/resume/gen_resume", methods=['POST'])
def gen_resume():
    form_data = request.form
    # add an api call for adding this object in the db
    
    return form_data
    # form_data['first_name']
    # form_data['last_name']

    

    # resume_text = form_data['resume_str']
    # jd_text = form_data['jd_str']

    # f = request.files['resume_pdf']
    # client_response = get_response(jd_text, resume=resume_text, resume_obj=f)
    # return "Success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
