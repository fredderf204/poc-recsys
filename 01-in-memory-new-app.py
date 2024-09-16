import os
import pandas as pd
import numpy as np
import tiktoken
from openai import AzureOpenAI

# Environment variables
aoai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
aoai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
embed_model = "text-embedding-ada-002" # model = "deployment_name" in AOAI
chat_model = "gpt-4o" # model = "deployment_name" in AOAI

# Load the data into a dataframe and give each column a data type
# 100 line CSV
df_products=pd.read_csv(os.path.join(os.getcwd(),'./data/test-recsys-data-100.csv'),dtype={'CompanyName':str,'State':str,'Industry':str,'Segment':str,'Product 1 Name':str,'Product 1 Performance':float,'Product 2 Name':str,'Product 2 Performance':float,'Product 3 Name':str,'Product 3 Performance':float,'Product 4 Name':str,'Product 4 Performance':float,'Product 5 Name':str,'Product 5 Performance':float,'Product 6 Name':str,'Product 6 Performance':float,'Product 7 Name':str,'Product 7 Performance':float,'Product 8 Name':str,'Product 8 Performance':float}) 

###########################
### Prepare the data ###
###########################
# Create a json column and a comb column
# 100 line CSV
cols=['CompanyName','State','Industry','Segment','Product 1 Name','Product 1 Performance','Product 2 Name','Product 2 Performance','Product 3 Name','Product 3 Performance','Product 4 Name','Product 4 Performance','Product 5 Name','Product 5 Performance','Product 6 Name','Product 6 Performance','Product 7 Name','Product 7 Performance','Product 8 Name','Product 8 Performance']
df_products = df_products.fillna('')
df_products['json'] = df_products.apply(lambda x: x.to_json(), axis=1)
df_products['comb'] = df_products[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

#check length of comb column
tokenizer = tiktoken.get_encoding("cl100k_base")
df_products['n_tokens'] = df_products["comb"].apply(lambda x: len(tokenizer.encode(x)))

# remove rows where token size is greater than 8192. Not really needed in this sample.
df_products = df_products[df_products.n_tokens<8192]

### Vectorise comb column ###
# create a client
vec_client = AzureOpenAI(
  api_key = aoai_api_key,  
  api_version = "2024-02-01",
  azure_endpoint = aoai_endpoint
)

def generate_embeddings(text, model=embed_model): 
    return vec_client.embeddings.create(input = [text], model=model).data[0].embedding

df_products['ada_v2'] = df_products['comb'].apply(lambda x : generate_embeddings (x, model = embed_model)) 
#print(df_products)

###########################
### Vectorise question and return top n results ###
###########################
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text, model=embed_model): 
    return vec_client.embeddings.create(input = [text], model=model).data[0].embedding

def search_docs(df, user_query, top_n=4, to_print=True):
    embedding = get_embedding(
        user_query,
        model= embed_model 
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    if to_print:
        print(res)
    return res

# test company profile. Finding better results using non JSON
test_company_profile = 'Madeup Inc NSW Finance Banking Widget W 85 Widget Y 74'

# Get top 20 results
res = search_docs(df_products, test_company_profile, top_n=20)
#print(res)

###########################
### Scope down results based on similarities and product performance ###
###########################
# First, remove any results with a similarity score of less than 0.87
res = res[res.similarities > 0.87] 
#print(res)

# change product performance columns to float
res["Product 1 Performance"] = pd.to_numeric(res["Product 1 Performance"], errors='coerce')
res["Product 2 Performance"] = pd.to_numeric(res["Product 2 Performance"], errors='coerce')
res["Product 3 Performance"] = pd.to_numeric(res["Product 3 Performance"], errors='coerce')
res["Product 4 Performance"] = pd.to_numeric(res["Product 4 Performance"], errors='coerce')
res["Product 5 Performance"] = pd.to_numeric(res["Product 5 Performance"], errors='coerce')
res["Product 6 Performance"] = pd.to_numeric(res["Product 6 Performance"], errors='coerce')
res["Product 7 Performance"] = pd.to_numeric(res["Product 7 Performance"], errors='coerce')
res["Product 8 Performance"] = pd.to_numeric(res["Product 8 Performance"], errors='coerce')
            
# find the mean of the product performance columns
res['performance'] = res[["Product 1 Performance","Product 2 Performance","Product 3 Performance","Product 4 Performance","Product 5 Performance","Product 6 Performance","Product 7 Performance","Product 8 Performance"]].mean(axis=1)

# Remove results with performance score less than 70
res = res[res.performance > 70]
#print(res)

###########################
### Take scoped down results and get AOAI to recommend the best product ###
###########################
# Loop through res and create variable from each row
comp_prof_1 = res.iloc[0]['json']
comp_prof_2 = res.iloc[1]['json']
comp_prof_3 = res.iloc[2]['json']
comp_prof_4 = res.iloc[3]['json']

### Create AOAI Client ###
chat_client = AzureOpenAI(
    api_key = aoai_api_key,  
    api_version="2024-02-01",
    azure_endpoint = aoai_endpoint
    )

# Company profile to be sent to the recommendation engine
# same as test_company_profile above
in_json = '[{"Company Name":"Madeup Inc","Aus State":"NSW","Industry":"Finance","Segment":"Banking","Product 1 Name":"Widget W","Product 1 Performance":85,"Product 2 Name":"","Product 2 Performance":"","Product 3 Name":"Widget Y","Product 3 Performance":74}]'

# Send a chat call to generate an answer
response = chat_client.chat.completions.create(
    model= chat_model,
    messages=[
        {"role": "system", "content": "You are a assistant that recommends products to companies.\n You will receive a company profile and you need to recommend the next product that the company should buy. \nBelow are some examples of similar companies and their products. Use the below to recommend the next products that the company should buy. \n\n### Example Company 1\n" + comp_prof_1 + "\n\n### Example Company 2\n" + comp_prof_2 + "\n\n### Example Company 3\n" + comp_prof_3 + "\n\n### Example Company 4\n" + comp_prof_4 + "\n\nRecommend the next one product only that the company should buy. Then on a separate line write a short concise reason why they should buy the product along with insights contained in the data."},
        {"role": "user", "content": in_json}
    ]
)

print(response.choices[0].message.content)