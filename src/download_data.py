import os
import subprocess
import requests
from concurrent.futures import ThreadPoolExecutor


def ol_download_dumb_files(url: str, unprocessed_path: str):
    """
        Downloads a file from a given URL and saves it to the specified destination path.

        Args:
        - url (str): The URL from which to download the file.
        - unprocessed_path (str): The path where the downloaded file will be saved.

        Returns:
        None. The function saves the downloaded file to the specified path.

        Raises:
        - requests.RequestException: If there is an issue during the GET request.

        The function performs a GET request to download a file from the specified URL.
        If the download is successful (status code 200), it saves the file to the specified path.
        If there is an error during the download, it prints an error message along with the
        status code (if available) or the encountered exception.
    """
    try:
        # Perform GET request to download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(unprocessed_path, 'wb') as archivo_destino:
                archivo_destino.write(response.content)
                print(f"File downloaded: {unprocessed_path}")
        else:
            print(f"Error downloading from {url}. Error code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error downloading from {url}: {e}")


def thread_download():
    """
        Downloads files from specified URLs concurrently using ThreadPoolExecutor.

        The function initiates concurrent downloading of files from the given URLs
        using ThreadPoolExecutor with a maximum of 5 workers. It utilizes the
        'ol_download_dumb_files' function to perform the download operation.

        This function assumes that 'ol_download_dumb_files' is defined and accepts
        two arguments: URL(s) and destination file path(s) for downloading.

        After parallel downloads, the function runs a decompression command for each
        downloaded gzip file in 'unprocessed_paths' using the 'gzip' command-line utility.
        It subsequently removes the original compressed files after successful decompression.

        Note:
        - The 'urls' list contains the URLs of the files to be downloaded.
        - The 'unprocessed_paths' list contains the destination paths where downloaded
          files will be saved.

        Returns:
        None. The function performs downloads and decompression in place.
    """
    urls = [
        'https://openlibrary.org/data/ol_dump_editions_latest.txt.gz'
    ]
    unprocessed_paths = [
        '../data/unprocessed/ol_dump_editions.txt.gz'
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Use executor.map to execute downloads in parallel
        executor.map(ol_download_dumb_files, urls, unprocessed_paths)

    # Run the gzip command to decompress the files
    for f_path in unprocessed_paths:
        decompression_command = f"gzip -d -c  {f_path} > {f_path.replace('.gz', '', 1)}"
        subprocess.run(decompression_command, shell=True)

        # Delete the archive after unzipping
        os.remove(f_path)
