import streamlit as st

st.title("💰 AI Personal Finance Assistant")

st.write("Upload a payment screenshot to begin.")

uploaded_file = st.file_uploader(
    "Upload Payment Screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")