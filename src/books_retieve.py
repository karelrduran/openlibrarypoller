import requests


def books_request_by_key(keys: list) -> list:
    """
        Retrieves book details from Open Library API based on provided keys.

        This function takes a list of book keys and fetches book details for each key
        from the Open Library API (https://openlibrary.org/).

        Args:
        - keys (list): A list of book keys in the format 'https://openlibrary.org/works/{book_key}'.

        Returns:
        list: A list containing book details fetched from the Open Library API for the provided keys.

        Note:
        - The function extracts the book key from the URL provided in the 'keys' list.
        - It constructs the API endpoint for each book using the extracted book key.
        - Retrieves book details for each book key using the Open Library API.
        - Returns a list containing book details in JSON format for the provided keys.

        Example:
        books_request_by_key(['https://openlibrary.org/works/OL1W', 'https://openlibrary.org/works/OL2W'])
        # This will fetch book details for books with keys OL1W and OL2W from Open Library API.
        """
    result = []
    for key in keys:
        book_key = key.split('/')[-1]
        url = f"https://openlibrary.org/works/{book_key}.json"
        response = requests.get(url)
        if response.status_code == 200:
            book_details = response.json()
            result.append(book_details)
    return result
