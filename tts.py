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
ca = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Andreas'")
ac = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Andreas'")
ct = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Tobias'")
tc = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Charan' AND opponent = 'Tobias'")
at = run_query("SELECT SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Andreas' AND opponent = 'Tobias'")
ta = run_query("SELECT SUM(matches)-SUM(won) FROM `bumblebee-233720.tt_data.tt_matches` WHERE player = 'Andreas' AND opponent = 'Tobias'")

for row in ca:
    charanVandreas = int(row['f0_'])
for row in ac:
    andreasVcharan = int(row['f0_'])
for row in ct:
    charanVtobias = int(row['f0_'])
for row in tc:
    tobiasVcharan = int(row['f0_'])
for row in at:
    andreasVtobias = int(row['f0_'])
for row in ta:
    tobiasVandreas = int(row['f0_'])

#Calculaing total number of matches played between the pairs
ca_matches = charanVandreas + andreasVcharan
ct_matches = charanVtobias + tobiasVcharan
at_matches = andreasVtobias + tobiasVandreas

# Print results.
st.title('Scoreboard')

st.header("Charan/Andreas")
scol1, scol2 = st.columns(2)
scol1.metric("Charan", charanVandreas, (charanVandreas-andreasVcharan))
scol2.metric("Andreas", andreasVcharan, (andreasVcharan-charanVandreas))

st.header("Charan/Tobias")
ccol1, ccol2 = st.columns(2)
ccol1.metric("Charan", charanVtobias, (charanVtobias-tobiasVcharan))
ccol2.metric("Tobias", tobiasVcharan, (tobiasVcharan-charanVtobias))

st.header("Andreas/Tobias")
c1 = st.container()
scol1, scol2 = st.columns(2)
scol1.metric("Andreas", andreasVtobias, (andreasVtobias-tobiasVandreas))
scol2.metric("Tobias", tobiasVandreas, (tobiasVandreas-andreasVtobias))

