import keyboard
import time
import threading


running = False
macro_thread = None
makro_hizi = 2.0  



def yaz_kelime_satirlari():
    global running
    try:
        with open("kelimeler.txt", "r", encoding="utf-8") as f:
            satirlar = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("kelimeler.txt dosyası bulunamadı!")
        running = False
        return

    if not satirlar:
        print("kelimeler.txt dosyası boş!")
        running = False
        return

    index = 0
    while running:
        satir = satirlar[index % len(satirlar)] 
        try:
            print(f"Yazılıyor ({(index % len(satirlar)) + 1}): .{satir}")
            

            keyboard.press_and_release('/')  
            time.sleep(0.1)  #
            
            keyboard.write(f".{satir}")  
            time.sleep(0.05) 
            
            keyboard.press_and_release('enter') 
            time.sleep(2)  
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            running = False
            break
        time.sleep(makro_hizi)
        index += 1

def nokta_enter_makro():
    """Makro: önce . sonra Enter basar"""
    global running
    while running:
        try:
            print("Nokta ve Enter yazılıyor...")
            keyboard.write('.')
            keyboard.press_and_release('enter')
        except Exception as e:
            print(f"Hata oluştu: {e}")
            running = False
            break
        time.sleep(makro_hizi)

def baslat():
    global running, macro_thread
    if not running:
        running = True
        macro_thread = threading.Thread(target=yaz_kelime_satirlari)
        macro_thread.daemon = True
        macro_thread.start()
        print("Makro başladı.")
    else:
        print("Makro zaten çalışıyor.")

def baslat_nokta_enter():
    """Nokta ve Enter makrosunu başlat"""
    global running, macro_thread
    if not running:
        running = True
        macro_thread = threading.Thread(target=nokta_enter_makro)
        macro_thread.daemon = True
        macro_thread.start()
        print("Nokta-Enter makrosu başladı.")
    else:
        print("Makro zaten çalışıyor.")

def durdur():
    global running
    if running:
        running = False
        print("Makro durduruluyor.")

def hiz_artir():
    global makro_hizi
    if makro_hizi > 0.1:
        makro_hizi -= 0.1
        print(f"Hız artırıldı: {makro_hizi:.1f}s")

def hiz_azalt():
    global makro_hizi
    if makro_hizi < 5.0:
        makro_hizi += 0.1
        print(f"Hız azaltıldı: {makro_hizi:.1f}s")


active_handlers = []

def load_keymap(filename):
    key_map = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value:
                        key_map[key] = value
    except FileNotFoundError:
        print(f"{filename} bulunamadı!")
    return key_map

def clear_handlers():
    global active_handlers
    for handler in active_handlers:
        keyboard.unhook(handler)
    active_handlers = []

    print("┏┓             ┏┓      ")
    print("┃┃┓┏┏┓┏┓┓  ┓┏  ┃┃┓┏┏┓┏┓")
    print("┗┻┗┻┗┻┛ ┗  ┛┗  ┗┻┗┻┗┻┛ ")
    print("                           ")

    print("Tüm remap'ler temizlendi. Klavye normale döndü.")

def remap_keys_from_file(filename):
    clear_handlers()
    key_map = load_keymap(filename)
    for key in key_map:
        handler = keyboard.on_press_key(key, lambda e, k=key: keyboard.write(key_map[k]), suppress=True)
        active_handlers.append(handler)
    print(f"{filename} yüklendi.")

def setup_keymap_switching():
    keyboard.add_hotkey("1", lambda: remap_keys_from_file("keys.txt"))
    keyboard.add_hotkey("2", lambda: remap_keys_from_file("keys2.txt"))
    keyboard.add_hotkey("3", lambda: remap_keys_from_file("keys3.txt"))
    keyboard.add_hotkey("4", lambda: remap_keys_from_file("keys4.txt"))
    keyboard.add_hotkey("5", lambda: remap_keys_from_file("keys5.txt"))
    keyboard.add_hotkey("6", lambda: remap_keys_from_file("keys6.txt"))
    keyboard.add_hotkey("7", lambda: remap_keys_from_file("keys7.txt"))
    keyboard.add_hotkey("8", lambda: remap_keys_from_file("keys8.txt"))
    keyboard.add_hotkey("9", lambda: remap_keys_from_file("keys9.txt"))
    keyboard.add_hotkey("esc", clear_handlers)

    print("1 → keys.txt, 2 → keys2.txt, 3 → keys3.txt")
    print("4 → keys4.txt, 5 → keys5.txt, 6 → keys6.txt")
    print("ESC → Tüm eşlemeleri iptal et")


if __name__ == "__main__":
    print("=== Tuş Atama & Makro Programı ===")
    print("F8 → Makro Başlat (nokta + kelime + enter)")
    print("F9 → Makro Durdur")
    print("F10 → Hız Artır, F11 → Hız Azalt")
    print("1-8 → Farklı tuş eşlemeleri yükle")
    print("ESC → Tüm eşlemeleri iptal et")
    print("Çıkmak için Ctrl+C")

    remap_keys_from_file("keys.txt") 
    setup_keymap_switching()

  
    keyboard.add_hotkey('F8', baslat)
    keyboard.add_hotkey('F9', durdur)
    keyboard.add_hotkey('F10', hiz_artir)
    keyboard.add_hotkey('F11', hiz_azalt)

    keyboard.wait()  
