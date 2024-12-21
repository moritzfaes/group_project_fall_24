import streamlit as st
import pandas as pd
import math
from src.data.filters import DataFilter
from src.data.data_loader import DataLoader


def initialize_session_state():
    """
    Initialize session state variables for the library feature.
    Only initialize if they don't exist to preserve data between reruns.
    """

    if "initialized" not in st.session_state:
        print("DEBUG: First time initialization")
        st.session_state.initialized = True
        st.session_state.library = {}
        st.session_state.search_results = pd.DataFrame()
        # Add pagination states
        st.session_state.current_page = 1
        st.session_state.items_per_page = 10
    else:
        print("DEBUG: Session already initialized, preserving state")
        print("DEBUG: Current library:", st.session_state.library)


def get_paginated_results(df: pd.DataFrame, page: int, items_per_page: int):
    """
     Return a slice of the dataframe for the current page.
     This is necessary for performance reasons

     Args:
         df: DataFrame containing all search results
         page: Current page number (1-based)
         items_per_page: Number of items to display per page

     Returns:
         DataFrame slice for the current page
     """
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    return df.iloc[start_idx:end_idx]


def display_pagination_controls(total_items: int):
    """
    Display pagination controls and handle page navigation.

    Args:
        total_items: Total number of items in the search results
    """
    total_pages = math.ceil(total_items / st.session_state.items_per_page)

    # Create three columns for pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("← Previous", disabled=st.session_state.current_page == 1):
            st.session_state.current_page -= 1
            st.rerun()

    with col2:
        st.write(f"Page {st.session_state.current_page} of {total_pages}")

    with col3:
        if st.button("Next →", disabled=st.session_state.current_page == total_pages):
            st.session_state.current_page += 1
            st.rerun()


def display_library_section(df: pd.DataFrame):
    """
    Display the user's library with options to update reading status.
    Now simplified since ISBNs are guaranteed unique.
    """
    st.header("My Library")

    if not st.session_state.library:
        st.info("Your library is empty. Add books from the search results!")
        return

    library_books = df[df["isbn"].isin(st.session_state.library.keys())]

    for _, book in library_books.iterrows():  # No need for enumerate anymore
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{book['title']}**")
            st.write(f"Author: {book['author']}")
            st.write(f"Status: {st.session_state.library[book['isbn']]}")

        with col2:
            current_status = st.session_state.library[book["isbn"]]
            if current_status == "Want to Read":
                if st.button(
                    "Mark as Read",
                    key=f"read_{book['isbn']}",
                    help="Mark this book as read"
                ):
                    st.session_state.library[book["isbn"]] = "Read"
                    st.rerun()

        with col3:
            if st.button(
                "Remove",
                key=f"remove_{book['isbn']}",
                help="Remove this book from your library"
            ):
                del st.session_state.library[book['isbn']]
                st.rerun()

        st.divider()


def add_to_library(isbn: str):
    """Callback function to add book to library"""
    st.session_state.library[isbn] = "Want to Read"
    print(f"DEBUG: Added {isbn} to library via callback")


def display_search_results(df: pd.DataFrame):
    """
    Display paginated search results with simplified key generation.
    """
    st.header("Search Results")

    if st.session_state.search_results.empty:
        st.warning("No books found matching your criteria")
        return

    total_results = len(st.session_state.search_results)

    current_page_results = get_paginated_results(
        st.session_state.search_results,
        st.session_state.current_page,
        st.session_state.items_per_page
    )

    st.write(f"Found {total_results} books. Showing {len(current_page_results)} results.")

    for _, book_data in current_page_results.iterrows():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"**{book_data['title']}**")
            st.write(f"Author: {book_data['author']}")
            st.write(f"Rating: {book_data['rating']:.2f}")

        with col2:
            if book_data["isbn"] not in st.session_state.library:
                st.button(
                    "Add to Library",
                    key=f"add_{book_data['isbn']}_{st.session_state.current_page}",
                    on_click=add_to_library,
                    args=(book_data["isbn"],),
                    help="Add this book to your library"
                )
            else:
                st.info("Already in library")

    st.divider()

    if total_results > st.session_state.items_per_page:
        display_pagination_controls(total_results)


def main():
    st.title("Book Recommendation System")

    print("DEBUG: Starting main function")

    # Initialize session state first
    initialize_session_state()

    # Load data
    try:
        df = DataLoader.get_book_data()
        print(f"DEBUG: Data loaded, shape: {df.shape}")
        #st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Create main tabs for library and search
    main_tab1, main_tab2 = st.tabs(["My Library", "Search Books"])

    # Library Tab
    with main_tab1:
        display_library_section(df)

    # Search Tab
    with main_tab2:
        # Create tabs for different search methods
        search_tabs = st.tabs([
            "Title/Author Search",
            "Rating",
            "Page Count",
            "Genre",
            "ISBN Search"
        ])

        # Tab 1: Title and Author Search
        with search_tabs[0]:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Search by Title")
                title_query = st.text_input("Enter title keywords", key="title_input")
                title_exact = st.checkbox("Exact title match", key="title_exact")

                if st.button("Search by Title", key="title_search"):
                    if title_query:
                        try:
                            st.session_state.search_results = DataFilter.filter_by_title(
                                df, title_query, title_exact
                            )
                            display_search_results(st.session_state.search_results)
                        except ValueError as e:
                            st.error(str(e))

            with col2:
                st.subheader("Search by Author")
                author_query = st.text_input("Enter author name", key="author_input")
                author_exact = st.checkbox("Exact author match", key="author_exact")

                if st.button("Search by Author", key="author_search"):
                    if author_query:
                        try:
                            st.session_state.search_results = DataFilter.filter_by_author(
                                df, author_query, author_exact
                            )
                            display_search_results(df)
                        except ValueError as e:
                            st.error(str(e))

        # Tab 2: Rating
        with search_tabs[1]:
            st.subheader("Filter by Rating")
            min_rating = st.slider(
                "Minimum Rating",
                0.0,
                5.0,
                0.0,
                0.5,
                key="rating_slider"
            )

            if st.button("Apply Rating Filter", key="rating_filter"):
                try:
                    st.session_state.search_results = DataFilter.filter_by_minimum_rating(
                        df, min_rating
                    )
                    display_search_results(df)
                except ValueError as e:
                    st.error(str(e))

        # Tab 3: Page Count
        with search_tabs[2]:
            st.subheader("Filter by Page Count")
            col1, col2 = st.columns(2)

            with col1:
                min_pages = st.number_input(
                    "Minimum Pages",
                    min_value=0,
                    value=0,
                    key="min_pages"
                )
            with col2:
                max_pages = st.number_input(
                    "Maximum Pages",
                    min_value=0,
                    value=1000,
                    key="max_pages"
                )

            if st.button("Apply Page Filter", key="page_filter"):
                try:
                    results = df
                    if min_pages > 0:
                        results = DataFilter.filter_by_minimum_pages(results, min_pages)
                    if max_pages > 0:
                        results = DataFilter.filter_by_maximum_pages(results, max_pages)
                    st.session_state.search_results = results
                    display_search_results(df)
                except ValueError as e:
                    st.error(str(e))

        # Tab 4: Genre
        with search_tabs[3]:
            st.subheader("Filter by Genre")
            # Extract unique genres from the string representation of lists
            all_genres = set()
            for genres_str in df["genres"].dropna():
                try:
                    # Remove brackets and quotes, split by comma and strip whitespace
                    genres = [g.strip().strip('"\'') for g in genres_str.strip('[]').split(',')]
                    all_genres.update(genres)
                except:
                    continue

            genres = sorted(all_genres)
            selected_genre = st.selectbox("Select Genre", genres, key="genre_select")

            if st.button("Apply Genre Filter", key="genre_filter"):
                try:
                    st.session_state.search_results = DataFilter.filter_by_genre(
                        df, selected_genre
                    )
                    display_search_results(df)
                except ValueError as e:
                    st.error(str(e))

        # Tab 5: ISBN Search
        with search_tabs[4]:
            st.subheader("Search by ISBN")
            isbn_query = st.text_input("Enter ISBN", key="isbn_input")

            if st.button("Search by ISBN", key="isbn_search"):
                if isbn_query:
                    try:
                        st.session_state.search_results = DataFilter.filter_by_isbn(
                            df, isbn_query
                        )
                        display_search_results(df)
                    except ValueError as e:
                        st.error(str(e))

        # Reset button for search results
        if st.button("Reset All Filters", key="reset_filters"):
            st.session_state.search_results = df
            display_search_results(df)


if __name__ == "__main__":
    main()