import sys, os, time, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BRAVE = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
VIDEOS_DIR = r"c:\Users\danie\Downloads\SF\ig_assets\videos"
HQ_IMAGES_DIR = r"c:\Users\danie\Downloads\SF\ig_assets\hq_images"
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(HQ_IMAGES_DIR, exist_ok=True)

# List of reel URLs from the scrape
REELS = [
    ("reel_1_sound_karaoke", "https://www.instagram.com/sfentretenimiento1/reel/DO6N2dxkR3h/"),
    ("reel_2_decked_out", "https://www.instagram.com/sfentretenimiento1/reel/DQg_4sAkQlI/"),
    ("reel_3_smile", "https://www.instagram.com/sfentretenimiento1/reel/DPHRQmLkY-9/"),
    ("reel_4_puerto_cabello", "https://www.instagram.com/sfentretenimiento1/reel/DPY4k57Eddg/"),
    ("post_5_centro_italo", "https://www.instagram.com/centroitalosanjuan/p/DcyOhZHERu1/"),
    ("reel_6_lighting", "https://www.instagram.com/sfentretenimiento1/reel/DVE-7tckRVs/"),
    ("reel_7_halloween_humo", "https://www.instagram.com/sfentretenimiento1/reel/DPPIJDEkRbx/"),
    ("reel_8_personal", "https://www.instagram.com/sfentretenimiento1/reel/DS-MJinkfkv/"),
    ("reel_9_celebra", "https://www.instagram.com/sfentretenimiento1/reel/DPCx44dkQZm/"),
    ("reel_10_curex_san_juan", "https://www.instagram.com/sfentretenimiento1/reel/Dcf_1vKRn6H/"),
    ("reel_11_curex_familia", "https://www.instagram.com/curex.ca/reel/DchMpzcJHQz/"),
    ("reel_12_15_georgett", "https://www.instagram.com/sfentretenimiento1/reel/DbEI9UwRb3J/"),
]

def download_stream(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://www.instagram.com/'})
        with urllib.request.urlopen(req, timeout=20) as resp, open(dest_path, 'wb') as f:
            f.write(resp.read())
        print(f"  [+] Downloaded: {os.path.basename(dest_path)} ({os.path.getsize(dest_path)} bytes)")
        return True
    except Exception as e:
        print(f"  [-] Failed downloading {dest_path}: {e}")
        return False

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=BRAVE if os.path.exists(BRAVE) else None, headless=True)
    
    for tag, url in REELS:
        print(f"\nProcessing {tag}: {url}")
        video_urls = set()
        img_urls = set()
        
        page = browser.new_page(user_agent=UA, viewport={"width": 1280, "height": 900})
        
        def handle_response(response):
            try:
                ct = response.headers.get("content-type", "")
                r_url = response.url
                if "video" in ct or ".mp4" in r_url:
                    video_urls.add(r_url)
                elif "image" in ct and ("cdninstagram" in r_url or "fbcdn" in r_url):
                    img_urls.add(r_url)
            except:
                pass
                
        page.on("response", handle_response)
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)
            
            # Dismiss overlays
            page.evaluate("""
                () => {
                    const dialogs = document.querySelectorAll('div[role="dialog"], div[role="presentation"]');
                    for (let d of dialogs) d.remove();
                    document.body.style.overflow = 'auto';
                }
            """)
            
            # Click play on any video if paused
            page.evaluate("""
                () => {
                    const vids = document.querySelectorAll('video');
                    for (let v of vids) {
                        v.muted = true;
                        v.play().catch(e => {});
                    }
                }
            """)
            time.sleep(3)
            
            # Also check DOM video src and images
            dom_media = page.evaluate("""
                () => {
                    const vids = Array.from(document.querySelectorAll('video')).map(v => v.src).filter(Boolean);
                    const imgs = Array.from(document.querySelectorAll('article img, main img')).map(i => i.src).filter(Boolean);
                    return { vids, imgs };
                }
            """)
            
            for v in dom_media['vids']:
                if v.startswith("http"): video_urls.add(v)
            for img in dom_media['imgs']:
                if img.startswith("http"): img_urls.add(img)
                
            print(f"  Found {len(video_urls)} video streams, {len(img_urls)} image streams")
            
            # Download the primary video if available
            v_idx = 0
            for v_url in video_urls:
                if "bytestart" in v_url or "byteend" in v_url:
                    continue # Partial chunk
                v_dest = os.path.join(VIDEOS_DIR, f"{tag}_{v_idx}.mp4")
                if download_stream(v_url, v_dest):
                    v_idx += 1
                    if v_idx >= 1: break # Got full video
                    
            # Download top HQ images
            im_idx = 0
            for im_url in img_urls:
                if "150x150" in im_url or "s150x150" in im_url or "profile_pic" in im_url:
                    continue
                im_dest = os.path.join(HQ_IMAGES_DIR, f"{tag}_{im_idx}.jpg")
                if download_stream(im_url, im_dest):
                    im_idx += 1
                    if im_idx >= 2: break
                    
        except Exception as e:
            print(f"  Error loading {url}: {e}")
        finally:
            page.close()
            
    browser.close()
    print("\n[✔] Finished downloading all media!")
