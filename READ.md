# Foundry Local RAG Projesi

Microsoft Foundry Local kullanarak, tamamen kendi bilgisayarımda ve internete
ihtiyaç duymadan çalışan bir RAG (Retrieval-Augmented Generation) uygulaması
geliştiriyorum. Bu proje, kendi verdiğim dokümanları okuyup, sorduğum sorulara
o dokümanlara dayanarak cevap veren yerel bir yapay zeka asistanı olacak.

Bu proje, Microsoft'un yaz proje grubu kapsamında 4 haftalık bir grup fazı
olarak geliştiriliyor; sonrasında bireysel olarak devam edecek.

## Kurulum

1. Foundry Local'i kurun: `winget install Microsoft.FoundryLocal` (Windows)
2. Sanal ortam oluşturun: `python -m venv venv` ve aktive edin
3. Paketleri kurun: `pip install foundry-local-sdk-winml openai`

## Çalıştırma

```bash
python hello_model.py
```

## İlerleme

- [x] Hafta 1: Foundry Local kurulumu, ilk model testi
- [ ] Hafta 2: Embedding ve anlamsal arama
- [ ] Hafta 3: Uçtan uca RAG hattı
- [ ] Hafta 4: Cilalama ve sunum hazırlığı