"""
BLE Proximity Lock - Ana Uygulama
Yazan ve Kodlayan: Web Erdem
GitHub: https://github.com/weberdem
Instagram: https://instagram.com/web.erdem
TikTok: https://tiktok.com/@web.erdem
YouTube: https://youtube.com/weberdem
"""

import asyncio
import ctypes
import json
import os
import threading
import time
from bleak import BleakScanner
import pystray
from PIL import Image, ImageDraw
from plyer import notification

# --- AYARLAR ---
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"target_address": "", "near_threshold": -65, "far_threshold": -78, "lock_delay": 45}

cfg = load_config()
TARGET_ADDRESS = cfg["target_address"]
NEAR_THRESHOLD = cfg["near_threshold"]
FAR_THRESHOLD = cfg["far_threshold"]
LOCK_DELAY = cfg["lock_delay"]

class ProximityService:
    def __init__(self):
        self.current_state = "NEAR"
        self.last_seen = time.time()
        self.is_running = True
        self.rssi_history = []
        self.tray_icon = None

    def get_smoothed_rssi(self, rssi):
        self.rssi_history.append(rssi)
        if len(self.rssi_history) > 5: self.rssi_history.pop(0)
        return sum(self.rssi_history) / len(self.rssi_history)

    def lock_pc(self):
        print(f"[{time.strftime('%H:%M:%S')}] KİLİTLENİYOR")
        ctypes.windll.user32.LockWorkStation()
        notification.notify(title="BLE Kilidi", message="Cihaz uzaklaştı, PC kilitlendi.", timeout=3)

    def wake_screen(self):
        print(f"[{time.strftime('%H:%M:%S')}] UYANDIRILIYOR")
        # Ekranı uyandırmak için mouse hareketi ve klavye sinyali gönder
        ctypes.windll.user32.mouse_event(0x0001, 1, 1, 0, 0)
        ctypes.windll.user32.keybd_event(0x20, 0, 0, 0) # Space bas
        ctypes.windll.user32.keybd_event(0x20, 0, 2, 0) # Space bırak
        notification.notify(title="BLE Kilidi", message="Cihaz yaklaştı, ekran açıldı.", timeout=3)

    def detection_callback(self, device, advertisement_data):
        if device.address.strip().lower() == TARGET_ADDRESS.strip().lower():
            self.last_seen = time.time()
            avg_rssi = self.get_smoothed_rssi(advertisement_data.rssi)
            
            if avg_rssi > NEAR_THRESHOLD and self.current_state != "NEAR":
                self.current_state = "NEAR"
                self.wake_screen()
            elif avg_rssi < FAR_THRESHOLD and self.current_state != "FAR":
                self.current_state = "FAR"
                self.lock_pc()

    async def monitor(self):
        async with BleakScanner(detection_callback=self.detection_callback):
            while self.is_running:
                if time.time() - self.last_seen > LOCK_DELAY and self.current_state != "FAR":
                    self.current_state = "FAR"
                    self.lock_pc()
                await asyncio.sleep(1)

def create_image(color):
    img = Image.new('RGB', (64, 64), color=color)
    d = ImageDraw.Draw(img)
    d.ellipse([16, 16, 48, 48], fill=(255, 255, 255))
    return img

service = ProximityService()

def start_ble():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(service.monitor())

def setup_tray():
    icon = pystray.Icon("BLELock", create_image((0, 122, 204)), "BLE Takibi Aktif")
    icon.menu = pystray.Menu(pystray.MenuItem("Çıkış", lambda i, j: [setattr(service, 'is_running', False), i.stop()]))
    icon.run()

if __name__ == "__main__":
    print("-" * 40)
    print("BLE Yakınlık Kilidi - Başlatıldı")
    print("Yazan ve Kodlayan: Erdem (weberdem)")
    print("-" * 40)
    
    if not TARGET_ADDRESS:
        print("Lütfen önce setup.py çalıştırın.")
    else:
        threading.Thread(target=start_ble, daemon=True).start()
        setup_tray()
