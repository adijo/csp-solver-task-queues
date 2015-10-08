from flask import Flask, jsonify
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, make_response
import redis
from celery import Celery
import json
import unicodedata
from csp_celery import process
import time
from utils import redis_result_prefix, redis_retry_prefix

app = Flask(__name__)
REDIS = redis.Redis("localhost")
MAX_RETRIES = 50

def transform_graph(graph):
    new_graph = []
    for key in graph:
        values = graph[key]
        for value in values:
            k, v = unicodedata.normalize('NFKD', key).encode('ascii','ignore'), unicodedata.normalize('NFKD', value).encode('ascii','ignore')
            new_graph.append((k, v))
    return new_graph


@app.route('/solver', methods = ["GET"])
def solver():
    graph = request.args.get("graph")
    variables = request.args.get("variables")
    domains = request.args.get("domains")
    unary = request.args.get("unary")
    graph = json.loads(graph)
    new_graph = transform_graph(graph)
    variables = json.loads(variables)
    domains = json.loads(domains)
    variables = map(lambda x : unicodedata.normalize('NFKD', x).encode('ascii','ignore'), variables)
    # do the same for unary, ignore unary for now. keep dummy values for now.
    unary = {x : set() for x in variables}
    job_id = round(time.time(), 2)
    print redis_result_prefix(job_id)
    REDIS.set(redis_result_prefix(job_id), "IN_PROGRESS")
    process.delay(new_graph, variables, domains, unary, job_id)
    return json.dumps({"status" : "ok", "job_id" : job_id})


@app.route('/poll', methods = ["GET"])
def poll():
    request_ip = request.remote_addr
    key = redis_retry_prefix(request_ip)
    times = REDIS.get(key)
    if times != None and int(times) > MAX_RETRIES:
        return json.dumps({"error" : "true", "error_message" : "Exceeded retries. Please try again in 10 minutes."})
    else:
        if times == None:
            REDIS.setex(key, 0, 600)
        REDIS.incr(key)
        job_id = request.args.get("job_id")
        res_key = redis_result_prefix(job_id)
        print res_key
        result = REDIS.get(res_key)
        if result == "IN_PROGRESS":
            return json.dumps({"error" : "false", "error_message" : None, "result" : "IN_PROGRESS"})
        elif result == None:
            return json.dumps({"error" : "true", "error_message" : "No such job_id.", "result" : None})
        else:
            return json.dumps({"error" : "false", "error_message" : None, "result" : result})

if __name__ == '__main__':
    app.run()