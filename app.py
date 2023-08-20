import streamlit as st
import io
import os
import zipfile
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

corpus = []
doc_index = []

st.title("Term frequencies from documents")

strip_accents = None
lowercase = False

stripaccents = st.checkbox('Strip accents')
lower = st.checkbox('Convert to lowercase')

if stripaccents:
    strip_accents = 'unicode'

if lower:
    lowercase = True

inp_files = st.file_uploader("Choose one or more txt-files", accept_multiple_files=True)
for inp_file in inp_files:
    stringio = io.StringIO(inp_file.getvalue().decode("utf-8"))
    # To read file as string:
    corpus.append(stringio.read())
    doc_index.append(inp_file.name)

if len(corpus) >0:

    vectorizer = CountVectorizer(lowercase=lowercase, strip_accents=strip_accents)

    X = vectorizer.fit_transform(corpus)

    df = pd.DataFrame(data=X.toarray(), columns=vectorizer.get_feature_names_out(), index=doc_index)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:  
        df.to_excel(writer, sheet_name='Term counts', index=True)

    st.download_button(
        label="Download term counts as xlsx",
        data=buffer,
        file_name='term_counts.xlsx',
        mime='application/vnd.ms-excel',
    )
