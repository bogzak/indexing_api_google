import streamlit as st
from indexing import IndexingGoogle

def main():
    st.title("Google Indexing")

    # JSON credentials file upload
    credentials_file = st.file_uploader("Upload JSON credentials file")

    # URL list input
    url_list = st.text_area("Enter URLs to be indexed, separated by a new line")

    # Send URLs button
    if st.button("Send URLs for indexing"):
        urls = url_list.strip().split("\n") if url_list.strip() else []
        indexing_google = IndexingGoogle()

        if credentials_file:
            credentials = credentials_file.read()
            indexing_google.set_credentials(credentials)
            result = indexing_google.send_urls(urls)
            st.write(result)
        else:
            st.write("Error: No credentials file uploaded")


if __name__ == "__main__":
    main()