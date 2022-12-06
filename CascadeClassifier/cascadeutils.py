import os

def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

# reads all the files in the /negative folder and generates neg.txt from them.

# we'll run it manually like this:
# $ python
# >>> from cascadeutils import generate_negative_description_file
# >>> generate_negative_description_file()
# >>> exit()
