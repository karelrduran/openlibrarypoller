import argparse
from src.download_data import thread_download
from src.data_processing import ol_read_manipulate_files
from src.database_manipulation import write_to_mongodb, read_from_mongodb
from src.books_retieve import books_request_by_key
import json

"""
    OpenLibrary Book Search Script
    
    This script allows users to search for books in OpenLibrary by topics. It uses
    various modules and functions to perform the following tasks:
    - Download data from OpenLibrary
    - Process downloaded data
    - Update a database with the processed data
    - Retrieve books based on specified topics
    
    Usage:
    python script_name.py [--updatedata] [--consoleoutput] [topics [topics ...]]
    
    Arguments:
    - --updatedata: Optional argument to download data, update the database, and process the data.
    - --consoleoutput: Optional argument to display obtained books in the console. If not specified,
      the output will be saved as a JSON file in the '/output/output.json' directory.
    - topics: The topics by which to search for books in OpenLibrary.
    
    The script uses command-line arguments to specify whether to update data, display output in
    the console, and provide topics for book searches. If the '--updatedata' flag is provided, it
    downloads data from OpenLibrary, processes it, and updates the database. Subsequently, it retrieves
    books based on the specified topics and provides output according to the specified options.
    
    This script requires the following modules and functions:
    - argparse: For parsing command-line arguments.
    - src.download_data.thread_download: Function to download data from OpenLibrary.
    - src.data_processing.ol_read_manipulate_files: Function to process downloaded data.
    - src.database_manipulation.write_to_mongodb: Function to update the database.
    - src.database_manipulation.read_from_mongodb: Function to retrieve book keys from the database.
    - src.books_retieve.books_request_by_key: Function to retrieve book details based on keys.
    - json: For handling JSON data.
    
    To use this script, provide the desired options and topics as command-line arguments when executing
    the script. For example:
    python script_name.py --updatedata --consoleoutput science fiction fantasy
"""

parser = argparse.ArgumentParser(description='Search for books in OpenLibrary by topics')
parser.add_argument(
    '--updatedata',
    action='store_true',
    help='Download data and update the database(optional).')
parser.add_argument(
    '--consoleoutput',
    action='store_true',
    help='Displays all books obtained, by console. if not specified, the output will be a json file in /output/output.json')
parser.add_argument(
    'topics',
    nargs='*',
    help='The topics you want to search by.')

args = parser.parse_args()

if args.updatedata:
    print('Update Data')
    # Download data from OpenLibrary
    thread_download()
    ol_read_manipulate_files()
    write_to_mongodb()

topics_list = []
books = []
if args.topics:
    for topic in args.topics:
        topics_list.append(topic)

    keys = read_from_mongodb(topics_list)
    books = books_request_by_key(keys)
    if args.consoleoutput:
        print(books)
    else:
        with open("output/output.json", 'w') as json_file:
            for elem in books:
                json.dump(elem, json_file)
                json_file.write('\n')

else:
    print("No topics were provided.")
