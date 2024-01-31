import streamlit as st
#from streamlit import session_state
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import bcrypt
import base64

st.set_page_config(
        page_title="IoT Power Saver",
        page_icon="💡",
    )
# Initialize st.session_state if it doesn't exist
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None
#st.rerun()

# -- USER AUTHENTICATION --
password1 = "Bhav123"
password2 = "Such123"

#names = {"user1": "Bhavadev", "user2": "Suchir"}
#usernames = {"user1": "Bhav", "user2": "Such"}
hashed_password1 = bcrypt.hashpw(password1.encode("utf-8"), bcrypt.gensalt())
hashed_password2 = bcrypt.hashpw(password2.encode("utf-8"), bcrypt.gensalt())
#hashed_password_dict = {"user1": "hashed_password1", "user2": "hashed_password2"}
#hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
        "usernames":{
            "Bhav":{
                "name":"Bhavadev",
                "password":"$2b$12$C7Na1nAvLrCZPmvb8lT9s.4s6dF3wHV50p9xBH8UEUjSzjsOsM4nW"
                },
            "Such":{
                "name":"Suchir",
                "password":"$2b$12$j13TEhBOAVjjsu9L5lSDv.YwKsIz07okKxEEXA6EV7twmVcK9KZeC"
                }            
            }
        }
#Authentication Object
authenticator = stauth.Authenticate(credentials, "IoT_Power_Saver","auth", cookie_expiry_days=30)

print("authentication_status before login:", st.session_state.authentication_status)
name, authentication_status, username = authenticator.login("Login", "main")
print("authentication_status after login:", st.session_state.authentication_status)

if authentication_status is True:
    #Text part in the app
    st.write("# Welcome to The Power Saver! 💡")

    file_ = open("smart-home.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    
    #st.markdown("![Smart Home](https://www.google.com/url?sa=i&url=https%3A%2F%2Fdribbble.com%2Fshots%2F6420054-Smart-Home&psig=AOvVaw02Kn8KJBpVrWPA0bztJW8u&ust=1703299406792000&source=images&cd=vfe&opi=89978449&ved=0CA8QjRxqFwoTCNC0wfSCooMDFQAAAAAdAAAAABAD)")
    
    
    st.markdown(
            """
        A smart system for a smart future!


        ### This app fetaures the data collected from our Electric Current Sensor and a Dynamic Electricity Bill Calculator.
        ---

        """
        )
    # Create the SQL connection as specified in your secrets file.
    conn = st.connection("mysql", type='sql')
    # Perform query.
    df = conn.query('SELECT * from mytable;', ttl = 600)

    df['Time'] = df['Time'].astype(str)

    # Query and display the data you inserted
    st.dataframe(df)

    st.markdown(
            """
            
        # Price Calculator 💸
        - We calculate the prices per KWh of usage and display the price in the country's local currency
        """
        )

    #Displaying Cost Data.
    df_2 = conn.query('SELECT * FROM electricity_cost;', ttl = 600)
    st.dataframe(df_2)

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.markdown(
        """

        My GitHub 😊 [Aaryan's GitHuB](https://github.com/AaryanTheLaughingGas)
"""
    )
else:
    if authentication_status is False:
        st.error("Username/ password is incorrect")
    else:
        st.warning("Please enter your Username and password to proceed")
