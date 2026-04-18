# 🛡️ BLE Proximity Lock (Akıllı Mesafe Kilidi)

Bu proje, bir Bluetooth Low Energy (BLE) cihazının (saat, telefon vb.) sinyal gücünü (RSSI) takip ederek, bilgisayardan uzaklaştığınızda otomatik olarak kilitlenmesini, yaklaştığınızda ise ekranın uyanmasını sağlar.

## ✨ Özellikler
- 🔒 **Güvenli Kilitleme**: Sinyal belirli bir eşiğin altına düştüğünde Windows kilitlenir.
- 🔅 **Akıllı Uyandırma**: Yaklaştığınızda ekranı otomatik olarak uyandırır.
- 🕵️ **Arka Planda Çalışma**: Sistem tepsisinde (System Tray) sessizce çalışır.
- 🛠️ **Kolay Kurulum**: Dahili setup sihirbazı ile cihazınızı saniyeler içinde seçebilirsiniz.

## 🚀 Başlangıç

### Gereksinimler
- Windows 10/11
- Python 3.10+
- Bluetooth LE destekli bir cihaz

### Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/weberdem/BLE-Proximity-Lock.git
   cd BLE-Proximity-Lock
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Kurulum sihirbazını çalıştırın ve cihazınızı seçin:
   ```bash
   python setup.py
   ```

4. Uygulamayı başlatın:
   ```bash
   python proximity_lock.py
   ```

## 👨‍💻 Yazan ve Kodlayan
**Web Erdem**
- [Instagram](https://instagram.com/web.erdem)
- [TikTok](https://tiktok.com/@web.erdem)
- [YouTube](https://youtube.com/weberdem)
- [GitHub](https://github.com/weberdem)

## 📄 Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
