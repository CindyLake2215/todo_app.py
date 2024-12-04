import streamlit as st
import time

st.title("Lap Timer")

# Initialize session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
    st.session_state.lap_times = []

# Start Timer Button
if st.button("Start Timer"):
    st.session_state.start_time = time.time()

# Record Lap Button
if st.button("Lap"):
    if st.session_state.start_time:
        lap_time = time.time() - st.session_state.start_time
        st.session_state.lap_times.append(lap_time)

# Reset Timer Button
if st.button("Reset"):
    st.session_state.start_time = None
    st.session_state.lap_times = []

# Display Lap Times
st.write("Lap Times:")
for idx, lap in enumerate(st.session_state.lap_times, start=1):
    st.write(f"Lap {idx}: {lap:.2f} seconds")
