# Constraint Satisfaction Problem Solver With Arc Consistency as a REST Service with Task Queues.

An implementation of a REST based CSP solver implemented with arc-consistency. 
The requests are handled by a task-queue called Celery with Redis as the 
message broker to enable asynchronous computation.

# System overview
![](https://github.com/adijo/csp-solver-task-queues/blob/master/images/csp.png)

# Installation

* Clone the repository.

```
git clone https://github.com/adijo/csp-solver-task-queues.git
``` 

* Enter the repository.

```
cd csp-solver-task-queues
```

* Install the python dependencies.

```
pip install -r requirements.txt
```

* Have `redis` installed.

# Setup

* Start the `redis` server.

```
redis-server
```

* Start the `celery` workers.

```
celery worker -A csp_celery -l info -c 5
```

* Start the python app.
```
python app.py
```

* The app will be deployed on port 5000 by default. REST requests can be sent through a client such as Postman
or using the `curl` command on the console.

# Examples.
* Sample REST request after app deployement. Sent through Postman.

```
127.0.0.1:5000/solver?graph={"a" : ["b"]}&variables=["a", "b", "c", "d"]&domains=[0, 1, 2]&unary={}
```

* Sample response:
```
{"status": "ok", "job_id": 1444331048.93}
```

* Sample poll request:

```
127.0.0.1:5000/poll?job_id=1444331048.93
```

* Sample poll response:

```
{"error_message": null, "result": "(True, {'a': 1, 'c': 0, 'b': 0, 'd': 0})", "error": "false"}
```








