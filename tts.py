import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime as dt

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.experimental_memo to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

#Pulling number of matches won by a player against an opponent from database
charanVandreas = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Andreas'")
andreasVcharan = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Andreas'")
charanVtobias = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Tobias'")
tobiasVcharan = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Tobias'")
andreasVtobias = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Andreas' AND opponent = 'Tobias'")
tobiasVandreas = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Andreas' AND opponent = 'Tobias'")

#Calculaing total number of matches played between the pairs
ca_matches = charanVandreas + andreasVcharan
ct_matches = charanVtobias + tobiasVcharan
at_matches = andreasVtobias + tobiasVandreas

# Print results.
st.title('Scoreboard')

col1, col2 = st.columns(2)

with col1:
    st.header("Charan/Andreas")
    c1 = st.container()
    scol1, scol2 = st.columns(2)
    c1.scol1.metric("Charan", charanVandreas, (charanVandreas-andreasVcharan))
    c1.scol2.metric("Andreas", andreasVcharan, (andreasVcharan-charanVandreas))

    st.header("Charan/Tobias")
    c2 = st.container();
    ccol1, ccol2 = st.columns(2)
    c2.ccol1.metric("Charan", charanVtobias, (charanVtobias-tobiasVcharan))
    c2.ccol2.metric("Tobias", tobiasVcharan, (tobiasVcharan-charanVtobias))

with col2:
    st.header("Andreas/Tobias")
    c1 = st.container()
    scol1, scol2 = st.columns(2)
    c1.scol1.metric("Andreas", andreasVtobias, (andreasVtobias-tobiasVandreas))
    c1.scol2.metric("Tobias", tobiasVandreas, (tobiasVandreas-andreasVtobias))

