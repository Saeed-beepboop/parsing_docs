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
    return lines


# def query(term:str, processed_doc:list):
#     i_list = []
#     p_list = []
#     for phrase_num in range(0,len(processed_doc)):
#         if "I:" in processed_doc[phrase_num]:
#             i_list.append(processed_doc[phrase_num])
#         elif "P:" in processed_doc[phrase_num]:
#             p_list.append(processed_doc[phrase_num])
#     for phrase_num in range(0,len(i_list)):
#         if term in i_list[phrase_num]:
#             return p_list[phrase_num]

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



# Main function
def main():
    with st.container():
        st.markdown("<center><h1>Parsing Documents</h1></center>", unsafe_allow_html=True)

    # st.title("Docx File Uploader")

    # File uploader
    uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

    if uploaded_file is not None:
        # Process the uploaded file
        lines = process_docx(uploaded_file)
        # st.success('Document uploaded successfully!')

        # Display the processed content
        # st.write("Number of paragraphs:", len(paragraphs))
        # st.write("Sample paragraph:", paragraphs[0])
    submitted = st.button("Submit", key="submit_button")

    if submitted:
        with st.spinner('Loading...'):
            #perform prediction
            # proc_doc = process_docx(uploaded_file)
            # st.write("Number of paragraphs:", len(paragraphs))
            # st.write("Sample paragraph:", lines[0])
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
            # st.write("You entered:", user_text)

            st.success('Keyword submitted successfully!')
            phrase_i, phrase_p = query(user_text, lines)
            # st.write("Response", phrase)
            # Display each item of the first list

            st.write(f"List of questions and responses containing '{user_text}':")
            for idx, (item1, item2) in enumerate(zip(phrase_i, phrase_p), start=1):
                st.markdown(f"**Instance {idx}**")
                st.write(f"Question: {item1}")
                st.write(f"Response: {item2}")


            # st.write("Questions:")
            # for item in phrase_i:
            #     st.write(item)

            # # Display each item of the second list
            # st.write("Responses:")
            # for item in phrase_p:
            #     st.write(item)
        else:
            st.write("Please enter a keyword.")






# Run the main function
if __name__ == "__main__":
    main()





    # uploaded_file = st.file_uploader("Upload .docx file", type="docx")
    # if uploaded_file is not None:
    #     file_contents = uploaded_file.getvalue()
    #     st.write("File contents:", file_contents)

    #     st.title("Docx File Uploader")

        # File uploader
    # uploaded_file = st.file_uploader("Upload .docx file", type=["docx"])

    # if uploaded_file is not None:
    #     # Process the uploaded file
    #     paragraphs = process_docx(uploaded_file)

        # with NamedTemporaryFile(dir='.', suffix='.docx') as f:
        #     f.write(uploaded_file.getbuffer())
