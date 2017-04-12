#!/bin/bash python
# loads metadata from a CSV file and matches this with the metadata fields of the EUDAT community schema in B2SHARE

import requests

# based on the type of the field and its substuctures, add the value to the right key in the exiting output structure
def setKey(out, definition, key, value, subkey = None):
    if "type" in definition:
        if definition["type"] in ["string", "integer"]:
            out[key] = value
        elif definition["type"] == "boolean":
            out[key] = True if value == "true" else False
        elif definition["type"] == "object":
            if key in out:
                out = out[key]
            elif key != subkey:
                out[key] = {}
                out = out[key]
            setKey(out, definition["properties"][subkey], subkey, value)
        elif definition["type"] == "array":
            if definition["items"]["type"] == "object":
                if not key in out:
                    out[key] = [{}]
                elif subkey in out[key][-1]:
                    out[key].append({})
                setKey(out[key][-1], definition["items"], subkey, value, subkey)
            else:
                if not key in out:
                    out[key] = []
                out[key].append(value)
    elif "enum" in definition:
        out[key] = value

def getMetadata(filename, community_id):
    # get the EUDAT metadata schema definition from B2SHARE
    r = requests.get('https://trng-b2share.eudat.eu/api/communities/%s/schemas/last' % community_id)

    # get the required block and metadata fields
    block = json.loads(r.text)['json_schema']['allOf'][0]
    metadata_fields = {k: v for k,v in block["properties"].items() if k[0].isalnum()}

    # read the metadata values from the CSV file
    with open(filename, 'r') as f:
        data = [tuple(l.rstrip('\n').split(';')) for l in f.readlines()]

    # determine the output structure using the schema definition and the metadata values
    out = {}
    for key,sub,value in data:
        setKey(out, metadata_fields[key], key, value, sub)

    # print the result
    return out

def test():
    return getMetadata('eudat-metadata.csv', 'e9b9792e-79fb-4b07-b6b4-b9c2bd06d095')

if __name__ == "__main__":
    test()
