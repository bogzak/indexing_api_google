import streamlit as st
from indexing import IndexingGoogle


def main():
    st.title('Google Indexing')

    # JSON credentials file upload
    credentials_file = st.file_uploader('Upload JSON credentials file')

    # URL list input
    url_list = st.text_area('Enter URLs, separated by a new line')

    # map the user-friendly display values to the actual values for type
    type_mapping = {
        'Update': 'URL_UPDATED',
        'Delete': 'URL_DELETED'
    }

    # Get the user's selection from the app
    user_selection = st.selectbox('Select action', ['Update', 'Delete'])
    option = type_mapping[user_selection]

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