import streamlit as st
import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

faq_data = pd.read_csv("faq_data.csv")

def preprocess_text(text):
    tokens = word_tokenize(str(text).lower())
    stop_words = set(stopwords.words("english"))

    return " ".join(
        word for word in tokens
        if word not in stop_words
        and word not in string.punctuation
    )

faq_data["processed"] = faq_data["Question"].apply(preprocess_text)

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_data["processed"])

def get_response(user_query):
    query_vector = vectorizer.transform([preprocess_text(user_query)])
    similarities = cosine_similarity(query_vector, faq_vectors)
    best_index = similarities.argmax()
    return faq_data.iloc[best_index]["Answer"]

st.title("⚡🤖 FAQ Chatbot \n(for Banking System)")

if "question" not in st.session_state:
    st.session_state.question = ""

st.subheader("📋 FAQ Questions \n(Click a row checkbox)")

event = st.dataframe(
    faq_data[["Question"]],
    use_container_width=True, height=200,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

if event.selection.rows:
    selected_row = event.selection.rows[0]
    st.session_state.question = faq_data.iloc[selected_row]["Question"]

user_input = st.text_input(
    "❓ Ask a question",
    key="question"
)

if st.button("Get Answer"):
    if user_input.strip():
        st.success(get_response(user_input))
    else:
        st.warning("Please enter a question.")
