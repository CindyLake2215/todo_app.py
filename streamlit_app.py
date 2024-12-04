import streamlit as st
import time
from datetime import timedelta
from streamlit_autorefresh import st_autorefresh

# Function to format seconds into HH:MM:SS
def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = []
if 'active_book_index' not in st.session_state:
    st.session_state.active_book_index = None
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

st.title("Book Logging Timer")

# Auto-refresh every second to update live timers
st_autorefresh(interval=1000, key="timer_refresh")

# Book entry form
with st.form("book_form", clear_on_submit=True):
    title = st.text_input("Book Title")
    est_hours = st.number_input("Estimated Hours", min_value=0, step=1, value=0)
    est_minutes = st.number_input("Estimated Minutes", min_value=0, max_value=59, step=1, value=0)
    est_seconds = st.number_input("Estimated Seconds", min_value=0, max_value=59, step=1, value=0)
    submitted = st.form_submit_button("Add Book")
    if submitted and title:
        estimated_time = est_hours * 3600 + est_minutes * 60 + est_seconds
        st.session_state.books.append({
            'title': title,
            'estimated_time': estimated_time,
            'actual_time': 0,
            'is_reading': False
        })
        st.success(f"Added '{title}' with an estimated reading time of {format_time(estimated_time)}.")

# Display list of books
for index, book in enumerate(st.session_state.books):
    st.subheader(f"{book['title']}")
    col1, col2, col3, col4 = st.columns(4)
    
    # Edit estimated time
    with col1:
        est_hours = st.number_input(
            "Hours",
            min_value=0,
            step=1,
            value=book['estimated_time'] // 3600,
            key=f"est_hours_{index}"
        )
        est_minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            step=1,
            value=(book['estimated_time'] % 3600) // 60,
            key=f"est_minutes_{index}"
        )
        est_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            step=1,
            value=book['estimated_time'] % 60,
            key=f"est_seconds_{index}"
        )
        st.session_state.books[index]['estimated_time'] = est_hours * 3600 + est_minutes * 60 + est_seconds
    
    # Start/Stop button
    if not book['is_reading']:
        if col2.button("Start Reading", key=f"start_{index}"):
            if st.session_state.active_book_index is not None:
                st.warning("Please stop the current reading session before starting a new one.")
            else:
                st.session_state.books[index]['is_reading'] = True
                st.session_state.active_book_index = index
                st.session_state.timer_start = time.time()
    else:
        if col2.button("Stop Reading", key=f"stop_{index}"):
            st.session_state.books[index]['is_reading'] = False
            st.session_state.books[index]['actual_time'] += time.time() - st.session_state.timer_start
            st.session_state.active_book_index = None
            st.session_state.timer_start = None
    
    # Display actual reading time
    if book['is_reading']:
        elapsed_time = time.time() - st.session_state.timer_start + book['actual_time']
    else:
        elapsed_time = book['actual_time']
    col3.write(f"Actual Reading Time: {format_time(elapsed_time)}")
    
    # Placeholder for live timer
    if book['is_reading']:
        col4.write(f"Live Time: {format_time(time.time() - st.session_state.timer_start + book['actual_time'])}")

# Summary of all books
st.subheader("Summary")
for book in st.session_state.books:
    st.write(f"**{book['title']}** - Estimated: {format_time(book['estimated_time'])}, Actual: {format_time(book['actual_time'])}")
