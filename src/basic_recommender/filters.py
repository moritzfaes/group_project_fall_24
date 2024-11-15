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
        Filter books dataframe by title.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            author_query (str): The author or partial author string to search for
            exact_match (bool): If True, requires exact match. If False, searches for substring (default: False)

        Returns:
            pd.DataFrame: Filtered dataframe containing only books of matching authors

        Raises:
            ValueError: If author_query is empty
        """
        # Help for implementation --> look at the filter_by_title function to see how this can be done

        pass

    @staticmethod
    def filter_by_minimum_rating(unfiltered_data: pd.DataFrame, minimum_rating: float) -> pd.DataFrame:
        """
        Filter books dataframe by minimum rating.

        Args:
            unfiltered_data (pd.DataFrame): DataFrame containing book data
            minimum_rating (str): The minimum desired rating to be included in the filtered data


        Returns:
            pd.DataFrame: Filtered dataframe containing only books that have a rating higher than specified

        Raises:
            ValueError: If minimum rating is empty or if it is not a numerical value
        """
        pass

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
        pass

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

        Notes:
            The genre filtering works by searching through lists of genres associated with each book.
            A book will be included in the results if the specified genre appears anywhere in its genre list.
            P.S. This will be more difficult to implement than the other functions
        """

        pass

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
            ValueError: If minimum_pages is not a positive integer (or if it is not an integer at all)
        """

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
            ValueError: If maximum_pages is not a positive integer (or if it is not an integer at all)
        """

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

        Notes:
            ISBN matching is exact and case-insensitive. Both ISBN-10 and ISBN-13 formats are supported. --> Check
            the data to see if both formats occur. if not, only account for the one that is appearing
        """
        pass


# This function is to show how you can test whether your code behaves in the way you want
def main():
    # Example usage
    book_data = DataLoader.get_book_data()

    # Test the filter with different scenarios
    print("\nTesting partial match:")
    harry_potter_books = DataFilter.filter_by_title(book_data, "harry potter")
    print(f"Found {len(harry_potter_books)} books matching 'harry potter'")
    print(harry_potter_books[["title", "author"]].head())

    print("\nTesting exact match:")
    exact_book = DataFilter.filter_by_title(
        book_data,
        "Harry Potter and the Sorcerer's Stone",
        exact_match=True
    )
    print(f"Found {len(exact_book)} books with exact title match")
    print(exact_book[["title", "author"]].head())


if __name__ == "__main__":
    main()

