#!/usr/bin/python3
import requests

r = requests.get('http://127.0.0.1:8000/test/../test')
print(r.text)

# Encodings - add orange stuff
dot = ['.','%2e','%u002e']
slash = ['/','%2f','%u002f']
