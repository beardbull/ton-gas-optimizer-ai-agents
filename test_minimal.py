import streamlit as st
st.set_page_config(page_title="TEST", layout="wide")
st.title("✅ MINIMAL WORKS")
st.write("Если видишь это — Streamlit исправен!")
if st.button("Click"): st.success("Button works!")
