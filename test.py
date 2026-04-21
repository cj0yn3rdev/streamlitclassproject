import streamlit as st 
import matplotlib as plt 
import pandas as pd 

st.title("hello world")
st.header("this is streamlit")
st.subheader("you will be able to start creating things") 
st.text("this is how you will create your porject") 
st.code(" a = 123\n"\
        "import pandas \n"\
            "plt.show()")

st.markdown("---")
st.header("lets display some data") 
df = pd.read_csv("https://raw.githubusercontent.com/ArtMarciano/datasets/refs/heads/main/tips.csv")
st.dataframe(df)

st.slider("Filter by tip amount", min_valie = 0.0, max_value = 15)

tip_range = st.sidebar.slider("Filter by tup amount", )

filtered_df = df[df['tip'] <= tip_range] 
st.write(f'Showing {len(filtered_df)} rows')
st.dataframe(filtered_df)

days = st.sidebar.selectbix('Day of the week', ('All', 'Thur', ))

fig, ax = plt.subplots()
ax.hist(filtered_df['tip'], bins = 15, color = 'steelblue', alpha = 0.7)
ax.set_xlabel('Tip amount ($)')
ax.set_ylabel('Count')
ax.set_title('Distributiuon  of tips')
st.pyplot(fig)

st.markdown("---") 
st.subheader('Summary') 

col1, col2, col3 = st.columns(3)
col1.metric(label = 'Total rows', value = len(filtered_df)) 
col2.metric(label='Avg Tip', value =f'${filtered_df['tip'].mean():.2f}') 
col3.metric(label = 'Avg Bill', value = f'{filtered_df['total_bill'].mean():.2f}') 

chart_col1, chart_col2 = st.columns(2)

with chart_col1: 
    st.write('tip distribution')
    fig1, ax1 = plt.subplot()
    ax1.hist(filtered_df['tip'], bins = 15, color = 'blue', alpha = 0.7)
    ax1.set_xlabel('Tip ($)')
    st.pyplot(fig1)
with chart_col2: 
    st.write('bill distribution')
    fig1, ax1 = plt.subplot()
    ax1.hist(filtered_df['total_bill'], bins = 15, color = 'tomato', alpha = 0.7)
    ax1.set_xlabel('total_bill ($)')
    st.pyplot(fig1)