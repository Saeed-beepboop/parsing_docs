import streamlit as st
import docx
import string # "string" module is already installed with Python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

import gensim.downloader
from collections import OrderedDict
# from sklearn.feature_extraction.text import CountVectorizer

# Function to read and process the uploaded docx file
def process_docx(file):
    doc = docx.Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    formatted = '\n'.join(fullText)
    lines = [line for line in formatted.split("\n")]
    return lines

def cleaning(sentence):
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    tokenized_sentence = word_tokenize(sentence) ## tokenize
    stop_words = set(stopwords.words('english')) ## define stopwords
    tokenized_sentence_cleaned = [ ## remove stopwords
        w for w in tokenized_sentence if not w in stop_words
    ]
    lemmatized_v = [
        WordNetLemmatizer().lemmatize(word, pos = "v")
        for word in tokenized_sentence_cleaned
    ]
    lemmatized_n = [
        WordNetLemmatizer().lemmatize(word, pos = "n")
        for word in lemmatized_v
    ]
    lemmatized_a = [
        WordNetLemmatizer().lemmatize(word, pos = "a")
        for word in lemmatized_n
    ]
    lemmatized_r = [
        WordNetLemmatizer().lemmatize(word, pos = "r")
        for word in lemmatized_a
    ]
    lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "s")
        for word in lemmatized_r
    ]
    cleaned_sentence = ' '.join(word for word in lemmatized)
    return cleaned_sentence

def query(term:str, processed_doc:list):
    i_list = []
    p_list = []
    i_term = []
    p_term = []
    for phrase_num in range(0,len(processed_doc)):
        if "I:" in processed_doc[phrase_num]:
            i_list.append(processed_doc[phrase_num])
        elif "P:" in processed_doc[phrase_num]:
            p_list.append(processed_doc[phrase_num])
    for phrase_number in range(0,len(i_list)):
        if term in i_list[phrase_number]:
            i_term.append(i_list[phrase_number])
            p_term.append(p_list[phrase_number])
    return i_term, p_term

def separate_interview_sentences(term:str, interview_sentences:list):
    questions_and_answers = []
    current_question = None
    current_answer = None
    for sentence in interview_sentences:
        sentence = sentence.strip()
        if sentence.startswith('I:'):
            if current_question:
                questions_and_answers.append((current_question, current_answer))
            current_question = sentence
            current_answer = None
        else:
            if not current_question:
                continue
            if current_answer is None:
                current_answer = sentence
            else:
                current_answer += ' ' + sentence
    if current_question:
        questions_and_answers.append((current_question, current_answer))
    term = cleaning(term)
    term = term.split(",")
    lem_user = []
    for t in term:
        lem_user.append(cleaning(t))
    lem_user = lem_user[0].split(' ')
    i_term = []
    p_term = []
    for phrase_number in range(0,len(questions_and_answers)):
        if all(term in cleaning(questions_and_answers[phrase_number][0]) for term in tuple(lem_user)):
            i_term.append(questions_and_answers[phrase_number][0])
            p_term.append(questions_and_answers[phrase_number][1])
    return i_term, p_term

def tidy_text(user_catsubcat):
    user_subcat_sep = user_catsubcat.splitlines()
    user_subcat_sep_clean = []
    for i in user_subcat_sep:
        i.strip()
        user_subcat_sep_clean.append(i)
    particular_value = ''
    result = []
    temp_list = []
    for i in user_subcat_sep_clean:
        if i == particular_value:
            temp_list.append(i)
            result.append(temp_list)
            temp_list = []
        else:
            temp_list.append(i)
    result.append(temp_list)
    for list in result:
        if '' in list:
            list.remove('')
    return result








# CHECK THIS PART OUT - transferred from word2vec_testing.ipynb

## imports

# print(list(gensim.downloader.info()['models'].keys()))
# model_wiki = gensim.downloader.load('glove-wiki-gigaword-50')
# N.B. Words not in glove-wiki-gigaword-50 will not have vectors computed
# example_1 = model_wiki["queen"] - model_wiki["king"] + model_wiki["man"]
# model_wiki.most_similar(example_1)

# def cleaning(sentence):
#     sentence = sentence.strip() ## remove whitespaces
#     sentence = sentence.lower() ## lowercase
#     for punctuation in string.punctuation:
#         sentence = sentence.replace(punctuation, '') ## remove punctuation
#     tokenized_sentence = word_tokenize(sentence) ## tokenize
#     stop_words = set(stopwords.words('english')) ## define stopwords
#     tokenized_sentence_cleaned = [
#         w for w in tokenized_sentence if not w in stop_words
#     ]
#     lemmatized_n = [
#         WordNetLemmatizer().lemmatize(word, pos = "n")
#         for word in tokenized_sentence_cleaned
#     ]
#     lemmatized_v = [
#         WordNetLemmatizer().lemmatize(word, pos = "v")
#         for word in lemmatized_n
#     ]
#     lemmatized_a = [
#         WordNetLemmatizer().lemmatize(word, pos = "a")
#         for word in lemmatized_v
#     ]
#     lemmatized_r = [
#         WordNetLemmatizer().lemmatize(word, pos = "r")
#         for word in lemmatized_a
#     ]
#     lemmatized = [
#         WordNetLemmatizer().lemmatize(word, pos = "s")
#         for word in lemmatized_r
#     ]
#     cleaned_sentence = ' '.join(word for word in lemmatized)
#     return cleaned_sentence

# def result_cleaning(model: str, model_results: list, n_top_results=20, search_term: str):
# def result_cleaning(model: str, search_term: str, n_top_results=20):
#     cleaned_list = []
#     this_model = gensim.downloader.load(model)
#     example = this_model[search_term]
#     this_model.most_similar(example)
#     similarities = this_model.most_similar(example, topn=n_top_results)
#     for w in similarities:
#         word = w[0]
#         cleaned_word = cleaning(word)
#         cleaned_list.append(cleaned_word)
#     cleaned_list = [*(OrderedDict.fromkeys(cleaned_list)).keys()]
#     for i in cleaned_list:
#         if i == '':
#             cleaned_list.remove(i)
#     return cleaned_list
    # return result_cleaning(this_model, example)

def result_cleaning(model: str, search_term: str, n_top_results=20):
    cleaned_list = []
    this_model = gensim.downloader.load(model)
    example = this_model[search_term]
    similarities = this_model.most_similar(example, topn=n_top_results)
    for w in similarities:
        word = w[0]
        cleaned_word = cleaning(word)
        cleaned_list.append(cleaned_word)
    cleaned_dict = dict.fromkeys(cleaned_list)
    cleaned_list = [*cleaned_dict]
    for i in cleaned_list:
        if i == '':
            cleaned_list.remove(i)
    return cleaned_list

genism_models = ['fasttext-wiki-news-subwords-300',
                 'conceptnet-numberbatch-17-06-300',
                 'word2vec-ruscorpora-300',
                 'word2vec-google-news-300',

                 'glove-wiki-gigaword-50', # Best one apparently

                 'glove-wiki-gigaword-100',
                 'glove-wiki-gigaword-200',
                 'glove-wiki-gigaword-300',
                 'glove-twitter-25',
                 'glove-twitter-50',
                 'glove-twitter-100',
                 'glove-twitter-200',
                 '__testing_word2vec-matrix-synopsis']

# for i in range(0, len(genism_models)):
#     print(genism_models[i])
# def synonym_finder(model: str, search_term: str):
#     # model_4 = genism_models[4]
#     this_model = gensim.downloader.load(model)
#     example = this_model[search_term]
#     this_model.most_similar(example)
#     return result_cleaning(this_model, example)

# print(f'Results from {model_4} model')
# print(this_model_4.most_similar(example_4))
# result_cleaning(this_model_4, example_4)


def approximate_responses(term:str, interview_sentences:list):
    questions_and_answers = []
    current_question = None
    current_answer = None
    for sentence in interview_sentences:
        sentence = sentence.strip()
        if sentence.startswith('I:'):
            if current_question:
                questions_and_answers.append((current_question, current_answer))
            current_question = sentence
            current_answer = None
        else:
            if not current_question:
                continue
            if current_answer is None:
                current_answer = sentence
            else:
                current_answer += ' ' + sentence
    if current_question:
        questions_and_answers.append((current_question, current_answer))

    term = cleaning(term)
    term = term.split(",")
    lem_user = []
    for t in term:
        lem_user.append(cleaning(t))
    lem_user = lem_user[0].split(' ')

    comprehensive_list = [] + lem_user
    for q in lem_user:
        try:
            similar_word = result_cleaning(genism_models[4], q)
        except KeyError as e:
            print(f"No synonyms were considered for '{q}'.")
            continue
        comprehensive_list.extend(similar_word)
        seen = set()
        unique_list = [x for x in comprehensive_list if not (x in seen or seen.add(x))]

    i_term = []
    p_term = []
    for phrase_number in range(0,len(questions_and_answers)):
        if all(term in cleaning(questions_and_answers[phrase_number][0]) for term in tuple(unique_list)):
            i_term.append(questions_and_answers[phrase_number][0])
            p_term.append(questions_and_answers[phrase_number][1])

    return i_term, p_term, unique_list
    # return unique_list








# def separate_qa(interview_sentences:list):
def separate_qa(interview_sentences:list, term:str):

    questions_and_answers = []
    current_question = None
    current_answer = None
    for sentence in interview_sentences:
        sentence = sentence.strip()
        if sentence.startswith('I:'):
            if current_question:
                questions_and_answers.append((current_question, current_answer))
            current_question = sentence
            current_answer = None
        else:
            if not current_question:
                continue
            if current_answer is None:
                current_answer = sentence
            else:
                current_answer += ' ' + sentence
    if current_question:
        questions_and_answers.append((current_question, current_answer))

    # return questions_and_answers

# def get_synonyms(term:str):

    term = cleaning(term)
    term = term.split(",")
    lem_user = []
    for t in term:
        lem_user.append(cleaning(t))
    lem_user = lem_user[0].split(' ')

    comprehensive_list = [] + lem_user
    for q in lem_user:
        try:
            similar_word = result_cleaning(genism_models[4], q)
        except KeyError as e:
            print(f"No synonyms were considered for '{q}'.")
            continue
        comprehensive_list.extend(similar_word)
        seen = set()
        unique_list = [x for x in comprehensive_list if not (x in seen or seen.add(x))]

    # return unique_list

# def get_responses_syns(qa:list, syns:list):
    # questions_and_answers = qa
    # syns = unique_list
    i_term = []
    p_term = []
    for phrase_number in range(0,len(questions_and_answers)):
        if any(term in cleaning(questions_and_answers[phrase_number][0]) for term in tuple(unique_list)):
            i_term.append(questions_and_answers[phrase_number][0])
            p_term.append(questions_and_answers[phrase_number][1])

    return i_term, p_term, unique_list


# def main():
#     with st.container():
#         st.markdown("<center><h1>Parsing Documents</h1></center>", unsafe_allow_html=True)

#         # File uploader
#     uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

#     if uploaded_file is not None:
#         # Process the uploaded file
#         lines = process_docx(uploaded_file)

#         # Display the processed content
#     submitted = st.button("Submit", key="submit_button")

#     if submitted:
#         with st.spinner('Loading...'):
#             st.success('Document submitted successfully!')
#             st.write("First paragraph:")
#             st.write(lines[0])

#     st.subheader("Query interviewee responses based on a keyword")
#     st.subheader("Add categories and subcategories")

#     # Text input field
#     user_text = st.text_area('Enter the categories, separated by paragraphs, and subcategories separated by linebreaks', height=350)

#     outcome = tidy_text(user_text)

#     # Submit button
#     if st.button("Submit Search Terms"):
#         # Process the entered text when the submit button is clicked
#         if user_text:
#             st.success('Categories and subcategories submitted successfully!')
#             st.write(f"List of questions and responses containing the following categories and subcategories:")
#             catsubcat_dict = {}
#             for cats in outcome:
#                 catsubcat_dict[cats[0]] = cats[1:]

#             listkeys_catsubcat_dict = []
#             for key in catsubcat_dict.keys():
#                 listkeys_catsubcat_dict.append(key)

#             for num in range(0,len(catsubcat_dict.keys())):
#                 cat = f"**Category {num+1}**: {listkeys_catsubcat_dict[num]}"
#                 st.write(cat)
#                 for n in range(0,len(catsubcat_dict[listkeys_catsubcat_dict[num]])):
#                     subcat = f"**Subcategory {n+1}**: {catsubcat_dict[listkeys_catsubcat_dict[num]][n]}"
#                     st.markdown(subcat)

#                     with st.spinner('Parsing...'):

#                         # st.markdown(approximate_responses(catsubcat_dict[listkeys_catsubcat_dict[num]][n], lines))

#                         # phrase_i, phrase_p = separate_interview_sentences(catsubcat_dict[listkeys_catsubcat_dict[num]][n], lines)
#                         # phrase_i, phrase_p, synonyms = approximate_responses(catsubcat_dict[listkeys_catsubcat_dict[num]][n], lines)
#                         synonyms = get_synonyms(catsubcat_dict[listkeys_catsubcat_dict[num]][n])
#                         # st.markdown(f"Synonyms considered: {synonyms}")
#                         st.markdown(f"Synonyms considered:")


#                         # SEPARATE THE FUNCTIONS THAT GET THE LISTS TO SEARCH FOR and SYNONYMS TO USE THE SYNONMS HERE SEPARATELY

#                         fields = st.multiselect('Select the synonyms to search by', synonyms)

#                         phrase_i, phrase_p = get_responses_syns(separate_qa(lines), fields)

#                         # Display each item of the first list
#                         # st.write(f"List of questions and responses containing '{user_text}':")

#                         for idx, (item1, item2) in enumerate(zip(phrase_i, phrase_p), start=1):
#                             st.markdown(f"{cat}, {subcat}, **Instance {idx}**")
#                             st.write(f"Question: {item1}")
#                             st.write(f"Response: {item2}")

#         else:
#             st.write("Please enter a category and a subcategory.")



def main():
    with st.container():
        st.markdown("<center><h1>Parsing Documents</h1></center>", unsafe_allow_html=True)

        # File uploader
    uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

    if uploaded_file is not None:
        # Process the uploaded file
        lines = process_docx(uploaded_file)

        # Display the processed content
    submitted = st.button("Submit", key="submit_button")

    if submitted:
        with st.spinner('Loading...'):
            st.success('Document submitted successfully!')
            st.write("First paragraph:")
            st.write(lines[0])

    st.subheader("Query interviewee responses based on a keyword")
    st.subheader("Add categories and subcategories")

    # Text input field
    user_text = st.text_area('Enter the categories, separated by paragraphs, and subcategories separated by linebreaks', height=350)

    outcome = tidy_text(user_text)

    # Submit button
    if st.button("Submit Search Terms"):
        # Process the entered text when the submit button is clicked
        if user_text:
            st.success('Categories and subcategories submitted successfully!')
            st.write(f"List of questions and responses containing the following categories and subcategories:")
            catsubcat_dict = {}
            for cats in outcome:
                catsubcat_dict[cats[0]] = cats[1:]

            listkeys_catsubcat_dict = []
            for key in catsubcat_dict.keys():
                listkeys_catsubcat_dict.append(key)

            for num in range(0,len(catsubcat_dict.keys())):
                cat = f"**Category {num+1}**: {listkeys_catsubcat_dict[num]}"
                st.write(cat)
                for n in range(0,len(catsubcat_dict[listkeys_catsubcat_dict[num]])):
                    subcat = f"**Subcategory {n+1}**: {catsubcat_dict[listkeys_catsubcat_dict[num]][n]}"
                    st.markdown(subcat)
                    with st.spinner('Loading Synonyms...'):
                        phrase_i, phrase_p, unique_list= separate_qa(lines, catsubcat_dict[listkeys_catsubcat_dict[num]][n])

                        # synonyms = get_synonyms(catsubcat_dict[listkeys_catsubcat_dict[num]][n])
                        st.markdown("Synonyms considered:")
                        st.markdown(unique_list)

                        # fields = st.multiselect('Select the synonyms to search by', synonyms)

                        # if st.button("Submit", key=f"Synonyms for {catsubcat_dict[listkeys_catsubcat_dict[num]][n]}"):


                        #     # PROBLEM: PAGE RESETS AS SOON AS I CHOOSE AN OPTION


                        #     if fields:
                        #         st.success('Synonyms submitted successfully!')
                        st.write("Results:")
                        with st.spinner('Parsing...'):
                            # phrase_i, phrase_p = get_responses_syns(separate_qa(lines), fields)

                            for idx, (item1, item2) in enumerate(zip(phrase_i, phrase_p), start=1):
                                st.markdown(f"{cat}, {subcat}, **Instance {idx}**")
                                st.write(f"Question: {item1}")
                                st.write(f"Response: {item2}")
                            # else:
                            #     st.write(f"Choose a synonym.")
        else:
            st.write("Please enter a category and a subcategory.")






# submitted = st.button("Submit", key="submit_button")
# if submitted:
#     if user_text:
#         st.success('Parameters, search terms, and fields submitted successfully!')
#         parameters = {}
#         for p, t in zip(params, user_text):
#             parameters[p] = t

#         parameters['limit'] = limit

#         if not fields:
#                 fields = 'all'
#         st.write("Results:")
#         with st.spinner('Calculating...'):





# Run the main function
if __name__ == "__main__":
    main()
