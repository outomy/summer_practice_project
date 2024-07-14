import PyPDF2

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


DOCS = {
    'elden_catalog': 'Каталог_товаров_Elden_Ring',
    'wacom_doc': 'Документация_к_графическому_планшету_Wacom_Intuos_Pro_Paper_Edition'
}


async def txt_and_embedding():
    # get text from pdf files
    text = ''
    for i in DOCS:

        with open(f'app/documents/{DOCS[i]}.pdf', 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        text += '\n'

    # write the extracted text to a text file
    with open(f'app/documents/ready_txt/doc.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

    # defining text chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                chunk_overlap=100)
    split_texts = text_splitter.split_text(text)

    # embedding and retriever
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embedding = HuggingFaceEmbeddings(model_name=model_name,
                                    model_kwargs=model_kwargs,
                                    encode_kwargs=encode_kwargs)
    
    vector_store = FAISS.from_texts(split_texts, embedding=embedding)
    
    vector_store.save_local('app/faiss_index')