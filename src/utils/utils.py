import backoff
import functools
import openai

import numpy as np
import pandas as pd
from sklearn import metrics as m
import pdfplumber


def load_pdf(fpath):
    doc_text = []
    with pdfplumber.open(fpath) as pdf:
        for p in pdf.pages:
            doc_text.append(p.extract_text())
    return doc_text

def process_doc(doc_text):
    df = pd.DataFrame()
    df['page_text'] = doc_text
    df['ada_embedding'] = df.page_text.apply(lambda x: get_embedding_openai(x))
    return df

def find_closest(df, query):

    embedding = get_embedding_openai(query)
    
    df['similarities'] = df.ada_embedding.apply(lambda x: m.pairwise.cosine_similarity(x.reshape(1, -1), embedding.reshape(1, -1)).flatten())
    
    res = df.sort_values('similarities', ascending=False).head(2)
    return res
 

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
@functools.lru_cache(maxsize=1024) 
def get_embedding_openai(text_):
    # time.sleep(2)
    embed = openai.Embedding.create(input=text_, model='text-embedding-ada-002')
    return np.array(embed['data'][0]['embedding'])

