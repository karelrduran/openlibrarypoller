<h1 align="center">OpenLibrary Book Search Script</h1>


## Description
***
This script allows users to search for books in OpenLibrary by topics. It uses
    various modules and functions to perform the following tasks:
    - Download data from OpenLibrary
    - Process downloaded data
    - Update a database with the processed data
    - Retrieve books based on specified topics



## Usage
***
    python search_books.py [--updatedata] [--consoleoutput] [topics [topics ...]]


## Arguments
***

    * --updatedata: Optional argument to download data, update the database, and process the data. (THIS OPTION TAKES A LONG TIME)
    * --consoleoutput: Optional argument to display obtained books in the console. If not specified,
      the output will be saved as a JSON file in the '/output/output.json' directory.
    * topics: The topics by which to search for books in OpenLibrary.
    
## Dependencies
    pandas       ->   pip install pandas
    pymongo[srv] ->   python -m pip install "pymongo[srv]"


The script uses command-line arguments to specify whether to update data, display output in
the console, and provide topics for book searches. If the '--updatedata' flag is provided, it
downloads data from OpenLibrary, processes it, and updates the database. Subsequently, it retrieves
books based on the specified topics and provides output according to the specified options.
