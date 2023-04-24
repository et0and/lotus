import requests
import streamlit as st
import pyqrcode

st.set_page_config(
    page_title="Lotus",
    page_icon="https://example.com/image.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "mailto:support@example.com",
        'About': "Powered by estuary.tech"
    }
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Create a file input widget
file = st.file_uploader('Upload a file')

# Create a button to submit the file
if st.button('Submit'):

    # Check if a file was uploaded
    if file is not None:

        # Set up the API endpoint
        url = "https://api.estuary.tech/content/add"

        # Set up the request headers
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer process.env.ESTUARY_API_KEY'
        }

        # Send the file as data
        files = {'data': ('file', file.read(), 'application/octet-stream')}
        response = requests.post(url, headers=headers, files=files)

        # Get the CID from the response
        cid = response.json().get('cid')

        # Append the CID to the IPFS URL
        ipfs_url = f"https://cloudflare-ipfs.com/ipfs/{cid}"

        # Generate the QR code
        qr = pyqrcode.create(ipfs_url)

        # Save the QR code as an image
        with open('qr.png', 'wb') as f:
            qr.png(f, scale=8)

        # Display the IPFS URL and QR code
        st.write(ipfs_url)
        st.image('qr.png')

    else:
        st.write('No file selected')
