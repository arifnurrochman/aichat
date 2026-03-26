import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# Import LangChain versi terbaru yang lebih stabil
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

# Cara panggil RetrievalQA yang paling aman untuk semua versi
from langchain.chains import RetrievalQA

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="My AI Assistant", page_icon="🤖", layout="wide")

# --- 2. SIDEBAR: PENGATURAN & API KEY ---
with st.sidebar:
    st.title("⚙️ Pengaturan AI")
    # Anda bisa langsung mengisi API Key di sini jika tidak ingin mengetik ulang
    # api_key = "sk-xxxxxxxxxxxxxxxx" 
    api_key = st.text_input("Masukkan OpenAI API Key", type="password")
    st.info("Dapatkan key di [platform.openai.com](https://platform.openai.com/)")
    
    st.divider()
    mode = st.radio("Pilih Mode Aplikasi:", ["💬 Chat Biasa (ChatGPT)", "📚 Tanya Jawab PDF (RAG)"])
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 3. LOGIKA UTAMA ---
if not api_key:
    st.warning("⚠️ Silakan masukkan API Key Anda di sidebar untuk memulai.")
else:
    # Inisialisasi Client OpenAI
    client = OpenAI(api_key=api_key)

    # Inisialisasi Riwayat Chat di Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- MODE A: CHAT BIASA (CHATGPT) ---
    if mode == "💬 Chat Biasa (ChatGPT)":
        st.header("💬 AI Chat Assistant")
        st.write("Mode ini berfungsi seperti ChatGPT standar.")

        # Tampilkan riwayat chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input Chat
        if prompt := st.chat_input("Tulis pesan Anda di sini..."):
            # Simpan pesan user
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Respon dari AI
            with st.chat_message("assistant"):
                try:
                    stream = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    )
                    response_text = stream.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    # --- MODE B: TANYA JAWAB PDF (RAG) ---
    elif mode == "📚 Tanya Jawab PDF (RAG)":
        st.header("📚 Chat dengan Dokumen PDF")
        st.write("Unggah PDF, dan AI akan menjawab berdasarkan isi dokumen tersebut.")

        uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")

        if uploaded_file:
            # Fungsi untuk memproses PDF (Caching agar cepat)
            @st.cache_resource
            def prepare_vector_store(file, _key):
                # Baca PDF
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                
                # Potong teks jadi kecil-kecil
                text_splitter = CharacterTextSplitter(
                    separator="\n",
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text)
                
                # Buat Embeddings dan simpan ke FAISS (Vector Store)
                embeddings = OpenAIEmbeddings(openai_api_key=_key)
                vector_db = FAISS.from_texts(chunks, embeddings)
                return vector_db

            try:
                with st.spinner("Sedang membaca dan menganalisis PDF..."):
                    vectorstore = prepare_vector_store(uploaded_file, api_key)
                st.success("✅ PDF Berhasil dianalisis!")

                # Form Pertanyaan
                query = st.text_input("Apa yang ingin Anda ketahui dari dokumen ini?")
                
                if query:
                    # Setup LLM untuk menjawab berdasarkan dokumen
                    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key, temperature=0)
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=vectorstore.as_retriever()
                    )
                    
                    with st.spinner("Mencari jawaban dalam dokumen..."):
                        result = qa_chain.invoke(query)
                        st.write("### Jawaban AI:")
                        st.info(result["result"])
            except Exception as e:
                st.error(f"Gagal memproses PDF: {e}")
