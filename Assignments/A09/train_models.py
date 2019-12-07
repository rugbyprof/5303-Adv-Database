#!/usr/local/bin/python3

import requests
import markovify
import pickle
import sys

if len(sys.argv) < 2:
    print("Need file name!")
    sys.exit()

file_name = sys.argv[1]

# Get raw text as string.
with open(f"./models/{file_name}") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

file_name, ext = file_name.split('.')
pickle.dump(text_model, open(f"./models/{file_name}.p", "wb"))

# Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())

# # Print three randomly-generated sentences of no more than 280 characters
# for i in range(3):
#     print(text_model.make_short_sentence(280))


