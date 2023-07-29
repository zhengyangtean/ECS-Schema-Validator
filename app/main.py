"""
ECS Search API

This module contains a FastAPI application that provides an API endpoint for 
performing search in the elastic common schema (ECS) 

Usage:
    - Perform a search using the API endpoint:
        ```
        GET http://<host>:<port>/field-query?field=geo
        ```
"""

from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch("http://0.0.0.0:9200")

@app.get("/")
async def homepage_documentation():
    """
    Homepage : Documentation

    This endpoint allows you to view all APIs of this service and how to use it

    URL: /
    Method: GET

    Returns:
        HttpResponse: OpenAPI based documentation of the APIs for this service
    """
    return RedirectResponse(url='/docs')

@app.get("/field-query")
def query_ecs_field(field: Union[str, None] = None):
    """
    Perform a search in the 'ecs_schema' index using a simple query string.

    This endpoint allows you to search for the specified text in the 'Field.text',
    'Description', and 'Example' fields of the 'ecs_schema' index using the 
    Elasticsearch `simple_query_string` query.

    Parameters:
        field (str, optional): The text to search for. If provided, the search will be 
        based on this value. If not provided (None), the search will return all 
        documents in the index. Defaults to None.

    Returns:
        List[dict]: A list of JSON objects representing the search results. 
        Each JSON object (hit) corresponds to a matching document in the 'ecs_schema' 
        index.

        If there are no search results, an empty list will be returned.

    Raises:
        HTTPException (status_code 500): If there is an issue with the Elasticsearch 
        search or an error occurs during the search.

    Examples:
        To search for the term "geo" in the specified fields:
        ```
        GET /field-query?field=geo
        ```
    """
    query = {
        "query": {
            "simple_query_string": {  
                "fields": ["Field.text", "Description", "Example"],          
                "query":  field,
                "analyze_wildcard": True
            }
        }
    }
    result = es.search( index='ecs_schema', body=query)
    if "hits" in result and "total" in result["hits"]:
        if result["hits"]["total"]["value"] > 0:
            return result["hits"]["hits"]
        else:
            result = []
    else:
        result = []
    return result
