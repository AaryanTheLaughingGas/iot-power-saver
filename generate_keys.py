import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Bhavadev", "Suchir"]
usernames = ["Bhav", "Such"]
passwords = ["Bhav123","Such123"]

#Uses bcrypt to hash passwords
hashed_passwords = stauth.Hasher(passwords).generate()

#Create file in same working directory
file_path = Path(__file__).parent / "hashed_pw.pkl"

#Open file and dump the passwords into it
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
