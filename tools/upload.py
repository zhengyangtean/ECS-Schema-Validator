"""
Elasticsearch Data Indexing from CSV

This script connects to an Elasticsearch cluster, defines an index, 
loads data from a ECS CSV file into a Pandas DataFrame, and indexes 
the data into Elasticsearch using the specified index.

Author: [Your Name]
Date: [Date]

Usage:
    - Ensure Elasticsearch is running and accessible.
    - Modify the CSV_PATH variable to point to your CSV file.
    - Run the script to create the Elasticsearch index and 
      index the data from the CSV file.

Required Python Libraries:
    - elasticsearch: Python Elasticsearch client.
    - pandas: Data manipulation library for loading CSV data.

Assumptions:
    - The Elasticsearch cluster is running at localhost:9200. 
      Modify the connection details as needed.
    - The CSV file has headers and is located at CSV_PATH.
    - The data in the CSV file corresponds to the mapping specified in index_definition.

Note: Ensure that the values in the "Field" column of the CSV file are unique, as they
will be used as document IDs in Elasticsearch.

"""

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import pandas as pd

# Path to your CSV file
CSV_PATH = 'data/fields.csv'
# index to use in elasticsearch
INDEX_NAME = "ecs_schema"

# Connect to Elasticsearch cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])


# Define the index settings and mappings
index_definition = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "ngram_filter"]
                }
            },
            "filter": {
                "ngram_filter": {
                    "type": "ngram",
                    "min_gram": 2,
                    "max_gram": 3
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "Field": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    },
                    "text": {
                        "type": "text",
                        "analyzer": "my_ngram_analyzer"
                    }
                }
            },
            "description": {
                "type": "text"
            },
            "ECS_Version": {
                "type": "keyword"
            },
            "Indexed": {
                "type": "keyword"
            },
            "Field_Set": {
                "type": "keyword"
            },
            "Type": {
                "type": "keyword"
            },
            "Level": {
                "type": "keyword"
            },
            "Normalization": {
                "type": "keyword"
            },
            "Example": {
                "type": "text"
            },
            "Description": {
                "type": "text"
            }
        }
    }
}

if es.indices.exists(index=INDEX_NAME):
    print(f"Index '{INDEX_NAME}' exists.")
else:
    print(f"Index '{INDEX_NAME}' does not exist. Creating ...")
    # Create the index with the provided settings and mappings
    es.indices.create(index=INDEX_NAME, body=index_definition)

# Load CSV data into a Pandas DataFrame and infer headers from the first row
df = pd.read_csv(CSV_PATH, header=0)
df = df.fillna("")

# Index data from the DataFrame into Elasticsearch
def index_data_from_dataframe(dataframe):
    """
    Index data from the Pandas DataFrame into Elasticsearch.

    This function takes a Pandas DataFrame as input and indexes its data 
    into Elasticsearch. Each row in the DataFrame corresponds to a document to be 
    indexed. The function iterates over the rows, converts each row into a dictionary 
    (document), and indexes it into Elasticsearch using the specified index.

    Parameters:
        dataframe (pandas.DataFrame): The Pandas DataFrame containing the data to be 
        indexed.

    Returns:
        None

    Raises:
        Exception: If there is an error during the indexing process, an exception is 
                   raised. The document causing the error and the details of the 
                   error are printed.

    Note:
        - The Elasticsearch index to which the data will be indexed should be specified 
          globally as INDEX_NAME before calling this function.
        - The "Field" column in the DataFrame is used as the document ID in 
          Elasticsearch, so it should have unique values.

    Example:
        # Assuming the DataFrame df contains the data to be indexed and INDEX_NAME is 
          defined
        # as the Elasticsearch index name:
        index_data_from_dataframe(df)

    """
    for _, row in dataframe.iterrows():
        document = row.to_dict()
        try:
            es.index(index=INDEX_NAME, body=document, id=document["Field"])
        except RequestError as err:
            print("Error indexing document: ", document)
            print("Error details: ", err)

# Call the function to index data from the DataFrame
index_data_from_dataframe(df)

es.indices.refresh(index=INDEX_NAME)
