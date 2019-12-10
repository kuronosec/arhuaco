# Copyright (c) 2019 Andres Gomez Ramirez.
# All Rights Reserved.

import logging
import socket

from flask import Flask
from flask import request,jsonify
from arhuaco.analysis.arhuaco_analysis import ArhuacoAnalysis
from arhuaco.response.arhuaco_response import ArhuacoResponse

import tensorflow as tf
from keras import backend as K

# Model objects for Flask
graph = None
session = None
arhuaco_analysis = None
arhuaco_response = None
app = Flask(__name__)

@app.route("/apply", methods=['GET'])
def predict():
    src_ip = request.args.get('src')
    # src_port = request.args.get('srcport')
    dst_ip = request.args.get('dst')
    # dst_port = request.args.get('dstport')
    global arhuaco_analysis
    global arhuaco_response
    global graph
    global session
    response = None
    with graph.as_default():
        K.set_session(session)
        result = arhuaco_analysis.model.predict(src_ip+" "+dst_ip)
        response = arhuaco_response.\
                   process_result(result)
    logging.info(response)
    logging.info(src_ip+" "+dst_ip)
    r = {}
    r['is_malicious'] = response
    return jsonify(r)

def start_analysis():
    # Create objects
    if K.backend() == "tensorflow":
        global graph
        graph = tf.Graph()
        with tf.Session(graph = graph) as sess:
            global arhuaco_analysis
            global arhuaco_response
            global session
            session = sess
            arhuaco_analysis = ArhuacoAnalysis(None, None)
            arhuaco_analysis.create_analysis_model("network")
            arhuaco_response = ArhuacoResponse(None)
            start_rest_service()
    else:
        rest_model = ArhuacoAnalysis(None, None).model
        arhuaco_response = ArhuacoResponse(None)
        arhuaco_analysis.create_analysis_model("network")
        start_rest_service()

def start_rest_service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 4444))
    port = sock.getsockname()[1]
    sock.close()
    logging.info("Running web app.")
    app.run(threaded=True, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_analysis()
