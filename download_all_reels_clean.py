import sys, os, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
VIDEOS_DIR = r"c:\Users\danie\Downloads\SF\ig_assets\videos"
os.makedirs(VIDEOS_DIR, exist_ok=True)

REELS = [
    ("reel_10_curex_san_juan", "https://www.instagram.com/sfentretenimiento1/reel/Dcf_1vKRn6H/"),
    ("reel_12_15_georgett", "https://www.instagram.com/sfentretenimiento1/reel/DbEI9UwRb3J/"),
    ("reel_1_sound_karaoke", "https://www.instagram.com/sfentretenimiento1/reel/DO6N2dxkR3h/"),
    ("reel_7_halloween_humo", "https://www.instagram.com/sfentretenimiento1/reel/DPPIJDEkRbx/"),
    ("reel_11_curex_familia", "https://www.instagram.com/curex.ca/reel/DchMpzcJHQz/"),
    ("reel_4_puerto_cabello", "https://www.instagram.com/sfentretenimiento1/reel/DPY4k57Eddg/")
]

def clean_cdn_url(url):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs.pop('bytestart', None)
    qs.pop('byteend', None)
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(qs, doseq=True)))

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=BRAVE if os.path.exists(BRAVE) else None, headless=True)
    for tag, url in REELS:
        dest_file = os.path.join(VIDEOS_DIR, f"{tag}.mp4")
        if os.path.exists(dest_file) and os.path.getsize(dest_file) > 100000:
            print(f"Already have {tag}")
            continue
            
        print(f"Fetching reel: {tag} ({url})")
        page = browser.new_page(user_agent=UA, viewport={"width": 1280, "height": 900})
        v_urls = set()
        
        def on_resp(resp):
            try:
                ct = resp.headers.get("content-type", "")
                r_url = resp.url
                if ("video" in ct or ".mp4" in r_url) and ("cdninstagram" in r_url or "fbcdn" in r_url):
                    v_urls.add(clean_cdn_url(r_url))
            except:
                pass
                
        page.on("response", on_resp)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
            page.evaluate("""() => {
                const dialogs = document.querySelectorAll('div[role="dialog"], div[role="presentation"]');
                for (let d of dialogs) d.remove();
                for (let v of document.querySelectorAll('video')) { v.muted = true; v.play().catch(e=>{}); }
            }""")
            time.sleep(3)
            
            # Try downloading
            downloaded = False
            for c_url in v_urls:
                try:
                    req = urllib.request.Request(c_url, headers={'User-Agent': UA, 'Referer': 'https://www.instagram.com/'})
                    with urllib.request.urlopen(req, timeout=15) as r, open(dest_file, 'wb') as f:
                        f.write(r.read())
                    sz = os.path.getsize(dest_file)
                    if sz > 100000:
                        print(f"  [+] Saved {tag}.mp4 ({sz} bytes)")
                        downloaded = True
                        break
                    else:
                        os.remove(dest_file)
                except Exception as e:
                    pass
            if not downloaded:
                print(f"  [-] Could not download video for {tag}")
        except Exception as e:
            print(f"  Error on {tag}: {e}")
        finally:
            page.close()
            
    browser.close()
    print("Done video extraction!")
