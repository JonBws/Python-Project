import random
import string
import streamlit as st

def generate_password(min_length, numbers=True, special_char=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation
    
    ## its always contain letter in our password
    characters = letters
    if numbers:
        characters += digits
    if special_char:
        characters += special
        
    pwd=""
    meets_criteria = False
    has_number = False
    has_special = False
    
    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char
        
        if new_char in digits:
            has_number=True
        elif new_char in special:
            has_special=True
            
        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_char:
            meets_criteria = meets_criteria and has_special
    return pwd

# min_length = int(input('Masukan jumlah minimum password: '))
# has_number = input('apakah kamu ingin angka dalam password(y/n) ?').lower() == 'y'   
# has_special = input('apakah kamu ingin karakter spesial dalam password (y/n) ?').lower() == 'y'

st.header(':key: Generate Your Own Password :key:')
min_length = st.number_input('Jumlah minimal password yang akan dibuat:', min_value=1, max_value=25)

if st.radio(label='Apakah password ingin memiliki angka ?', options=['Yes', 'No']) == 'Yes':
    numbers = True
else:
    numbers = False
    
if st.radio(label='Apakah password ingin memiliki karakter spesial ?', options=['Yes', 'No']) == 'Yes':
   special_char = True
else:
    special_char = False
    
if st.button('Generate'):
   password = generate_password(min_length,numbers,special_char)
   st.write(password)
