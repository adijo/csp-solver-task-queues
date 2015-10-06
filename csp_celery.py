from celery import Celery
from csp_solver import CSPSolver
import redis
from utils import redis_result_prefix

app = Celery('celery_blog', broker='redis://localhost:6379/0')
SOLVER = CSPSolver()
REDIS = redis.Redis("localhost")
EXPIRE = 10 * 60

@app.task
def process(graph, variables, domains, unary, job_id):
    res = SOLVER.solve(graph, variables, domains, unary)
    # log results for checking.
    print redis_result_prefix(job_id)
    REDIS.setex(redis_result_prefix(job_id), str(res), EXPIRE)

