import nltkmodules
from flask import Flask, request, jsonify
import warnings
import jwt
from resume_gen import paraphrase_fn
from similarity_check import get_response
from generate_model import make_model
import pymongo
from dotenv import dotenv_values
from transformers import AutoModelWithLMHead, AutoTokenizer
from functools import wraps
from bson.objectid import ObjectId

warnings.filterwarnings("ignore")

model = None
tokenizer = None
global env_vars
env_vars = dotenv_values('.env')

app = Flask(__name__)

client = pymongo.MongoClient(env_vars['MongoURI'])
db = client["KCP"]


def load_model():
    global tokenizer
    global model
    tokenizer = AutoTokenizer.from_pretrained(
        "mrm8488/t5-small-finetuned-quora-for-paraphrasing")
    model = AutoModelWithLMHead.from_pretrained(
        "mrm8488/t5-small-finetuned-quora-for-paraphrasing")


# def gen_model():
#     make_model()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-auth-token' in request.headers:
            token = request.headers['x-auth-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            decoded = jwt.decode(token,
                                 env_vars['JWT_SECRET'],
                                 algorithms=['HS256'])
            current_user = db.users.find_one(
                {"_id": ObjectId(decoded['user']['id'])})
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Token is invalid !!'}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/upload", methods=['POST'])
@middleware
def uploadPDF(user):
    form_data = request.form
    resume_text = form_data['resume_str']
    jd_text = form_data['jd_str']
    f = request.files['resume_pdf']
    client_response = get_response(jd_text, resume=resume_text, resume_obj=f)
    return client_response


@app.route("/resume/paraphrase", methods=['POST'])
@middleware
def paraphrase(user):
    form_data = request.form

    p_text = form_data['p_text']
    p_out = paraphrase_fn(model, tokenizer, p_text)
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
    # gen_model()
    load_model()
    app.run(host='0.0.0.0', port=5001, debug=True)
