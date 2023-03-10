import streamlit as st
import time
st.title('How to layout your Streamlit app')

with st.expander('About this app'):
  st.write('This app shows the various ways on how you can layout your Streamlit app.')
  st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

with st.sidebar.header('Input'):
  username = st.sidebar.text_area("text_area")

col1 , col2, col2 = st.columns(3)

with col1:
  if(username != ""):
    st.write(username)
  
# working with progress - bar

# working with select slider 
st.subheader("select slider")

select_slider = st.select_slider("select slider",['0', "25", "75", "100"])

if(select_slider is not None):
  my_bar = st.progress(0)
  for i in range(int(select_slider)):
    time.sleep(.05)
    my_bar.progress(i + 1)



# ----------  refrence - 2 ------------------

"""
@st.cache(allow_output_mutation=False)

def return_frame():
    data_1 = pd.DataFrame(np.random.rand(1000,3),columns= ['a','b','c'])
    return data_1

a1 = time.time()
st.write(return_frame())
a2 = time.time()
print("process - 1 {}".format(a2 - a1))

# the below function do not use st.cache [facility]
def return_frame_2():
    data_2 = pd.DataFrame(np.random.rand(1000,3), columns=['e', 'f', 'g'])
    return data_2
a3 = time.time()
st.write(return_frame_2())
a4 = time.time()
print("process-2 {}".format(a4 - a3))
"""