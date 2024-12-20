import pandas as pd
from src.data.data_loader import DataLoader


class DataFilter:
    @staticmethod
    def filter_by_title(unfiltered_data: pd.DataFrame, title_query: str, exact_match: bool = False) -> pd.DataFrame:
        """
        Filter books dataframe by title.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            title_query (str): The title or partial title to search for
            exact_match (bool): If True, requires exact title match. If False, searches for substring (default: False)

        Returns:
            pd.DataFrame: Filtered dataframe containing only matching books

        Raises:
            ValueError: If title_query is empty or if required columns are missing
        """
        # Input validation
        if not isinstance(title_query, str) or not title_query.strip():
            raise ValueError("Title query must be a non-empty string")

        # Convert query and titles to lowercase for case-insensitive comparison
        title_query = title_query.lower().strip()

        if exact_match:
            return unfiltered_data[unfiltered_data["title"].str.lower() == title_query]
        else:
            return unfiltered_data[unfiltered_data["title"].str.lower().str.contains(title_query, na=False)]

    @staticmethod
    def filter_by_author(unfiltered_data: pd.DataFrame, author_query: str, exact_match: bool = False) -> pd.DataFrame:
        """
        Filter books dataframe by author.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            author_query (str): The author or partial author string to search for
            exact_match (bool): If True, requires exact match. If False, searches for substring (default: False)

        Returns:
            pd.DataFrame: Filtered dataframe containing only books of matching authors

        Raises:
            ValueError: If author_query is empty
        """
        if not isinstance(author_query, str) or not author_query.strip():
            raise ValueError("Author query must be a non-empty string")

        author_query = author_query.lower().strip()

        if exact_match:
            return unfiltered_data[unfiltered_data["author"].str.lower() == author_query]
        else:
            return unfiltered_data[unfiltered_data["author"].str.lower().str.contains(author_query, na=False)]

    @staticmethod
    def filter_by_minimum_rating(unfiltered_data: pd.DataFrame, minimum_rating: float) -> pd.DataFrame:
        """
        Filter books dataframe by minimum rating.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            minimum_rating (float): The minimum desired rating to be included in the filtered data

        Returns:
            pd.DataFrame: Filtered dataframe containing only books that have a rating higher than specified

        Raises:
            ValueError: If minimum rating is not a valid numerical value
        """
        if not isinstance(minimum_rating, (int, float)):
            raise ValueError("Minimum rating must be a number")

        return unfiltered_data[unfiltered_data["rating"] >= minimum_rating]

    @staticmethod
    def filter_by_language(unfiltered_data: pd.DataFrame, language: str) -> pd.DataFrame:
        """
        Filter books dataframe by language.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            language (str): The language code to filter by (e.g., 'eng' for English)

        Returns:
            pd.DataFrame: Filtered dataframe containing only books in the specified language

        Raises:
            ValueError: If language is empty
        """
        if not isinstance(language, str) or not language.strip():
            raise ValueError("Language must be a non-empty string")

        language = language.lower().strip()
        return unfiltered_data[unfiltered_data["language"].str.lower() == language]

    @staticmethod
    def filter_by_genre(unfiltered_data: pd.DataFrame, genre: str) -> pd.DataFrame:
        """
        Filter books dataframe by genre.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            genre (str): The genre to search for within the books' genre lists

        Returns:
            pd.DataFrame: Filtered dataframe containing only books that include the specified genre

        Raises:
            ValueError: If genre is empty
        """
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError("Genre must be a non-empty string")

        genre = genre.lower().strip()

        # Convert string representation of list to actual list and handle NaN values
        def check_genre(genres_str):
            if pd.isna(genres_str):
                return False
            try:
                # Remove brackets and quotes, split by comma and strip whitespace
                genres_list = [g.strip().strip('"\'').lower() for g in genres_str.strip("[]").split(",")]
                return genre in genres_list
            except:
                return False

        return unfiltered_data[unfiltered_data["genres"].apply(check_genre)]

    @staticmethod
    def filter_by_minimum_pages(unfiltered_data: pd.DataFrame, minimum_pages: int) -> pd.DataFrame:
        """
        Filter books dataframe by minimum number of pages.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            minimum_pages (int): The minimum number of pages a book must have to be included

        Returns:
            pd.DataFrame: Filtered dataframe containing only books with at least the specified number of pages

        Raises:
            ValueError: If minimum_pages is not a positive integer
        """
        if not isinstance(minimum_pages, int) or minimum_pages < 0:
            raise ValueError("Minimum pages must be a non-negative integer")

        # Handle NaN values by excluding them from results when filtering
        return unfiltered_data[unfiltered_data["pages"].notna() & (unfiltered_data["pages"] >= minimum_pages)]

    @staticmethod
    def filter_by_maximum_pages(unfiltered_data: pd.DataFrame, maximum_pages: int) -> pd.DataFrame:
        """
        Filter books dataframe by maximum number of pages.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            maximum_pages (int): The maximum number of pages a book can have to be included

        Returns:
            pd.DataFrame: Filtered dataframe containing only books with at most the specified number of pages

        Raises:
            ValueError: If maximum_pages is not a positive integer
        """
        if not isinstance(maximum_pages, int) or maximum_pages < 0:
            raise ValueError("Maximum pages must be a non-negative integer")

        # Handle NaN values by excluding them from results when filtering
        return unfiltered_data[unfiltered_data["pages"].notna() & (unfiltered_data["pages"] <= maximum_pages)]

    @staticmethod
    def filter_by_isbn(unfiltered_data: pd.DataFrame, isbn_query: str) -> pd.DataFrame:
        """
        Filter books dataframe by ISBN.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            isbn_query (str): The ISBN to search for

        Returns:
            pd.DataFrame: Filtered dataframe containing only books matching the specified ISBN

        Raises:
            ValueError: If isbn_query is empty or not in a valid ISBN format
        """
        if not isinstance(isbn_query, str) or not isbn_query.strip():
            raise ValueError("ISBN query must be a non-empty string")

        # Clean ISBN query - remove hyphens and spaces
        isbn_query = isbn_query.strip().replace("-", "").replace(" ", "")

        # Basic validation of ISBN format
        if not isbn_query.isalnum() or (len(isbn_query) != 10 and len(isbn_query) != 13):
            raise ValueError("ISBN must be either 10 or 13 characters long and contain only letters and numbers")

        # Clean ISBNs in dataframe for comparison
        clean_isbns = unfiltered_data["isbn"].str.replace("-", "").str.replace(" ", "")
        return unfiltered_data[clean_isbns == isbn_query]
