import os
import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from difflib import SequenceMatcher
from statistics import median, mean


def write_to_mongodb():
    """
        Writes data from CSV files to a MongoDB collection.

        The function reads CSV files from a specified folder path ('../data/processed'),
        filters for files with a '.csv' extension, and establishes a connection with a
        MongoDB database hosted on MongoDB Atlas.

        It's important to note that the function uses visible credentials for accessing the
        MongoDB database. The 'ol_user' used in the connection URI was created with limited
        time-based access and will be removed from MongoDB after one week for security purposes.

        The function utilizes the 'pymongo' library to establish a connection, create a client,
        access the specified database ('ol_database'), and a collection ('ol_collection').
        It then drops the existing collection and proceeds to read each CSV file from the
        folder, converting its contents into Pandas DataFrames. These DataFrames are then
        converted into dictionaries and inserted into the MongoDB collection using the
        'insert_many' method.

        Note:
        - The MongoDB connection string is created using credentials and the database URI.
        - The function assumes the existence of CSV files in the specified folder path.
        - The MongoDB collection ('ol_collection') is cleared ('drop') before inserting
          new data.

        Returns:
        None. The function writes data from CSV files to the specified MongoDB collection.

        Raises:
        Any exceptions raised during the process (such as connection errors, file reading errors,
        or insertion errors) are caught and printed. The function tries to proceed with the
        remaining files even if one fails, and eventually closes the MongoDB client connection.
    """
    # Path of the folder where the CSV files are located
    folder_path = '../data/processed'

    # Get all files in the folder
    archivos_en_carpeta = os.listdir(folder_path)

    # Filtering .csv files
    archivos_csv = [archivo for archivo in archivos_en_carpeta if archivo.endswith('.csv')]

    # Establish connection with MongoDB
    username = quote_plus('ol_user')
    password = quote_plus('12345678ol_user')
    uri = 'mongodb+srv://' + username + ':' + password + '@oldb.kcwnra7.mongodb.net/?retryWrites=true&w=majority'

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:

        db = client['ol_database']
        collection = db['ol_collection']

        collection.drop()

        # Read each CSV file and load the data into DataFrames
        for archivo_csv in archivos_csv:
            complete_path = os.path.join(folder_path, archivo_csv)
            df = pd.read_csv(complete_path)
            records = df.to_dict(orient='records')
            collection.insert_many(records)
    except Exception as e:
        print(e)
    finally:
        client.close()


def getWords(input: str) -> list:
    """
        Extracts words from an input string based on specified criteria.

        This function splits the input string into words and filters the words based
        on certain criteria. It calculates the minimum word length depending on the
        word count and the median length of words to exclude presumed fillers or short
        words that may not be relevant.

        Args:
        - input (str): The input string to extract words from.

        Returns:
        list: A list containing words from the input string that meet the minimum length
        criteria calculated based on the word count and median length of words.

        Note:
        - The function determines the minimum word length dynamically based on word count
          and the median length of words in the input string.
        - It filters out words shorter than the calculated minimum length.

        Example:
        getWords("This is a test sentence with some words")
        # This will extract words longer than the dynamically determined minimum length
        # based on the word count and median length of words in the input string.
    """
    words = input.split()
    lengths = [len(x) for x in words if len(x) > 1]

    # set the minimum word length based on word count
    # and median of word length to remove presumed fillers
    minLength = 2
    if len(words) >= 3 and median(lengths) > 4:
        minLength = 5
    elif len(words) >= 2 and median(lengths) > 3:
        minLength = 4

    # keep words of minimum length
    answer = list()
    for item in words:
        if len(item) >= minLength:
            answer.append(item)

    return answer


def string_matching(match_list: list, user_input: str) -> tuple:
    """
        Finds the best match between user input and a list of strings.

        This function compares the user input string with a list of strings (matchList)
        to find the best match based on similarity scores. It calculates the similarity
        scores using the SequenceMatcher from difflib library.

        Args:
        - match_list (list): A list of strings to be compared with the user input.
        - user_input (str): The input string provided by the user for comparison.

        Returns:
        tuple: A tuple containing the maximum similarity score and the string from
        matchList that has the best match with the user input.

        Note:
        - The function uses difflib's SequenceMatcher to calculate similarity scores
          between strings.
        - It compares the user input string with each string in matchList and calculates
          a score based on full string comparison and word-level comparisons.
        - The string with the highest score is considered the best match and returned
          along with its score.

        Example:
        string_matching(['apple', 'orange', 'banana'], 'apples')
        # This will compare 'apples' with 'apple', 'orange', and 'banana' and return
        # the maximum similarity score and the best-matching string from the list.
    """

    # find the best match between the user input and the link list
    maxi = 0
    result = ''
    for matchItem in match_list:

        # ratio of the original item comparison
        fullRatio = SequenceMatcher(None, user_input, matchItem).ratio()

        # every word of the user input will be compared
        # to each word of the list item, the maximum score
        # for each user word will be kept
        wordResults = list()
        for userWord in getWords(user_input):
            maxWordRatio = 0
            for matchWord in getWords(matchItem):
                wordRatio = SequenceMatcher(None, userWord, matchWord).ratio()
                if wordRatio > maxWordRatio:
                    maxWordRatio = wordRatio
            wordResults.append(maxWordRatio)

        # the total score for each list item is the full ratio
        # multiplied by the mean of all single word scores
        itemScore = fullRatio * mean(wordResults)

        # print item result
        print('%.5f' % itemScore, matchItem)

        # keep track of maximum score
        if itemScore > maxi:
            maxi = itemScore
            result = matchItem

    # award ceremony
    print('result:', result, maxi)
    return maxi, result


def match_topic(subjects: str, topics: list) -> bool:
    """
        Checks if any topics exist within the subjects string.

        This function iterates through a list of topics and checks if any of them exist
        within the subjects string. Both subjects and topics are treated in a case-insensitive
        manner during comparison.

        Args:
        - subjects (str): A string containing subjects or topics.
        - topics (list): A list of topics to check for within the subjects string.

        Returns:
        bool: Returns True if any of the specified topics are found within the subjects string.
        Otherwise, returns False.

        Note:
        - The function performs a case-insensitive check between the subjects and topics.
        - It iterates through each topic in the list and checks if it exists within the subjects string.
        - Returns True immediately upon finding the first matching topic, otherwise, returns False.

        Example:
        topic_exist("Math, Science, History", ["science", "literature"]) will return True.
    """
    result = False
    for t in topics:
        result = t.lower() in subjects.lower()
        if result:
            return True

        # ------------------------------------------

        # if len(subjects) > 0:
        #     subjects_list = list(subjects[1:-1].split(','))
        #     item_score, _ = string_matching(subjects_list, t)
        #     if item_score > 0.5:
        #         return True
    return False


def read_from_mongodb(topics) -> list:
    """
        Retrieves data from a MongoDB collection based on specified topics.

        The function establishes a connection with a MongoDB database hosted on MongoDB Atlas
        using credentials visible within the function ('ol_user' and its password). It creates
        a client, accesses the specified database ('ol_database'), and a collection
        ('ol_collection'). Then, it retrieves all documents from the collection and filters
        the data based on specified 'topics'.

        Args:
        - topics (list): A list of topics to filter the MongoDB documents.

        Returns:
        list: A list containing keys from documents in the MongoDB collection that match the
        specified 'topics'.

        Note:
        - The MongoDB connection string is created using visible credentials and the database URI.
        - The function uses 'topics' to filter documents based on 'subjects' in the collection.
        - If 'topics' match any 'subjects' in the documents, the 'key' of those documents is
          appended to the result list.

        Raises:
        Any exceptions raised during the retrieval process (such as connection errors or
        querying errors) are caught and printed. The function eventually closes the MongoDB
        client connection.
    """

    if not bool(len(topics)):
        return []
    # Establish connection with MongoDB
    username = quote_plus('ol_user')
    password = quote_plus('12345678ol_user')
    uri = 'mongodb+srv://' + username + ':' + password + '@oldb.kcwnra7.mongodb.net/?retryWrites=true&w=majority'

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    result = []

    try:
        db = client['ol_database']
        my_collection = db['ol_collection']

        all_data = my_collection.find()

        if all_data:
            for doc in all_data:
                if match_topic(doc['subjects'], topics):
                    result.append(doc['key'])
    except Exception as e:
        print(e)
    finally:
        client.close()

    return result
