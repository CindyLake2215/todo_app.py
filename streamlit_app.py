import streamlit as st
import time

st.title("Book Logging Timer")

# Initialize session state for book data
if "books" not in st.session_state:
    st.session_state.books = []  # A list of dictionaries, each representing a book
if "current_book" not in st.session_state:
    st.session_state.current_book = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# Input for book details
with st.form("book_form", clear_on_submit=True):
    title = st.text_input("Enter Book Title")
    estimated_time = st.number_input(
        "Estimated Reading Time (in minutes)", min_value=0, step=1
    )
    submitted = st.form_submit_button("Add Book")

    if submitted and title:
        st.session_state.books.append(
            {
                "title": title,
                "estimated_time": estimated_time,
                "actual_time": None,
                "start_time": None,
                "elapsed_time": 0,
            }
        )
        st.success(f"Book '{title}' added!")

# Display the list of books and allow tracking
if st.session_state.books:
    st.subheader("Books Logged")
    for idx, book in enumerate(st.session_state.books):
        st.markdown(f"**{book['title']}**")
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        # Edit Estimated Time
        new_estimated_time = col1.number_input(
            f"Edit Estimated Time for '{book['title']}' (min)",
            value=book["estimated_time"],
            key=f"edit_time_{idx}",
        )
        book["estimated_time"] = new_estimated_time

        # Start Timer Button
        if col2.button(f"Start Timer", key=f"start_{idx}"):
            st.session_state.start_time = time.time()
            book["start_time"] = time.time()

        # Stop Timer Button
        if col3.button(f"Stop Timer", key=f"stop_{idx}"):
            if book["start_time"]:
                elapsed_time = time.time() - book["start_time"]
                book["elapsed_time"] += elapsed_time
                book["start_time"] = None
            st.session_state.start_time = None

        # Display Elapsed Time
        col4.write(
            f"Actual Time: {book['elapsed_time'] / 60:.2f} min"
            if book["elapsed_time"]
            else "Not Started"
        )

    st.subheader("Summary")
    for idx, book in enumerate(st.session_state.books):
        st.write(
            f"**{book['title']}** | Estimated: {book['estimated_time']} min | Actual: {book['elapsed_time'] / 60:.2f} min"
        )
