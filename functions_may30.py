import docx

def process_doc(document):
    doc = docx.Document(document)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    formatted = '\n'.join(fullText)
    lines = [line for line in formatted.split("\n")]
    return lines

def query(term:str, processed_doc:list):
    i_list = []
    p_list = []
    for phrase_num in range(0,len(processed_doc)):
        if "I:" in processed_doc[phrase_num]:
            i_list.append(processed_doc[phrase_num])
        elif "P:" in processed_doc[phrase_num]:
            p_list.append(processed_doc[phrase_num])
    for phrase_num in range(0,len(i_list)):
        if term in i_list[phrase_num]:
            print(p_list[phrase_num])
        # elif term not in i_list[phrase_num]:
        #     return "Term not found."
