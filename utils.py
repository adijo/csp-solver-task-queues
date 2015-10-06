"""
Helper file for functions that
help to build redis keys.
"""

def redis_result_prefix(job_id):
	return str(job_id) + ":" + "res"

def redis_retry_prefix(ip):
	return str(ip) + ":" + "tries"