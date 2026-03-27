import streamlit as st

<<<<<<< HEAD
# Impor LangChain standar modern 2026
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import RetrievalQA

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Assistant SMK Voctech 2", layout="wide")

# CSS Custom untuk tampilan lebih profesional
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f9; }
    .main-header { color: #1E3A8A; font-size: 30px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. PENGATURAN API KEY (SECRETS) ---
# Mengambil API Key dari Streamlit Cloud Secrets secara otomatis
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    # Jika dijalankan di localhost dan belum ada secrets
    openai_api_key = st.sidebar.text_input("Masukkan OpenAI API Key", type="password")

# --- 3. FUNGSI PENGOLAH PDF ---
def process_pdf(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Memecah teks menjadi potongan kecil (chunks)
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Membuat Vector Store menggunakan FAISS
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

# --- 4. TAMPILAN UTAMA (UI) ---
st.markdown('<p class="main-header">🤖 AI Chat Assistant & RAG PDF</p>', unsafe_allow_html=True)

# Sidebar untuk navigasi dan upload
with st.sidebar:
    st.title("Pengaturan AI")
    app_mode = st.radio("Pilih Mode:", ["Chat Biasa", "Tanya Jawab PDF (RAG)"])
    
    if app_mode == "Tanya Jawab PDF (RAG)":
        uploaded_files = st.file_uploader("Upload Dokumen PDF Sekolah", accept_multiple_files=True)
        if st.button("Proses Dokumen"):
            if openai_api_key:
                with st.spinner("Sedang mempelajari dokumen..."):
                    st.session_state.vectorstore = process_pdf(uploaded_files)
                    st.success("Dokumen siap didiskusikan!")
            else:
                st.error("Masukkan API Key terlebih dahulu!")

    if st.button("Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
=======
# --- 0. AUTO-INSTALL LIBRARY (STANDAR 2026) ---
# Baris ini membantu server Streamlit mengenali library jika requirements.txt bermasalah
# [st.requirement: streamlit, openai, PyPDF2, langchain, langchain-community, langchain-openai, langchain-text-splitters, faiss-cpu]

try:
    from openai import OpenAI
    from PyPDF2 import PdfReader
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import CharacterTextSplitter
    # Cara impor RetrievalQA yang paling aman untuk Python 3.11/3.12
    from langchain.chains import RetrievalQA
except ImportError as e:
    st.error(f"Server sedang menyiapkan library: {e}. Silakan tunggu 1-2 menit lalu klik 'Reboot App' di menu kanan bawah.")
    st.stop()

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Assistant SMK Voctech 2", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f5f7f9; }
    .main-header { color: #1E3A8A; font-size: 30px; font-weight: bold; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. PENGATURAN API KEY (SECRETS) ---
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai_api_key = st.sidebar.text_input("Masukkan OpenAI API Key", type="password")

# --- 3. FUNGSI PENGOLAH PDF ---
def process_pdf(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

# --- 4. TAMPILAN UTAMA (UI) ---
st.markdown('<p class="main-header">🤖 AI Assistant SMK Voctech 2</p>', unsafe_allow_html=True)

with st.sidebar:
    st.title("Menu Utama")
    app_mode = st.radio("Pilih Mode:", ["Chat Biasa", "Tanya Jawab PDF (RAG)"])
    
    if app_mode == "Tanya Jawab PDF (RAG)":
        st.info("Upload dokumen (Kurikulum, Tata Tertib, dll) agar AI bisa menjawab berdasarkan data tersebut.")
        uploaded_files = st.file_uploader("Upload PDF", accept_multiple_files=True, type=['pdf'])
        if st.button("Proses Dokumen"):
            if openai_api_key and uploaded_files:
                with st.spinner("Sedang membaca dokumen..."):
                    st.session_state.vectorstore = process_pdf(uploaded_files)
                    st.success("Dokumen berhasil dipelajari!")
            else:
                st.warning("Pastikan API Key sudah diisi dan file sudah dipilih.")

    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

<<<<<<< HEAD
# Input Chat dari User
if prompt := st.chat_input("Tulis pesan Anda di sini..."):
    if not openai_api_key:
        st.info("Silakan masukkan OpenAI API Key untuk melanjutkan.")
        st.stop()

    # Simpan pesan user
=======
if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    if not openai_api_key:
        st.error("API Key belum terpasang di Secrets!")
        st.stop()

>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

<<<<<<< HEAD
    # Respon AI
=======
>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
    with st.chat_message("assistant"):
        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
            
<<<<<<< HEAD
            # Mode RAG (Tanya Jawab PDF)
=======
>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
            if app_mode == "Tanya Jawab PDF (RAG)" and "vectorstore" in st.session_state:
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=st.session_state.vectorstore.as_retriever()
                )
                response = qa_chain.run(prompt)
<<<<<<< HEAD
            
            # Mode Chat Biasa
=======
>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
            else:
                client = OpenAI(api_key=openai_api_key)
                api_res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                response = api_res.choices[0].message.content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
<<<<<<< HEAD
            st.error(f"Terjadi kesalahan: {str(e)}")
=======
            st.error(f"Error: {str(e)}")
>>>>>>> 06a58e9 (Update ai_app.py dengan versi stabil 2026)
