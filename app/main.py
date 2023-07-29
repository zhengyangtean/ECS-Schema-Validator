from typing import Union

from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch("http://0.0.0.0:9200")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/field-validator")
def verify_field(field: Union[str, None] = None):
    query = {    
        "query": {
            "simple_query_string": {  
                "fields": ["Field.text", "Description", "Example"],          
                "query":  field,
                "analyze_wildcard": True
            }  
        }
    }
    r = es.search( index='ecs_schema', body=query)
    if "hits" in r and "total" in r["hits"] and r["hits"]["total"]["value"] > 0:
        return r["hits"]["hits"]
    else:
        return []

