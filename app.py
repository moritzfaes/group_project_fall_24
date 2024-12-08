import streamlit as st
import pandas as pd
from src.basic_recommender.filters import DataFilter
from src.data.data_loader import DataLoader


def main():
    st.title("Book Recommendation System")

    # Load data
    try:
        df = DataLoader.get_book_data()
        st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Create sidebar for filtering options
    st.sidebar.header("Filter Options")

    # Initialize session state for search results if not exists
    if 'search_results' not in st.session_state:
        st.session_state.search_results = df

    # Create tabs for different search methods
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Title/Author Search",
        "Rating",
        "Page Count",
        "Genre",
        "ISBN Search"
    ])

    # Tab 1: Title and Author Search
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Search by Title")
            title_query = st.text_input("Enter title keywords", key="title_input")
            title_exact = st.checkbox("Exact title match", key="title_exact")

            if st.button("Search by Title", key="title_search"):
                if title_query:
                    try:
                        results = DataFilter.filter_by_title(df, title_query, title_exact)
                        st.session_state.search_results = results
                    except ValueError as e:
                        st.error(str(e))

        with col2:
            st.subheader("Search by Author")
            author_query = st.text_input("Enter author name", key="author_input")
            author_exact = st.checkbox("Exact author match", key="author_exact")

            if st.button("Search by Author", key="author_search"):
                if author_query:
                    try:
                        results = DataFilter.filter_by_author(df, author_query, author_exact)
                        st.session_state.search_results = results
                    except ValueError as e:
                        st.error(str(e))

    # Tab 2: Rating and Language
    with tab2:
        col1 = st.columns(1)[0]

        with col1:
            st.subheader("Filter by Rating")
            min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5, key="rating_slider")

            if st.button("Apply Rating Filter", key="rating_filter"):
                try:
                    results = DataFilter.filter_by_minimum_rating(df, min_rating)
                    st.session_state.search_results = results
                except ValueError as e:
                    st.error(str(e))

    # Tab 3: Page Count
    with tab3:
        st.subheader("Filter by Page Count")
        col1, col2 = st.columns(2)

        with col1:
            min_pages = st.number_input("Minimum Pages", min_value=0, value=0, key="min_pages")
        with col2:
            max_pages = st.number_input("Maximum Pages", min_value=0, value=1000, key="max_pages")

        if st.button("Apply Page Filter", key="page_filter"):
            try:
                results = df
                if min_pages > 0:
                    results = DataFilter.filter_by_minimum_pages(results, min_pages)
                if max_pages > 0:
                    results = DataFilter.filter_by_maximum_pages(results, max_pages)
                st.session_state.search_results = results
            except ValueError as e:
                st.error(str(e))

    # Tab 4: Genre
    with tab4:
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
                results = DataFilter.filter_by_genre(df, selected_genre)
                st.session_state.search_results = results
            except ValueError as e:
                st.error(str(e))

    # Tab 5: ISBN Search
    with tab5:
        st.subheader("Search by ISBN")
        isbn_query = st.text_input("Enter ISBN", key="isbn_input")

        if st.button("Search by ISBN", key="isbn_search"):
            if isbn_query:
                try:
                    results = DataFilter.filter_by_isbn(df, isbn_query)
                    st.session_state.search_results = results
                except ValueError as e:
                    st.error(str(e))

    # Display results
    st.header("Search Results")
    if len(st.session_state.search_results) > 0:
        # Display the results in a clean format
        results_df = st.session_state.search_results[['title', 'author', 'rating', 'language', 'pages', 'genres']]
        st.dataframe(results_df)
        st.write(f"Found {len(st.session_state.search_results)} books")
    else:
        st.warning("No books found matching your criteria")

    # Reset button
    if st.button("Reset All Filters", key="reset_filters"):
        st.session_state.search_results = df


if __name__ == "__main__":
    main()