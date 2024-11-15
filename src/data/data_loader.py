import pandas as pd
from pathlib import Path


class DataLoader:
    @staticmethod
    def get_project_root() -> Path:
        """Returns project root folder."""
        # Starting from the current file, go up until we find the root directory
        current_file = Path(__file__).resolve()
        # Go up two levels from src/data to reach root
        return current_file.parent.parent.parent

    @staticmethod
    def get_book_data() -> pd.DataFrame:
        """Load the book dataset using an absolute path resolved from project root."""
        root_dir = DataLoader.get_project_root()
        data_path = root_dir / "data" / "books_dataset_cleaned.csv"

        if not data_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {data_path}. "
                f"Please ensure the file exists at the correct location relative to project root: {root_dir}"
            )

        book_data = pd.read_csv(data_path)
        return book_data

