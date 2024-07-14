from settings import settings

from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain 

async def chatting(query: str, vector_store, past_requests):
    chat = GigaChat(credentials=f'{settings.GIGACHAT_AUTH}==', verify_ssl_certs=False)

    # defining scale of retriever and generate answer to query
    embedding_retriever = vector_store.as_retriever(search_kwargs={"k": 6})

    prompt = ChatPromptTemplate.from_template("""Ты полезный бот-менеджер.
    Отвечай на вопрос ориентируясь только на контекст. Твой ответ не должен быть длиннее, чем 6 предложений.
    Если в контексте нет информации для ответа, то так и скажи.
    Если в вопросе пользователя несколько предложений, тогда отвечай только на последние.
    Контекст: {context}
    Вопрос: {input}
    Ответ:
    """)

    document_chain = create_stuff_documents_chain(
        llm=chat,
        prompt=prompt
    )

    retrieval_chain = create_retrieval_chain(embedding_retriever, document_chain)

    response = retrieval_chain.invoke(
        {'input': past_requests + query}
        )
    
    print(past_requests + query)

    return response['answer']