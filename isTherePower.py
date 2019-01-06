import os
import dropbox
import requests


def wait_for_internet_connection(url='http://www.example.com', timeout=3):
    print('Waiting for an internet connection...')
    while True:
        try:
            requests.head(url, timeout=timeout)
            print('Connection OK')
            return
        except requests.ConnectionError:
            pass


def main():
    folderPath = '/IFTTT/SMS/'
    fileName = 'is_there_power.txt'

    print('Connecting to Dropbox...')  # Instantiate dropbox object
    dbx = dropbox.Dropbox(os.environ['DBX_ACCESS_TOKEN'])

    print('Searching for message...')
    searchResult = dbx.files_search(folderPath, fileName, max_results=1)

    if len(searchResult.matches) == 1:
        print('Message found! Sending reply...')
        requests.post('https://maker.ifttt.com/trigger/there_is_power/with/key/'
                      + os.environ['WEBHOOK_KEY'],
                      data={'value1': 'Looks like there is power!'})

        # cleanup
        print('Reply sent, cleaning up...')
        dbx.files_delete(folderPath + fileName)
        print('Done!')

    else:
        print('No message received. Exiting.')


if __name__ == '__main__':
    wait_for_internet_connection()
    main()
