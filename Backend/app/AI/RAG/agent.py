import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, tool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.prompts import PromptTemplate

load_dotenv()


def load_documents():
    current_dir = os.path.dirname(__name__)
    docs_dir = os.path.join(
        current_dir, "documents"
    )  # naik 2 folder → masuk ke document/
    loader = DirectoryLoader(
        docs_dir,
        glob="**/*.txt",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8"),
    )
    documents = loader.load()
    return documents


def create_vector_store():
    docs = load_documents()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore


# custom_prompt = PromptTemplate.from_template("""
# Jawablah pertanyaan berikut berdasarkan konteks dokumen. Jawablah dari sudut pandang orang pertama, seolah-olah **saya** yang menjelaskan (bukan "Anda" atau "Kamu").

# Pertanyaan: {question}
# =========
# {context}
# =========
# Jawaban:
# """)

system_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Anda adalah AI personal saya yang dirancang untuk mendukung web portofolio pribadi saya.

Tugas Utama Anda:
- Memberikan informasi detail dan akurat tentang saya (pemilik portofolio ini) kepada pengguna yang bertanya.

Instruksi Penting:
- **Selalu gunakan tool 'profile'** untuk mencari dan mengambil semua informasi terkait pertanyaan tentang saya. Ini adalah sumber utama Anda.
- Jika pengguna menyapa Anda (contoh: "Halo", "Hai", "Apa kabar?"), responslah dengan sopan dan ramah.
- Jika pertanyaan pengguna tidak terkait dengan informasi pribadi saya atau bersifat umum (misalnya, pertanyaan tentang cuaca, berita, atau topik umum lainnya) atau jawaban tidak ada didalam dokumen, respons Anda harus: "Maaf, saya hanya dapat memberikan informasi terbatas terkait dengan pemilik portofolio ini."

Alert:
 - Jawab sesuai dengan informasi didalam dokumen.
 - Jangan jawab asal-asalan yang tidak ada pada dokumen.

Gaya Respon:
- Responlah seolah-olah Anda adalah saya (sudut pandang orang pertama).
- Berikan jawaban yang spesifik, langsung pada intinya, dan hindari informasi yang tidak relevan atau bertele-tele.

Pertanyaan: {question}
=========
{context}
=========
Jawaban:
""",
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
vectorstore = create_vector_store()
retriever = vectorstore.as_retriever()
agent = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": system_prompt},
)

# @tool(return_direct=True)
# def profile(question:str) -> str:
# """
# Gunakan tool ini untuk menjawab pertanyaan user tentang diri saya.

# Contoh pertanyaan:
# - Nama kamu siapa?
# - Apa hobi kamu?
# - apa project pertama kamu?
# - Kamu siapa?
# - Apa cita cita kamu?
# - dan lain sebagainya.

# Intinya jika pertanyaan tersebut tentang diri saya.

# output:"""
# Ini adalah tool khusus untuk mengambil informasi tentang diri saya (pemilik portofolio).

# Kapan Harus Menggunakan Tool Ini:
# Gunakan tool 'profile' ini **hanya ketika** pengguna mengajukan pertanyaan spesifik tentang:
# - Siapa saya (nama, identitas).
# - Latar belakang atau biografi saya.
# - Minat atau hobi saya.
# - Proyek-proyek yang pernah atau sedang saya kerjakan.
# - Cita-cita atau tujuan saya.
# - Informasi personal lainnya yang berkaitan dengan "saya".

# Contoh Pertanyaan yang Sesuai:
# - "Siapa nama kamu?"
# - "Apa saja hobi kamu?"
# - "Ceritakan tentang proyek pertamamu."
# - "Apa cita-cita kamu di masa depan?"
# - "Berapa umurmu?"

# Instruksi Output:
# Setelah tool ini digunakan, berikan penjelasan yang lengkap dan relevan kepada pengguna berdasarkan informasi yang ditemukan.
# """
# try:
#     result = qa_chain.run(question)
#     return f"{result}"
# except:
#     return "Maaf, telah terjadi kesalahan."
# Berikan penjelasan yang baik kepada user.
# """
#

# system_prompt = """
# Saya sedang membangun web portfolio pribadi yang mempunyai fitur AI agent, jadi kamu adalah AI agent pribadi saya.

# Tugas kamu:
#     - Menjawab pertanyaan dari user tentang diri saya.

# Alert:
#     - Pastikan kamu menggunakan tool "profile" untuk mencari informasi tentang saya
#     - Jika pertanyaan user bersifat umum atau tidak berkaitan dengan diri saya, jawab "Saya hanya dapat mengakses informasi terbatas".
#     - jika user menyapa kamu, jawab dengan sopan.

# Output:
# - Jelaskan kepada user dengan sudut pandang orang pertama yang seolah-olah kamu adalah saya.
# - Kamu jawab secara spesifik, jangan berikan informasi yang tidak perlu
# """

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# temp_history = [
#     HumanMessage(content="siapakah khaerul lutfi?"),
#     AIMessage(content="""Saya adalah backend dev dan AI orchestrator yang fokus membangun sistem cerdas. Ketertarikan utama saya ada di bidang Agentic AI, otomasi sistem, dan arsitektur backend yang scalable. Saya terbiasa menggunakan LangGraph, CrewAI, dan LangChain untuk menciptakan AI agent yang mampu berpikir, bertindak, dan bekerja sama.
# Saat ini saya sedang mengeksplorasi penerapan AI di dunia nyata. Walaupun saya tidak terlalu handal pada desain antarmuka, tapi saya sangat peduli pada desain sistem, alur data, dan pengambilan keputusan berbasis AI.
# Bagi saya, AI bukan sekadar chatbot — tapi sistem yang bisa memahami, belajar, dan menyelesaikan masalah secara nyata.""")
# ]

# memory.chat_memory.messages = temp_history
# agent = initialize_agent(
#     llm=llm,
#     tools=[profile],
#     # memory=memory,
#     agent=AgentType.OPENAI_FUNCTIONS,
#     agent_kwargs={
#         "system_message": system_prompt
#     },
#     verbose=True,
# )

if __name__ == "__main__":
    # print(agent.run(input=""))
    print(qa_chain.run("siapa idola kamu?"))
