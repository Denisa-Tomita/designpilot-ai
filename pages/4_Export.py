import streamlit as st
from tools.zip_exporter import build_brand_zip

st.title("📦 Export Brand Kits")

user_input = st.text_input("Enter project name")

if st.button("Generate ZIP"):

    zip_data = build_brand_zip(user_input)

    if not zip_data:
        st.error("Project not found.")
    else:
        st.success("ZIP ready!")

        st.download_button(
            label="Download Brand Kit",
            data=zip_data,
            file_name="designpilot-brand-kit.zip",
            mime="application/zip"
        )