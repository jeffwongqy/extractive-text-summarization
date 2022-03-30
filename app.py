import streamlit as st
import docx2txt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import re
import heapq


import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

###############################################################################
############################ FUNCTION DECLARATION #############################
###############################################################################
# create a function for displaying raw text
def displayRawText(text):
    st.subheader("Original Text:")
    st.info(text)

# create a function for text cleaning
def normalization(text):
    # convert all text into its lower case
    text = text.lower()
    
    # remove all special characters
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    
    # remove all digits 
    text = re.sub(r'[\d]', '', text)
    
    return text

# create a function to find the weighted term frequency
def weightedTF(normalized_text):
    # initialize an empty dict for term frequency 
    term_frequency = dict()
    
    # split the text into individual tokens
    tokenized_text = word_tokenize(normalized_text)
    
    # check the presence of word in the term frequency dict 
    for word in tokenized_text:
        if word not in stopwords.words('english'):
            if word not in term_frequency.keys(): # if word is not found in the term frequency dict, add 1
                term_frequency[word] = 1 
            else:
                term_frequency[word] += 1 # if word is found in the term frequency dict, increment by 1
    
    # find the max term frequency 
    max_tf = max(term_frequency.values())
    
    # find the weighted term frequency 
    for word in term_frequency.keys():
        term_frequency[word] = term_frequency[word] / max_tf
    
    return term_frequency
    

# create a function to find the sentence scores
def sentenceScores(text, normalized_text, weighted_term_frequency):
    
    # tokenized the sentences 
    tokenized_sent = sent_tokenize(text)
    
    # initialized an empty dict for sentence scores
    sentence_scores = dict()
    
    for sent in tokenized_sent:
        for word in word_tokenize(sent.lower()):
            if word in weighted_term_frequency:
                if len(word_tokenize(sent)) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = weighted_term_frequency[word]
                    else:
                        sentence_scores[sent] += weighted_term_frequency[word]
    
    return sentence_scores

# create a function to form a summary text 
def summaryText(sentence_scores):
    # extract the top 5 sentences with highest sentence scores
    summary_sentences = heapq.nlargest(5, sentence_scores, key = sentence_scores.get)
    
    # rejoin the sentences to form a summary text
    summary_text = (' ').join(summary_sentences)
    
    return summary_text

###############################################################################
################################# MAIN ########################################
###############################################################################

# display the title of the page
st.title("Text Summarization")

st.write("""This app uses an extractive text summarization techniques - a novel statistical process of creating a summary from 
         the text using important phrases and sentence from the document and stacking them up to create a summary. """)

# display image
st.image("text_summary_cartoon.jpeg")

# display information
st.info("**NOTE:** You may choose either a single text file or a word document to upload or input a text into the text box and then click on the **Perform Text Summarization** button to perform the text summarization. ")

# prompt the user to upload document files
text_file = st.file_uploader("Choose a file to upload: ", accept_multiple_files = False, type = ['docx', 'txt', 'None'])

# prompt the user to input a text into the text box
input_text = st.text_area("Enter your text here: ", value = "", placeholder = "Enter your text here (e.g. Forensic science, also known as criminalistics, is ...).")

# prompt the user to click on the button to perform text summary
submit_button = st.button("Perform Text Summarization")

if submit_button:
    # check whether if both input text and uploaded file are empties
    if text_file is None and input_text == "":
        st.error("Please choose either a single text file or a word document to upload or input a text into the text box to perform the text summarization. ")
    
    # check whether if both input text and uploaded file are not empties 
    elif text_file is not None and len(input_text) != 0:
        st.error("Please choose either a single text file or a word document to upload or input a text into the text box to perform the text summarization. ")
    
    elif text_file is None and len(input_text) != 0:
        # call the function to display original text
        originalText = input_text
        displayRawText(originalText)
        
        # remove square brackets
        originalText = re.sub(r'[[0-9]*]', ' ', originalText)
        
        # call the function to normalized text
        normalizedText = normalization(originalText)
        
        # call the function to find the weighted term frequency 
        weighted_term_frequency = weightedTF(normalizedText)
        
        # display the weighted term frequency 
        st.subheader("Weighted Term Frequencies")
        st.write(weighted_term_frequency)
        
        # call the function to find the sentence scores
        sentence_scores_ = sentenceScores(originalText, normalizedText, weighted_term_frequency)
        
        # display the sentence scores
        st.subheader("Sentence Scores")
        st.write(sentence_scores_)
        
        # call the function to form a summary text
        summary_text_ = summaryText(sentence_scores_)
        
        # display the text summarization
        st.subheader("Text Summarization")
        st.success(summary_text_)
        
    elif text_file.type == 'text/plain' and input_text == "":
        # read the text file 
        originalText = str(text_file.read(), "utf-8")
        
        # call the function to display original text
        displayRawText(originalText)
        
        # remove square brackets
        originalText = re.sub(r'[[0-9]*]', ' ', originalText)
        
        # call the function to normalized text
        normalizedText = normalization(originalText)
        
        # call the function to find the weighted term frequency 
        weighted_term_frequency = weightedTF(normalizedText)
        
        # display the weighted term frequency 
        st.subheader("Weighted Term Frequencies")
        st.write(weighted_term_frequency)
        
        # call the function to find the sentence scores
        sentence_scores_ = sentenceScores(originalText, normalizedText, weighted_term_frequency)
        
        # display the sentence scores
        st.subheader("Sentence Scores")
        st.write(sentence_scores_)
        
        # call the function to form a summary text
        summary_text_ = summaryText(sentence_scores_)
        
        # display the text summarization
        st.subheader("Text Summarization")
        st.success(summary_text_)
        
    else:
        # read the document file
        originalText = docx2txt.process(text_file)
        
        # call the function to display original text
        displayRawText(originalText)
        
        # remove square brackets
        originalText = re.sub(r'[[0-9]*]', ' ', originalText)
        
        # call the function to normalized text
        normalizedText = normalization(originalText)
        
        # call the function to find the weighted term frequency 
        weighted_term_frequency = weightedTF(normalizedText)
        
        # display the weighted term frequency 
        st.subheader("Weighted Term Frequencies")
        st.write(weighted_term_frequency)
        
        # call the function to find the sentence scores
        sentence_scores_ = sentenceScores(originalText, normalizedText, weighted_term_frequency)
        
        # display the sentence scores
        st.subheader("Sentence Scores")
        st.write(sentence_scores_)
        
        # call the function to form a summary text
        summary_text_ = summaryText(sentence_scores_)
        
        # display the text summarization
        st.subheader("Text Summarization")
        st.success(summary_text_)
    
