# BLE Smart Watch → PC Automation System

## 🎯 Amaç

Bu proje, BLE (Bluetooth Low Energy) üzerinden bir akıllı saat ile Windows PC arasında bağlantı kurarak aşağıdaki otomasyonları gerçekleştirmek için tasarlanmıştır:

### 📌 Fonksiyonlar
- Saat PC’ye yaklaştığında:
  - PC otomatik olarak "aktif / uyku modundan çıkar"
  - İsteğe bağlı: ekran açılır
- Saat bağlantısı koptuğunda:
  - PC ekranı kilitlenir veya kapanır
- Saatin RSSI (sinyal gücü) takip edilerek yakınlık algılanır
- Heartbeat (isteğe bağlı): cihazdan periyodik sinyal alınır

---

## 🧠 Sistem Mimarisi

### 1. BLE Central (PC - Python App)
- Bluetooth LE cihazlarını tarar
- Belirli MAC adresi veya cihaz adı ile filtreler
- Bağlantı durumu ve RSSI izler
- Disconnect event algılar
- Windows API ile sistem kontrolü yapar

### 2. BLE Peripheral (Smart Watch)
- Sürekli advertising yayınlar
- Bağlanabilir (connectable mode)
- İsteğe bağlı heartbeat characteristic gönderir

---

## 🔧 Teknoloji Stack

### Python Libraries
- bleak (BLE client)
- asyncio
- pywin32 (Windows system control)
- ctypes (low-level Windows API)
- logging

### Optional
- tkinter / fastapi (UI veya dashboard)
- pystray (system tray app)

---

## 📡 BLE Behavior

### Target Device Discovery
- Device name filter OR MAC address
- Example:
  - Name: "Sifli Watch"
  - UUID: custom service UUID

### Connection Flow
1. Scan devices (5-10 sec interval loop)
2. Find target device
3. Connect via BLE GATT
4. Subscribe to:
   - notify characteristics (if available)
5. Monitor:
   - RSSI
   - connection state

---

## 📊 Proximity Logic

```python
if rssi > -60:
    state = "NEAR"
elif -80 < rssi <= -60:
    state = "MEDIUM"
else:
    state = "FAR"