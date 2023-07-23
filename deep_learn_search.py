
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from transformers import pipeline
import torch
import cloudpickle as pickle 
import codecs
from transformers import RobertaTokenizer, T5ForConditionalGeneration

model = pipeline(
    model="Lazyhope/RepoSim",
    trust_remote_code=True,
    device_map="auto")

def encode(string):
    with torch.no_grad():
        embedding = model.encode(string, 512)
    return embedding.squeeze().cpu()

#CODE SUMMARIZATION
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
summary_model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')

def generate_summary(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    generated_ids = summary_model.generate(input_ids, max_length=20)
    summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return summary


#SEARCH 
def similarity_search(user_query,all_pes,type):

    #format all PEs response 
    all_pes_df = pd.json_normalize(all_pes)
   
    #query embedding 
    user_query_docs_emb = encode(user_query)

    # Compute cosine similarity
    user_query_emb = np.array(user_query_docs_emb)

    if type == "text":
        embed_type = 'descEmbedding'
    else:
        embed_type = 'codeEmbedding'

    # Apply conversion to the column
    all_pes_df[embed_type] = all_pes_df[embed_type].apply(lambda x: torch.tensor(list(map(float, x[1:-1].split()))))
    cos_similarities = cosine_similarity(user_query_emb.reshape(1, -1), np.vstack(all_pes_df[embed_type]))  

    # Add cosine similarity scores as a new column              
    all_pes_df_copy = all_pes_df.copy()
    all_pes_df_copy["cosine_similarity"] = cos_similarities[0]

    # Sort the dataframe based on cosine similarity
    sorted_df = all_pes_df_copy.sort_values(by="cosine_similarity", ascending=False)

    # Retrieve the top 5 most similar documents
    top_5_similar_docs = sorted_df.head(5)

    selected_columns = ['peId', 'peName','description','cosine_similarity']
    print(top_5_similar_docs[selected_columns])

    #Retrieve code column 
    obj_list = top_5_similar_docs["peCode"].apply(lambda x: pickle.loads(codecs.decode(x.encode(), "base64"))).tolist()

    return obj_list
