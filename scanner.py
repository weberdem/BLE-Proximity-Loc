import asyncio
from bleak import BleakScanner

async def main():
    print("Bluetooth LE cihazları taranıyor... Lütfen cihazınızı (saat/telefon) PC'ye yakın tutun.")
    print("-" * 50)
    
    # Cihazları ve beraberindeki reklam verilerini (RSSI dahil) tara
    devices_dict = await BleakScanner.discover(return_adv=True)
    
    if not devices_dict:
        print("Hiçbir cihaz bulunamadı. Bluetooth'un açık olduğundan emin olun.")
        return

    # Cihazları ve reklam verilerini bir listeye dönüştür
    scanned_list = []
    for addr, (device, adv_data) in devices_dict.items():
        scanned_list.append((device, adv_data))

    # Sinyal gücüne göre sırala (adv_data.rssi kullanarak)
    sorted_devices = sorted(scanned_list, key=lambda x: x[1].rssi, reverse=True)
    
    print(f"{'Ad':<25} | {'Adres':<20} | {'Sinyal (RSSI)':<10}")
    print("-" * 50)
    
    for device, adv_data in sorted_devices:
        name = device.name if device.name else "Bilinmiyor"
        print(f"{name:<25} | {device.address:<20} | {adv_data.rssi} dBm")
    
    print("-" * 50)
    print("\nLütfen cihazınızın 'Adres' bilgisini kopyalayın ve proximity_lock.py içindeki TARGET_ADDRESS kısmına yapıştırın.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Hata oluştu: {e}")
