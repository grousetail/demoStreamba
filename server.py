from flask import Flask, request
app = Flask(__name__)
import predict


@app.route('/', methods=['POST'])
def run_post_analysis():
    result=predict.post_analysis(request.form["url"])
    return result