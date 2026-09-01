# Proje Notlarım

Bu belgede "Local RAG Application" projesini yaparken haftalık olarak aldığım notlar yer alıyor. 

## Hafta 1 - Kurulum ve İlk Denemeler
Foundry Local'i bilgisayarıma kurdum. Amacı modelleri internete bağlanmadan localde çalıştırmakmış. 
İlk deneme olarak komut satırından `phi-3.5-mini` modelini indirip biraz sohbet ettim. 
Sonrasında SDK'yı kurup Python koduyla bağlanmayı başardım.

## Hafta 2 - Embedding ve Vektör Arama
Bu hafta uygulamanın RAG tarafına giriş yaptım. Metinleri vektörlere çevirmek için `qwen3-embedding-0.6b` modelini kurdum. İki farklı metnin birbirine ne kadar benzediğini hesaplamak için kosinüs benzerliği formülü kullandım. Test ettiğimde sorduğum sorulara en uygun metni başarılı bir şekilde eşleştirebildi.

## Hafta 3 - Dokümanları Okuma (Chunking)
Bu hafta sistemi sadece koddaki sabit metinlerle değil, dışarıdan dosya okuyarak çalışacak hale getirdim. 
Öncelikle `docs` diye bir klasör açıp, içindeki txt veya md dosyalarını okuyan bir kod yazdım.
Uzun dosyaları model tek seferde anlayamadığı için (token sınırı), yazıları paragraflara göre "chunk"lara bölmem gerekti. Şimdilik ortalama 500 karakterlik parçalar halinde ayırıyorum, iş görüyor.

## Hafta 4 - Arayüz ve Sonuç
Sürekli terminalden kod çalıştırmak kullanışsız olduğu için projeye bir web arayüzü eklemeye karar verdim. Gradio kütüphanesi bu iş için çok pratik oldu, hızlıca bir chat ekranı çıkarttım. 
En önemli kısım "Sistem Promptu" oldu. Modelle konuşurken arkaplanda sürekli "sadece verdiğim bağlama göre cevap ver, uydurma" şeklinde bir kural gönderiyorum, bu sayede halüsinasyon yapmıyor.
Projeyi test etmek için internetimi kapattım ve offline olarak belgelerim üzerinden soru cevap yapabildim. Proje bitti.
