import json
import pandas as pd


def ol_read_manipulate_files():
    """
        Reads, processes, and manipulates data from a file in chunks and saves it to CSV files.

        The function reads data from the file located at '../data/ol_dump_editions.txt'. It reads
        the data in chunks using Pandas, selects specific columns, processes JSON data within the
        'json' column, and creates a new DataFrame with columns 'key', 'title', and 'subjects'.
        The 'subjects' column is generated by joining subjects from the JSON data.

        The function iterates through the chunks, processes JSON data from the 'json' column, extracts
        relevant information such as 'key', 'title', and 'subjects' if available, and appends this
        information to the 'data' DataFrame.

        Upon processing each chunk, the function saves the current 'data' DataFrame into a separate
        CSV file located at '../data/processed/booksX.csv', where X represents the file number.

        Note:
        - The input file '../data/ol_dump_editions.txt' is assumed to exist.
        - JSON data within the file is processed to extract 'key', 'title', and 'subjects'.
        - The function saves the processed data into separate CSV files.
    """
    input_file = "../data/ol_dump_editions.txt"

    columns = ['type', 'key', 'revision', 'last_modified', 'json']

    chunksize = 10 ** 5
    iterator = pd.read_csv(input_file, sep='\t', iterator=True, chunksize=chunksize, names=columns)

    df_columns = ['key', 'title', 'subjects']
    data = pd.DataFrame(columns=df_columns)

    file_number = 0

    for iter in iterator:
        for row in iter['json']:
            book = json.loads(row)
            if ('key' not in book) or ('title' not in book):
                continue
            else:
                key = book['key']
                title = book['title']
            if 'subjects' in book:
                subjects = ','.join(book['subjects'])
            else:
                subjects = ''
            data = data.append({'key': key, 'title': title, 'subjects': subjects}, ignore_index=True)
        # write the dataframe to a file
        output_file = '../data/processed/books' + str(file_number) + '.csv'
        data.to_csv(output_file, index=False)
        file_number += 1
        data = pd.DataFrame(columns=df_columns)
