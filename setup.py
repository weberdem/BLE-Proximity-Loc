"""
BLE Proximity Lock - Kurulum Sihirbazı
Yazan ve Kodlayan: Web Erdem
GitHub: https://github.com/weberdem
Instagram: https://instagram.com/web.erdem
TikTok: https://tiktok.com/@web.erdem
YouTube: https://youtube.com/weberdem
"""

import json
import os
import sys
import asyncio
import winreg
from bleak import BleakScanner

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
APP_NAME = "BLEProximityLock"
STARTUP_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "proximity_lock.py"))
PYTHONW = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")

def save_config(data: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def step1_scan_devices():
    print("\n" + "="*55)
    print("  ADIM 1: Cihaz Seçimi")
    print("="*55)
    print("Bluetooth LE cihazları taranıyor...")
    
    async def scan():
        devices_dict = await BleakScanner.discover(return_adv=True)
        return devices_dict

    devices_dict = asyncio.run(scan())
    if not devices_dict:
        print("HATA: Cihaz bulunamadı.")
        return None

    scanned = []
    for addr, (device, adv_data) in devices_dict.items():
        scanned.append((device, adv_data))
    scanned.sort(key=lambda x: x[1].rssi, reverse=True)

    print(f"{'#':<4} {'Ad':<30} {'Adres':<20} {'Sinyal'}")
    print("-" * 65)
    for i, (dev, adv) in enumerate(scanned):
        name = dev.name if dev.name else "Bilinmiyor"
        print(f"[{i+1}]  {name:<30} {dev.address:<20} {adv.rssi} dBm")

    while True:
        try:
            choice = int(input("\nTakip edilecek cihaz numarası: ")) - 1
            if 0 <= choice < len(scanned):
                return scanned[choice][0].address
        except: pass

def step2_startup():
    print("\n" + "="*55)
    print("  ADIM 2: Windows Başlangıcında Çalışma")
    print("="*55)
    enable = input("Windows açılınca otomatik başlasın mı? (e/h): ").strip().lower()
    
    if enable == 'e':
        startup_cmd = f'"{PYTHONW}" "{SCRIPT_PATH}"'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, startup_cmd)
        return True
    return False

def main():
    print("\n" + "="*55)
    print("   BLE Yakınlık Kilidi - Kurulum")
    print("   Yazan ve Kodlayan: Erdem (weberdem)")
    print("="*55)
    print("   GitHub   : https://github.com/weberdem")
    print("   Instagram: https://instagram.com/web.erdem")
    print("   YouTube  : https://youtube.com/weberdem")
    print("="*55)
    config = load_config()
    
    address = step1_scan_devices()
    if not address: return
    
    config["target_address"] = address
    config["startup"] = step2_startup()
    
    # Eşik değerleri (Varsayılan başarılı değerler)
    config["near_threshold"] = -65
    config["far_threshold"] = -78
    config["lock_delay"] = 45
    
    save_config(config)
    print("\n✓ Kurulum Tamamlandı! Şimdi proximity_lock.py çalıştırabilirsiniz.")

if __name__ == "__main__":
    main()
