#!/usr/bin/python3 
from eia.utils.credentials import load_credentials
import json 
import warnings 
from functools import wraps 
import redis 
import boto3 
import os  

load_credentials() 
warnings.filterwarnings('ignore') 

secrets = boto3.client(service_name='secretsmanager',
                        region_name='us-east-1', 
                        aws_access_key_id=os.environ["DEV-KEY"],
                        aws_secret_access_key=os.environ["DEV-VAL"])

host,port = list(json.loads(secrets.get_secret_value(SecretId='redis_server').get('SecretString')).values())
r: redis = redis.StrictRedis(host=host, port=port) 

def redis_cache(app: object, ttl: int = 600):

    def decorator(func):
        @wraps(func) 
        def wrapper(*args, **kwargs): 

            cache_key: str = f"{app.current_request.uri_params}:{func.__name__}:{args}"
            cached_data = r.get(cache_key)

            if cached_data:
                return cached_data


            result = func(*args, **kwargs)
            r.set(cache_key, json.dumps(result) , ex=ttl)
            return result
    
        return wrapper

    return decorator