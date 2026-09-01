import os
import math
import glob
import gradio as gr
from foundry_local_sdk import Configuration, FoundryLocalManager

DOCS_DIR = "docs"

# Dokümanları okuyup token sınırına takılmamak için parçalara bölüyoruz
def load_and_chunk_documents(docs_dir, chunk_size=500):
    chunks = []
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        return chunks

    # Tüm .txt ve .md dosyalarını bul
    files = glob.glob(os.path.join(docs_dir, "*.txt")) + glob.glob(os.path.join(docs_dir, "*.md"))
    
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Paragraflara ayır
            paragraphs = content.split("\n\n")
            current_chunk = ""
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                # chunk boyutu sınırını aşıyorsa yeni chunk'a geç
                if len(current_chunk) + len(para) > chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = para
                else:
                    current_chunk += "\n" + para if current_chunk else para
            
            # Kalan son chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
                
    return chunks

# Vektörler arası benzerlik hesabı
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

# En alakalı dokümanları bulma
def find_relevant(query_embedding, doc_embeddings, top_k=2):
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((i, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

# Global Değişkenler
manager = None
embedding_client = None
chat_client = None
doc_chunks = []
doc_embeddings = []

def initialize_ai():
    global manager, embedding_client, chat_client, doc_chunks, doc_embeddings
    print("Foundry Local başlatılıyor...")
    
    config = Configuration(app_name="foundry_local_rag_ui")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    
    # Modelleri yükle
    print("Modeller yükleniyor (Lütfen bekleyin)...")
    
    emb_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    emb_model.download()
    emb_model.load()
    embedding_client = emb_model.get_embedding_client()
    
    chat_model = manager.catalog.get_model("phi-3.5-mini")
    chat_model.download()
    chat_model.load()
    chat_client = chat_model.get_chat_client()
    
    print("Modeller hazır. Dokümanlar indeksleniyor...")
    
    # Dokümanları oku ve indeksle
    doc_chunks = load_and_chunk_documents(DOCS_DIR)
    
    if not doc_chunks:
        print(f"Uyarı: {DOCS_DIR} klasöründe doküman bulunamadı. Lütfen .txt veya .md ekleyin.")
    else:
        response = embedding_client.generate_embeddings(doc_chunks)
        doc_embeddings = [item.embedding for item in response.data]
        print(f"Toplam {len(doc_chunks)} parça başarıyla indekslendi.")

def chat_interface(message, history):
    global embedding_client, chat_client, doc_chunks, doc_embeddings
    
    if not message.strip():
        return "Lütfen geçerli bir soru sorun."
        
    if not doc_chunks:
        return f"Şu an veri tabanında doküman yok. Lütfen '{DOCS_DIR}' klasörüne .txt dosyaları ekleyin ve uygulamayı yeniden başlatın."
        
    # Sorguyu vektöre çevir
    query_response = embedding_client.generate_embedding(message)
    query_embedding = query_response.data[0].embedding
    
    # En alakalı 2 parçayı getir (retrieval)
    results = find_relevant(query_embedding, doc_embeddings, top_k=2)
    context = "\n\n".join(f"- {doc_chunks[i]}" for i, _ in results)
    
    # Modele bağlamı ve görevi verdiğimiz prompt
    system_prompt = (
        "Sen yerel çalışan akıllı bir asistansın. "
        "Sana sağlanan 'Bağlam' bilgilerini kullanarak kullanıcının sorusuna net, anlaşılır ve doğru cevaplar ver. "
        "Eğer sorunun cevabı bağlamda yoksa, bunu açıkça belirt ve uydurma. "
        f"\n\nBağlam:\n{context}"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    
    # Gradio history listesini (önceki mesajlar) formata uygun ekle
    for item in history:
        if isinstance(item, dict):  # Gradio 5+ formatı
            messages.append(item)
        elif isinstance(item, (list, tuple)) and len(item) == 2: # Gradio 3/4 formatı
            user_msg, bot_msg = item
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
        
    messages.append({"role": "user", "content": message})
    
    # Cevabı harf harf (streaming) döndür
    response_text = ""
    try:
        for chunk in chat_client.complete_streaming_chat(messages):
            if chunk.choices and len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content:
                    response_text += content
                    yield response_text
    except Exception as e:
        yield f"\n\n[Hata Oluştu: {str(e)}]"

# Uygulamayı başlat
if __name__ == "__main__":
    initialize_ai()
    
    # Gradio ile web arayüzü kurulumu
    demo = gr.ChatInterface(
        fn=chat_interface,
        title="Foundry Local RAG Asistanı",
        description="Bu asistan, 'docs' klasöründeki belgelerinizi okur ve internet bağlantısı olmadan sorularınızı cevaplar.",
        examples=["Foundry Local nedir?", "RAG ne işe yarar?", "Yapay zeka ile makine öğrenmesi arasındaki fark nedir?"]
    )
    
    print("Arayüz başlatılıyor! Tarayıcıda açmak için aşağıdaki linke tıklayın.")
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
