''' This file contains several examples on how to access the EUDAT B2SHARE service through its API
    In general all access requires a token generated on the B2SHARE service instance on a personal account '''
''' Note: this file is not intended to be used as a library or framework '''
''' More information can be found here: https://trng-b2share.eudat.eu/docs/b2share-rest-api '''

import requests
import json
from urlparse import urljoin

B2SHARE_URL = 'https://trng-b2share.eudat.eu/'

def access_token_file():
    ''' Read the token from a given file named 'token' '''

    f = open(r'token', 'r')
    return f.read()


def read_deposit_id():
    ''' Read deposit from file '''
    
    f = open('deposit_id', 'r')
    return f.read()


def list_records():
    ''' List all records in service '''

    token = access_token_file().rstrip()
    url = urljoin(B2SHARE_URL, 'api/records')
    payload = {'access_token': token}

    r = requests.get(url, params=payload, verify=False)
    print r
    print r.text


def list_records_pagination(page_size, page_offset):
    ''' List all user records per page '''
    
    token = access_token_file().rstrip()
    url = urljoin(B2SHARE_URL, 'api/records')
    payload = {'page_size': page_size,
               'page_offset': page_offset,
               'access_token': token
               }

    r = requests.get(url, params=payload, verify=False)
    print r
    print r.text


def list_specific_record(record_id):
    ''' List specific records '''

    token = access_token_file().rstrip()
    exten = 'api/record/' + record_id
    url = urljoin(B2SHARE_URL, exten)
    payload = {'access_token': token}
    r = requests.get(url, params=payload, verify=False)
    print r
    r = json.loads(r.text)
    print json.dumps(r, indent=4, separators=(',', ': '))


def create_deposition():
    ''' Create deposition '''

    token = access_token_file().rstrip()
    url = urljoin(B2SHARE_URL, '/api/depositions')
    payload = {'access_token': token}
    r = requests.post(url, params=payload, verify=False)
    print r
    print r.text
    res = r.json()
    deposit_id = res['deposit_id']
    f = open('deposit_id' , 'wb')
    f.write(deposit_id)
    f.closed


def add_file(file_path):
    ''' Add file to deposition '''

    token = access_token_file().rstrip()
    deposit_id = read_deposit_id().rstrip()
    files = {'file': open(file_path, 'rb')}
    path = '/api/deposition/' + deposit_id + '/files'
    url = urljoin(B2SHARE_URL, path)
    payload = {'access_token': token}
    r = requests.post(url, files=files, params=payload, verify=False)
    print r
    print r.text


def list_files():
    ''' List files in deposition '''

    token = access_token_file().rstrip()
    deposit_id = read_deposit_id().rstrip()
    path = '/api/deposition/' + deposit_id + '/files'
    url = urljoin(B2SHARE_URL, path)
    payload = {'access_token': token}
    r = requests.get(url, params=payload, verify=False)
    print r.text


def commit_deposition():
    ''' Commit deposition '''

    token = access_token_file().rstrip()
    deposit_id = read_deposit_id().rstrip()
    path = '/api/deposition/' + deposit_id + '/commit'
    url = urljoin(B2SHARE_URL, path)
    payload = {'access_token': token}
    info = {"domain":           "generic",
            "title":            "Demo",
            "description":      "A little demo ...",
            "open_access":      "true",
            "creator":          "Demo",
            "publication_date": "05-02-2016",
            "licence":          "Creative Commons Attribution (CC-BY)",
            "keywords":         "Demo"
            }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(info),
                      params=payload, verify=False, headers=headers)
    print r
    print r.text
