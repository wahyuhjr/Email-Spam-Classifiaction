# Read the txt file.
with open('text-email.txt', 'r') as email:
    file_contents = email.read()

file_contents

import re
from string import punctuation
from nltk.stem.snowball import SnowballStemmer

# Create a function to read the fixed vocab list.
def getVocabList():
    """
    Reads the fixed vocabulary list in vocab.txt
    and returns a dictionary of the words in vocabList.
    """
    # Read the fixed vocabulary list.
    with open('vocab.txt', 'r') as vocab:
        
        # Store all dictionary words in dictionary vocabList.
        vocabList = {}
        for line in vocab.readlines():
            i, word = line.split()
            vocabList[word] = int(i)

    return vocabList

# Create a function to process the email contents.
def processEmail(email_contents):
    """
    Preprocesses the body of an email and returns a
    list of indices of the words contained in the email.
    Args:
        email_contents: str
    Returns:
        word_indices: list of ints
    """
    # Load Vocabulary.
    vocabList = getVocabList()

    # Init return value.
    word_indices = []
    
    # ============================ Preprocess Email ============================

    # Find the Headers ( \n\n and remove ).
    # Uncomment the following lines if you are working with raw emails with the
    # full headers.

    # hdrstart = email_contents.find("\n\n")
    # if hdrstart:
    #     email_contents = email_contents[hdrstart:]

    # Convert to lower case.
    email_contents = email_contents.lower()

    # Strip all HTML.
    # Look for any expression that starts with < and ends with > and
    # does not have any < or > in the tag and replace it with a space.
    email_contents = re.sub('<[^<>]+>', ' ', email_contents)

    # Handle Numbers.
    # Look for one or more characters between 0-9.
    email_contents = re.sub('[0-9]+', 'number', email_contents)

    # Handle URLS.
    # Look for strings starting with http:// or https://.
    email_contents = re.sub('(http|https)://[^\s]*', 'httpaddr', email_contents)

    # Handle Email Addresses.
    # Look for strings with @ in the middle.
    email_contents = re.sub('[^\s]+@[^\s]+', 'emailaddr', email_contents)

    # Handle $ sign.
    # Look for "$" and replace it with the text "dollar".
    email_contents = re.sub('[$]+', 'dollar', email_contents)


    # ============================ Tokenize Email ============================

    # Output the email to screen as well.
    print('\n==== Processed Email ====\n')

    # Process file
    l = 0
    
    # Get rid of any punctuation.
    email_contents = email_contents.translate(str.maketrans('', '', punctuation))

    # Split the email text string into individual words.
    email_contents = email_contents.split()

    for token in email_contents:

        # Remove any non alphanumeric characters.
        token = re.sub('[^a-zA-Z0-9]', '', token)
        
        # Create the stemmer.
        stemmer = SnowballStemmer("english")
        
        # Stem the word.
        token = stemmer.stem(token.strip())

        # Skip the word if it is too short
        if len(token) < 1:
           continue
        
        # Look up the word in the dictionary and add to word_indices if found.
        if token in vocabList:
            idx = vocabList[token]
            word_indices.append(idx)

        # ====================================================================

        # Print to screen, ensuring that the output lines are not too long.
        if l + len(token) + 1 > 78:
            print()
            l = 0
        print(token, end=' ')
        l = l + len(token) + 1

    # Print footer.
    print('\n\n=========================\n')

    return word_indices


# Extract features.
word_indices = processEmail(file_contents)

# Print stats.
print('Word Indices: \n')
print(word_indices)
print('\n\n')