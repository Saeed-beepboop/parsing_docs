import streamlit as st
import docx

# Function to read and process the uploaded docx file
def process_docx(file):
    doc = docx.Document(file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    formatted = '\n'.join(fullText)
    lines = [line for line in formatted.split("\n")]
    # return lines
    return fullText

def query(term:str, processed_doc:list):
# def separate_interview_sentences(processed_doc:list, term:str):
    questions_and_answers = []
    current_question = None
    current_answer = None

    for sentence in processed_doc:
        # Remove leading/trailing whitespaces
        sentence = sentence.strip()

        # If the sentence ends with a question mark or a colon,
        # it's likely a question
        # if sentence.endswith('?') or sentence.endswith(':'):
        # for para_num in range(0,len(processed_doc)):
        if sentence.startswith('I:'):
        # if "I:" in processed_doc[para_num]:
            # sentence = processed_doc[para_num]
            # If there was a previous question, add it to the list with its answer
            if current_question:
                questions_and_answers.append((current_question, current_answer))
            # Set the new question
            current_question = sentence
            # Reset the current answer
            current_answer = None
        # Otherwise, it's likely an answer to the previous question
        else:
            # If there's no question yet, skip this sentence
            if not current_question:
                continue
            # If there's no answer yet, initialize it with this sentence
            if current_answer is None:
                current_answer = sentence
            # If there's already an answer, concatenate this sentence to it
            else:
                current_answer += ' ' + sentence

    # Add the last question and its answer to the list
    if current_question:
        questions_and_answers.append((current_question, current_answer))

    # return questions_and_answers
    i_term = []
    p_term = []
    for phrase_number in range(0,len(questions_and_answers)):
        if term in questions_and_answers[phrase_number][0]:
            # i_term.append(i_list[phrase_number])
            # p_term.append(p_list[phrase_number])
            i_term.append(questions_and_answers[phrase_number][0])
            p_term.append(questions_and_answers[phrase_number][1])
    return i_term, p_term
    #         i_term = questions_and_answers[phrase_number]
    # return i_term













# Main function
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

    # Text input field
    user_text = st.text_input("Enter the keyword:")

    # Submit button
    if st.button("Submit"):
        # Process the entered text when the submit button is clicked
        if user_text:
            st.success('Keyword submitted successfully!')
            phrase_i, phrase_p = query(user_text, lines)
            # Display each item of the first list
            st.write(f"List of questions and responses containing '{user_text}':")
            for idx, (item1, item2) in enumerate(zip(phrase_i, phrase_p), start=1):
                st.markdown(f"**Instance {idx}**")
                st.write(f"Question: {item1}")
                st.write(f"Response: {item2}")
        else:
            st.write("Please enter a keyword.")

# Run the main function
if __name__ == "__main__":
    main()
