import streamlit as st
from indexing import IndexingGoogle


def main():
    st.title('Google Indexing')

    # JSON credentials file upload
    credentials_file = st.file_uploader('Upload JSON credentials file')

    # URL list input
    url_list = st.text_area('Enter URLs to be indexed, separated by a new line')

    # Define a radio button to allow user to choose between "URL_UPDATED" and "URL_DELETED"
    option = st.radio('Choose an option:', ('URL_UPDATED', 'URL_DELETED'))

    # Send URLs button
    if st.button('Send URLs'):
        urls = url_list.strip().split('\n') if url_list.strip() else []
        indexing_google = IndexingGoogle()

        if credentials_file:
            credentials = credentials_file.read().decode('utf-8-sig')
            if credentials:
                indexing_google.set_credentials(credentials)
                result = indexing_google.send_urls(urls, option)
                st.write(result)
            else:
                st.write('Error: Credentials file is empty')
        else:
            st.write('Error: No credentials file uploaded')


if __name__ == '__main__':
    main()