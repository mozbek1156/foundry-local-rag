import math
from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. Bilgi tabanı
documents = [
    "Foundry Local runs AI models directly on your device without cloud connectivity.",
    "The Foundry Local SDK supports Python, C#, JavaScript, and Rust.",
    "Embedding models convert text into numerical vectors for similarity search.",
    "Foundry Local uses ONNX Runtime for efficient model inference on CPUs and GPUs.",
    "The model catalog provides pre-optimized models that you can download and run locally.",
    "Retrieval-augmented generation grounds model responses in your own data.",
    "Vector similarity search finds documents that are semantically close to a query.",
    "Chat completions generate natural language responses from a prompt and context.",
]

# Kosinüs benzerlik fonksiyonu
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

# En alakalı dokümanları bulma fonksiyonu
def find_relevant(query_embedding, doc_embeddings, top_k=2):
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((i, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

def main():
    # SDK'yı başlat
    config = Configuration(app_name="foundry_local_rag")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # --- EMBEDDING MODELİ ---
    embedding_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    embedding_model.download(
        lambda p: print(f"\rEmbedding modeli indiriliyor: {p:.1f}%", end="", flush=True)
    )
    print()
    embedding_model.load()
    embedding_client = embedding_model.get_embedding_client()

    # Dokümanları vektöre çevir
    response = embedding_client.generate_embeddings(documents)
    doc_embeddings = [item.embedding for item in response.data]
    print(f"{len(doc_embeddings)} doküman indekslendi.\n")

    # --- SOHBET MODELİ (YENİ - Hafta 3) ---
    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download(
        lambda p: print(f"\rSohbet modeli indiriliyor: {p:.1f}%", end="", flush=True)
    )
    print()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    print("\nModeller yüklendi. Sorularınızı bekliyorum.")
    print('Örnek: "What programming languages does the SDK support?"')
    print('Çıkmak için "quit" yazın.\n')

    TOP_K = 2  # Kaç doküman getirilecek — deneyerek değiştirebilirsiniz (1, 2, 3...)

    # --- İNTERAKTİF SORU-CEVAP DÖNGÜSÜ (YENİ - Hafta 3) ---
    while True:
        query = input("Soru: ").strip()
        if not query or query.lower() == "quit":
            break

        # Sorguyu vektöre çevir
        query_response = embedding_client.generate_embedding(query)
        query_embedding = query_response.data[0].embedding

        # En alakalı dokümanları getir (retrieval)
        results = find_relevant(query_embedding, doc_embeddings, top_k=TOP_K)
        context = "\n".join(f"- {documents[i]}" for i, _ in results)

        # Hangi dokümanların bulunduğunu göster (isteğe bağlı, şeffaflık için)
        print("  [Bulunan bağlam:]")
        for i, score in results:
            print(f"    ({score:.3f}) {documents[i]}")

        # Bağlamla birlikte prompt oluştur
        messages = [
            {
                "role": "system",
                "content": (
                    "Yalnızca verilen bağlamı kullanarak kullanıcının sorusunu cevapla. "
                    "Bağlamda yeterli bilgi yoksa, bunu açıkça belirt.\n\n"
                    f"Bağlam:\n{context}"
                ),
            },
            {"role": "user", "content": query},
        ]

        # Cevabı akış halinde yazdır (generation)
        for chunk in chat_client.complete_streaming_chat(messages):
            if chunk.choices and len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
    # Temizlik
    embedding_model.unload()
    chat_model.unload()
    print("Modeller kapatıldı. Hafta 3 testi tamam!")

if __name__ == "__main__":
    main()