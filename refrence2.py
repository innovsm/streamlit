import streamlit as st
import time
import numpy as np
import pandas as pd
# using cache function

@st.cache(allow_output_mutation=False)

def return_frame():
    data_1 = pd.DataFrame(np.random.rand(1000,3),columns= ['a','b','c'])
    return data_1

a1 = time()
st.write(return_frame())
a2 = time()
print(a2- a1)
