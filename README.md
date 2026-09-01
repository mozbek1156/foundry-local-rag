# Local RAG Projesi (Foundry Local)

Bu proje, Microsoft Yaz/Staj programı kapsamında hazırladığım bir RAG (Retrieval-Augmented Generation) uygulamasıdır. Amacım internet bağlantısı olmadan, tamamen cihaz üzerinde çalışan ve kendi verdiğim dosyaları okuyup ona göre cevap veren bir yapay zeka asistanı yapmaktı.

Projede Microsoft'un Foundry Local altyapısını ve Python SDK'sını kullandım.

## Özellikler

- Offline çalışma: Uygulama internet olmadan da çalışıyor. Modeller (phi-3.5-mini ve qwen-embedding) bilgisayarın kendi donanımını kullanıyor.
- Doküman okuma: `docs` klasörünün içine attığım txt ve md dosyalarını otomatik okuyup parçalara ayırıyor (chunking).
- Arama ve cevap üretme: Sorduğum soruya en yakın olan metinleri kosinüs benzerliği ile bulup modele context olarak veriyor.
- Arayüz: Uygulamayı terminal yerine Gradio ile web arayüzünde çalışacak şekilde ayarladım.

## Nasıl Çalıştırılır?

1. Önce Python 3.8 veya üzeri bir sürümün yüklü olması lazım. 
2. Projedeki gerekli kütüphaneleri yüklemek için terminalde şunu çalıştırın:
   ```
   pip install foundry-local-sdk-winml gradio
   ```
3. Kendi notlarınızı veya test dosyalarınızı `docs` klasörünün içine atın. (Örnek bir txt dosyası bıraktım).
4. Sonra uygulamayı başlatın:
   ```
   python app.py
   ```

İlk açılışta eğer modeller bilgisayarınızda yoksa indirmeye başlıyor, bu biraz uzun sürebilir. İndikten sonra `http://127.0.0.1:7860/` linki üzerinden asistanı test edebilirsiniz.

## Projedeki Dosyalar

- `app.py`: Ana Python kodu. Embedding, chunking, model yükleme ve Gradio arayüzü burada.
- `main.py`: Projeye ilk başladığımda yazdığım konsol versiyonu, referans için duruyor.
- `docs/`: Okunacak dosyaların olduğu klasör.
- `notes.md`: Projeyi yaparken tuttuğum notlar.