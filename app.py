import streamlit as st
import pandas as pd
from src.basic_recommender.filters import DataFilter
from src.data.data_loader import DataLoader


def initialize_session_state():
    """
    Initialize session state variables for the library feature.
    """
    if "library" not in st.session_state:
        # Store library as a dictionary with ISBN as key and reading status as value
        st.session_state.library = {}

    if "search_results" not in st.session_state:
        st.session_state.search_results = None


def display_library_section(df: pd.DataFrame):
    """
    Display the user's library with options to update reading status.
    """
    st.header("My Library")

    if not st.session_state.library:
        st.info("Your library is empty. Add books from the search results!")
        return

    # Get full book details for books in library
    library_books = df[df["isbn"].isin(st.session_state.library.keys())]

    for _, book in library_books.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{book['title']}**")
            st.write(f"Author: {book['author']}")
            # Fixed: Use ISBN instead of title to get status
            st.write(f"Status: {st.session_state.library[book['isbn']]}")

        with col2:
            current_status = st.session_state.library[book["isbn"]]
            if current_status == "Want to Read":
                if st.button("Mark as Read", key=f"read_{book['isbn']}"):
                    st.session_state.library[book["isbn"]] = "Read"
                    st.rerun()

        with col3:
            if st.button("Remove", key=f"remove_{book['isbn']}"):
                del st.session_state.library[book['isbn']]
                st.rerun()

        st.divider()


def display_search_results(df: pd.DataFrame):
    """Display search results with options to add books to library."""
    st.header("Search Results")

    if len(st.session_state.search_results) > 0:
        # Use enumerate to get a unique index for each book
        for idx, book in enumerate(st.session_state.search_results.iterrows()):
            _, book_data = book  # Unpack the row data
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**{book_data['title']}**")
                st.write(f"Author: {book_data['author']}")
                st.write(f"Rating: {book_data['rating']:.2f}")

            with col2:
                if book_data["isbn"] not in st.session_state.library:
                    # Use both ISBN and index to create unique keys
                    if st.button("Add to Library", key=f"add_{book_data['isbn']}_{idx}"):
                        st.session_state.library[book_data['isbn']] = "Want to Read"
                        st.success("Added to library!")
                        st.rerun()  # Add this to refresh the view after adding a book
                else:
                    st.info("Already in library")

            st.divider()

        st.write(f"Found {len(st.session_state.search_results)} books")
    else:
        st.warning("No books found matching your criteria")


def main():
    st.title("Book Recommendation System")

    # Initialize session state
    initialize_session_state()

    # Load data
    try:
        df = DataLoader.get_book_data()
        st.success("Data loaded successfully!")
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
                            display_search_results(df)
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