from elasticsearch import Elasticsearch
import pandas as pd

index_name = "ecs_schema"

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

if es.indices.exists(index=index_name):
    print(f"Index '{index_name}' exists.")
else:
    print(f"Index '{index_name}' does not exist. Creating ...")
    # Create the index with the provided settings and mappings
    es.indices.create(index=index_name, body=index_definition)

# Path to your CSV file
csv_file_path = 'data/fields.csv'

# Load CSV data into a Pandas DataFrame and infer headers from the first row
df = pd.read_csv(csv_file_path, header=0)
df = df.fillna("")

# Index data from the DataFrame into Elasticsearch
def index_data_from_dataframe(dataframe, index_name):
    for _, row in dataframe.iterrows():
        document = row.to_dict()
        try:
            es.index(index=index_name, body=document, id=document["Field"])
        except Exception as err:
            print("Error indexing document: ", document)
            print("Error details: ", err)

# Call the function to index data from the DataFrame
index_data_from_dataframe(df, index_name)

es.indices.refresh(index=index_name)
