import os
import time
import random
import requests
from bs4 import BeautifulSoup

# Konfigurasi
VISITS_TARGET = 30                    # Jumlah kunjungan yang diinginkan
MIN_VISIT_TIME = 40                   # Waktu minimal kunjungan (detik)
MAX_VISIT_TIME = 65                   # Waktu maksimal kunjungan (detik)
DELAY_BETWEEN_VISITS = 15             # Jeda antar kunjungan (detik)
ADSTERRA_URL = "https://www.profitableratecpm.com/icb56k0m?key=34b261d534e4a259e9e2af3861057e03"
RENDER_API_URL = "https://render-tron.appspot.com/render"


def get_fresh_proxies():
    """Mengambil proxy dari berbagai sumber terpercaya"""
    all_proxies = []
    
    # Sumber proxy yang terverifikasi
    sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    ]
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            proxies = [p.strip() for p in response.text.splitlines() if p.strip() and ':' in p]
            
            # Menghindari duplikat
            new_proxies = [p for p in proxies if p not in all_proxies]
            all_proxies.extend(new_proxies)
            
            print(f"✓ {len(new_proxies)} proxy berhasil diambil dari {url.split('/')[-1]}")
            
        except Exception as e:
            print(f"⚠️ Gagal mengambil proxy dari {url}: {str(e)[:50]}...")
    
    # Proxy cadangan jika tidak ada yang berhasil diambil
    if not all_proxies:
        all_proxies = [
            "45.8.211.195:80", "104.18.70.24:80", "104.19.43.6:80",
            "185.176.26.94:80", "185.193.29.160:80", "104.16.63.102:80"
        ]
        print("⚠️ Menggunakan proxy cadangan")
    
    print(f"✅ Total: {len(all_proxies)} proxy berhasil dimuat")
    return all_proxies


def simulate_human_interaction():
    """Simulasi interaksi manusia (waktu kunjungan)"""
    visit_duration = random.randint(MIN_VISIT_TIME, MAX_VISIT_TIME)
    print(f"⏱ Simulasi kunjungan selama {visit_duration} detik")
    time.sleep(visit_duration)
    return True


def visit_adsterra_via_api(proxy):
    """Kunjungi Adsterra menggunakan API render"""
    try:
        print(f"🌐 Memulai kunjungan via API dengan proxy: {proxy}")
        
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        # Kunjungi Google dulu (untuk terlihat lebih natural)
        search_query = random.choice(["berita", "cuaca", "olahraga", "teknologi", "musik"])
        google_url = f"https://www.google.com/search?q={search_query}+{random.randint(1000,9999)}"
        
        params = {
            "url": google_url,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(RENDER_API_URL, params=params, timeout=30, proxies=proxies)
        response.raise_for_status()
        print("✓ Akses Google berhasil disimulasikan")
        time.sleep(random.uniform(2, 4))
        
        # Kunjungi Adsterra
        params = {
            "url": ADSTERRA_URL,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "waitFor": 5000
        }
        response = requests.get(RENDER_API_URL, params=params, timeout=60, proxies=proxies)
        response.raise_for_status()
        print("✓ Halaman Adsterra berhasil dimuat via API")
        
        success = simulate_human_interaction()
        
        if success:
            print("✅ Kunjungan via API BERHASIL!")
            return True
    
    except Exception as e:
        print(f"❌ Error saat kunjungan via API: {str(e)}")
    
    return False


def visit_adsterra_direct(proxy):
    """Kunjungi Adsterra secara langsung menggunakan requests"""
    try:
        print(f"🌐 Memulai kunjungan langsung dengan proxy: {proxy}")
        
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        
        # Kunjungi Google dulu
        search_query = random.choice(["berita", "cuaca", "olahraga", "teknologi", "musik"])
        google_url = f"https://www.google.com/search?q={search_query}+{random.randint(1000,9999)}"
        
        response = requests.get(google_url, headers=headers, timeout=15, proxies=proxies)
        response.raise_for_status()
        print("✓ Akses Google berhasil")
        time.sleep(random.uniform(2, 4))
        
        # Kunjungi Adsterra
        response = requests.get(ADSTERRA_URL, headers=headers, timeout=30, proxies=proxies)
        response.raise_for_status()
        print("✓ Halaman Adsterra berhasil dimuat")
        
        success = simulate_human_interaction()
        
        if success:
            print("✅ Kunjungan langsung BERHASIL!")
            return True
    
    except Exception as e:
        print(f"❌ Error saat kunjungan langsung: {str(e)}")
    
    return False


def visit_adsterra():
    """Melakukan satu kunjungan lengkap"""
    proxies = get_fresh_proxies()
    proxy = random.choice(proxies) if proxies else None
    
    # Coba via API dulu
    if proxy and visit_adsterra_via_api(proxy):
        return True
    
    # Jika gagal, coba langsung
    if proxy and visit_adsterra_direct(proxy):
        return True
    
    # Terakhir coba tanpa proxy
    print("⚠️ Mencoba tanpa proxy...")
    if visit_adsterra_direct(None):
        return True
    
    return False


def main():
    print("""
    █████╗ ██████╗ ███████╗████████╗███████╗██████╗ ██████╗  █████╗ 
   ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
   ███████║██║  ██║███████╗   ██║   █████╗  ██████╔╝██████╔╝███████║
   ██╔══██║██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║
   ██║  ██║██████╔╝███████║   ██║   ███████╗██║  ██║██║  ██║██║  ██║
   ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
          Bot Traffic Adsterra - Versi Bahasa Indonesia
    """)
    
    visits_count = 0
    
    while visits_count < VISITS_TARGET:
        success = visit_adsterra()
        
        if success:
            visits_count += 1
            print(f"✅ Kunjungan berhasil: {visits_count}/{VISITS_TARGET}")
        
        # Jeda sebelum kunjungan berikutnya
        delay = DELAY_BETWEEN_VISITS + random.randint(-5, 10)
        print(f"😴 Jeda {delay} detik sebelum kunjungan berikutnya...")
        time.sleep(max(10, delay))
    
    print("🎉 Proses generate traffic selesai!")


if __name__ == "__main__":
    # Install dependencies otomatis
    os.system('pip install requests beautifulsoup4 > /dev/null 2>&1')
    main()
