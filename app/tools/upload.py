from elasticsearch import Elasticsearch
import pandas as pd

index_name = "ecs_schema"

# Connect to Elasticsearch cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

if es.indices.exists(index=index_name):
    print(f"Index '{index_name}' exists.")
else:
    print(f"Index '{index_name}' does not exist.")

# Path to your CSV file
csv_file_path = '../data/fields.csv'

# Load CSV data into a Pandas DataFrame and infer headers from the first row
df = pd.read_csv(csv_file_path, header=0)
df = df.fillna("") 

print(df.head()) 

# Index data from the DataFrame into Elasticsearch
def index_data_from_dataframe(dataframe, index_name):
    for _, row in dataframe.iterrows():
        document = row.to_dict()
        try:
            es.index(index=index_name, body=document)
        except Exception as e:
            print("Error indexing document: ", document)
            print("Error details: ", e)

# Call the function to index data from the DataFrame
index_data_from_dataframe(df, index_name)

es.indices.refresh(index=index_name)