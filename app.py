import streamlit as st
import pandas as pd
import datetime
import io
import os
import sqlite3
import base64

st.set_page_config(page_title="TTS Ships Panel", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.main-header{background:linear-gradient(90deg,#0b3d91,#1e6fd9);padding:20px;border-radius:10px;color:#fff;margin-bottom:20px}
.main-header h1{margin:0;font-size:26px}
.main-header p{margin:5px 0 0 0;opacity:.9;font-size:14px}
.ship-card{background:#fff;border:1px solid #e3e8ef;border-radius:12px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:15px}
.card-flex{display:flex;gap:14px;align-items:flex-start}
.eto-left{flex:0 0 130px;text-align:center}
.eto-avatar{width:120px;height:120px;border-radius:50%;background:#f1f5fb;color:#1e6fd9;display:flex;align-items:center;justify-content:center;font-size:60px;margin:0 auto;border:3px solid #1e6fd9}
.eto-name{font-size:11.5px;font-weight:700;color:#0b3d91;margin-top:8px}
.eto-role{font-size:10px;color:#7a8699;margin-top:2px}
.contract-box{margin-top:8px;font-size:10.5px}
.contract-dates{display:flex;justify-content:space-between;color:#5a6b82;font-size:10px;margin-bottom:4px}
.progress-track{background:#e6ecf5;border-radius:10px;height:8px;overflow:hidden}
.progress-fill{height:100%;border-radius:10px;background:linear-gradient(90deg,#22c55e,#16a34a)}
.progress-fill.warn{background:linear-gradient(90deg,#f59e0b,#d97706)}
.progress-fill.err{background:linear-gradient(90deg,#ef4444,#b91c1c)}
.contract-remaining{text-align:center;font-size:10.5px;margin-top:5px;font-weight:600;color:#16a34a}
.contract-remaining.warn{color:#d97706}
.contract-remaining.err{color:#b91c1c}
.ship-right{flex:1;min-width:0}
.ship-photo{width:100%;height:110px;object-fit:cover;border-radius:8px;margin-bottom:8px;display:block;background:#eef2f7}
.ship-photo-placeholder{width:100%;height:110px;border-radius:8px;margin-bottom:8px;background:linear-gradient(135deg,#eef2f7,#e3e8ef);display:flex;align-items:center;justify-content:center;font-size:40px;color:#b7c2d0}
.ship-name{font-weight:700;font-size:15px;color:#0b3d91;margin-bottom:3px}
.ship-imo{font-size:11px;color:#7a8699;margin-bottom:8px}
.ship-info{font-size:11.5px;color:#333;line-height:1.55}
.ship-info b{color:#0b3d91}
.ship-status{display:inline-block;padding:2px 9px;border-radius:10px;font-size:10px;font-weight:600;background:#e6f4ea;color:#1e7e34;margin-top:8px}
.ship-status.warn{background:#fff4e0;color:#b76e00}
.ship-status.err{background:#fdecea;color:#c0392b}
.panel-card{background:#fff;border:1px solid #e3e8ef;border-radius:12px;padding:16px 18px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:16px}
.panel-title{font-size:15px;font-weight:700;color:#0b3d91;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #e6ecf5}
.fault-item{display:flex;justify-content:space-between;align-items:flex-start;padding:8px 10px;border-radius:8px;margin-bottom:6px;background:#f8fafc;font-size:12.5px}
.fault-item.high{background:#fdecea;border-left:4px solid #dc2626}
.fault-item.mid{background:#fff7e6;border-left:4px solid #d97706}
.fault-item.low{background:#eaf7ee;border-left:4px solid #16a34a}
.fault-item.closed{background:#f1f5f9;border-left:4px solid #94a3b8;opacity:.65}
.fault-badge{font-size:10.5px;padding:2px 8px;border-radius:10px;background:#0b3d91;color:#fff;font-weight:600;white-space:nowrap}
.inspect-item{padding:10px 12px;border-radius:8px;margin-bottom:8px;background:#f8fafc;border-left:4px solid #1e6fd9;font-size:12.5px}
.inspect-date{font-size:10.5px;color:#7a8699;margin-bottom:3px}
.inspect-title{font-weight:700;color:#0b3d91;margin-bottom:4px}
.inspect-desc{color:#333;line-height:1.5}
.mat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;border-bottom:1px solid #eef2f7;font-size:12.5px}
.mat-name{font-weight:600;color:#333}
.mat-ship{font-size:10.5px;color:#7a8699}
.mat-qty{background:#e6ecf5;color:#0b3d91;padding:2px 8px;border-radius:10px;font-size:10.5px;font-weight:700}
.mat-priority{font-size:10px;padding:2px 8px;border-radius:10px;margin-left:6px;font-weight:600}
.mat-priority.acil{background:#fdecea;color:#c0392b}
.mat-priority.yuksek{background:#fff4e0;color:#b76e00}
.mat-priority.normal{background:#e6f4ea;color:#1e7e34}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Filo Yönetim Paneli</h1>
<p>MarineTraffic · Sertifika/Survey · Satınalma · Teknik Doküman · ETO Eğitim/PSC · Megger · Excel</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# VERİTABANI (SQLite) - Uygulama kapansa/yenilense bile veriler kalıcıdır
# ------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts_ships.db")

# Gemi fotoğrafları için klasör: app.py ile aynı dizinde "ship_images" klasörü oluşturup
# içine <IMO_NUMARASI>.jpg / .jpeg / .png / .webp formatında dosya eklemen yeterli.
# Örn: ship_images/9337028.jpg  -> M/V MED STAR (IMO 9337028)
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ship_images")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS ships(
        gemi TEXT PRIMARY KEY, imo TEXT, tip TEXT, dwt TEXT, grt TEXT,
        bayrak TEXT, yil TEXT, loa TEXT, eto TEXT, giris TEXT, kontrat_bitis TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS faults(
        id INTEGER PRIMARY KEY AUTOINCREMENT, gemi TEXT, ekipman TEXT,
        aciliyet TEXT, tespit TEXT, aciklama TEXT, status TEXT DEFAULT 'Açık'
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS inspections(
        id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT, gemi TEXT,
        baslik TEXT, aciklama TEXT, denetci TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS materials(
        id INTEGER PRIMARY KEY AUTOINCREMENT, malzeme TEXT, gemi TEXT,
        miktar INTEGER, oncelik TEXT, tedarikci TEXT, talep TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS purchases(
        id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT, gemi TEXT,
        malzeme TEXT, miktar INTEGER, oncelik TEXT, tedarikci TEXT,
        notlar TEXT, durum TEXT DEFAULT '🕓 Bekliyor'
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS megger(
        id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT, gemi TEXT,
        devre TEXT, test_v TEXT, ir_deger REAL, sonuc TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS certificates(
        id INTEGER PRIMARY KEY AUTOINCREMENT, gemi TEXT, sertifika TEXT,
        veren_kurum TEXT, duzenleme_tarihi TEXT, bitis TEXT, notlar TEXT
    )""")

    conn.commit()

    # Bakım temizliği: M/V BOSPHORUS filoda yer almıyor, önceki sürümde yanlışlıkla
    # eklenmişti. Zaten mevcut olmayan kayıtlar için DELETE no-op olduğundan
    # bu blok her başlatmada güvenle çalışır (var olan DB'leri de otomatik düzeltir).
    for tbl in ("ships", "faults", "inspections", "materials", "purchases", "megger", "certificates"):
        cur.execute("DELETE FROM " + tbl + " WHERE gemi='M/V BOSPHORUS'")
    conn.commit()

    # İlk çalıştırmada seed (örnek) veriyi yükle - sadece tablo boşsa
    cur.execute("SELECT COUNT(*) FROM ships")
    if cur.fetchone()[0] == 0:
        seed_ships = [
            ("M/V MED STAR", "9337028", "Container", "27254", "23633", "Panama", "2004", "191,10 m", "Ahmet YILMAZ", "2025-06-15", "2026-06-15"),
            ("M/T MOON STAR", "9667928", "Tanker", "49997", "29940", "Liberia", "2013", "183 m", "Mehmet DEMİR", "2025-11-02", "2026-08-02"),
            ("M/T KUZEY STAR II", "9499175", "Tanker", "6107", "4081", "Malta", "2020", "108,10 m", "Ali KAYA", "2026-01-20", "2027-01-20"),
            ("M/V A380", "9310915", "Ro-Ro Cargo", "1300", "1285", "Liberia", "2003", "75 m", "Hasan ÇELİK", "2025-09-05", "2026-03-05"),
            ("M/V AKBABA", "9319478", "Ro-Ro Cargo", "1300", "1281", "Liberia", "2004", "75 m", "Emre ŞAHİN", "2025-12-01", "2026-09-01"),
            ("M/V ALEXANDRA I", "8876340", "Bulk Carrier", "6005", "4949", "Panama", "1991", "138,40 m", "Serkan AYDIN", "2025-07-12", "2026-07-12"),
            ("M/V ALENA", "8857772", "Bulk Carrier", "6059", "4949", "Panama", "1991", "138,40 m", "Burak ÖZTÜRK", "2025-08-20", "2026-05-20"),
            ("M/V ATLANTIC STAR", "9473327", "Bulk Carrier", "75002,58", "41074", "Liberia", "2011", "225 m", "Kemal ARSLAN", "2026-02-10", "2027-02-10"),
            ("M/V PACIFIC STAR", "9470387", "Bulk Carrier", "78128", "41718", "Liberia", "2013", "224,90 m", "Onur YILDIZ", "2025-10-01", "2026-04-01"),
            ("M/V CHIEF SEATTLE", "9230751", "Bulk Carrier", "52428", "30174", "Panama", "2001", "189,89 m", "Volkan KOÇ", "2025-05-18", "2026-05-18"),
            ("M/V VENUS STAR", "9609134", "Bulk Carrier", "80888", "44025", "Liberia", "2013", "229 m", "Cem POLAT", "2026-03-01", "2027-03-01"),
            ("M/V MERCUR STAR", "9609287", "Bulk Carrier", "79520", "43501", "Malta", "2015", "229 m", "Barış TAŞ", "2025-12-15", "2026-06-15"),
            ("M/V DENIZ STAR", "1071472", "General Cargo", "8300", "6641", "Liberia", "2025", "142 m", "Tolga ERDOĞAN", "2026-01-05", "2026-10-05"),
            ("M/V BLACKSEA STAR", "1114901", "General Cargo", "8330", "6732", "Liberia", "2025", "142 m", "Yusuf KURT", "2026-02-20", "2026-11-20"),
            ("M/V SAPHIRA", "7924425", "Live Stock", "12900", "38988", "Antigua-Barbuda", "1995", "185,82 m", "Murat AVCİ", "2025-04-10", "2026-04-10"),
        ]
        cur.executemany("INSERT INTO ships VALUES (?,?,?,?,?,?,?,?,?,?,?)", seed_ships)

        seed_faults = [
            ("M/V MED STAR", "Bow Thruster Kumanda Panosu", "Orta", "2026-09-15", "Kumanda kartı arızalı.", "Açık"),
            ("M/T MOON STAR", "Acil Aydınlatma Devresi", "Yüksek", "2026-09-20", "Toprak kaçağı tespit edildi.", "Açık"),
            ("M/V A380", "Soğutma Kompresörü Motoru", "Düşük", "2026-09-10", "Rulman sesi artmış.", "Açık"),
            ("M/V ATLANTIC STAR", "MSB Bus-Bar Bağlantısı", "Yüksek", "2026-09-12", "Sıcak nokta tespit edildi (85 C).", "Açık"),
            ("M/V SAPHIRA", "Yangın Alarm Panosu", "Orta", "2026-09-08", "Zone 3 dedektörü arızalı.", "Açık"),
        ]
        cur.executemany("INSERT INTO faults(gemi,ekipman,aciliyet,tespit,aciklama,status) VALUES (?,?,?,?,?,?)", seed_faults)

        seed_inspections = [
            ("2026-09-20", "M/T MOON STAR", "Aylık Elektrik Denetimi", "MSB, acil jeneratör kontrol edildi. Acil aydınlatmada toprak kaçağı bulundu.", "Ahmet YILMAZ"),
            ("2026-09-15", "M/V MED STAR", "PSC Öncesi Öz Denetim", "Steering gear, emergency generator kontrol edildi. Bow thruster kartı arızalı.", "Ali KAYA"),
            ("2026-09-12", "M/V ATLANTIC STAR", "Termal Kamera Taraması", "Bus-bar bağlantısında sıcak nokta tespit edildi.", "Kemal ARSLAN"),
            ("2026-09-08", "M/V SAPHIRA", "Yangın Alarm Testi", "Zone 3 dedektörü cevap vermedi.", "Murat AVCİ"),
            ("2026-09-05", "M/V A380", "Rutin Elektrik Kontrolü", "Aydınlatma ve ana pano kontrol edildi.", "Hasan ÇELİK"),
        ]
        cur.executemany("INSERT INTO inspections(tarih,gemi,baslik,aciklama,denetci) VALUES (?,?,?,?,?)", seed_inspections)

        seed_materials = [
            ("Bow Thruster Kumanda Kartı", "M/V MED STAR", 1, "Acil", "Kongsberg", "2026-09-16"),
            ("Termal Kamera Kartuşu", "M/V ATLANTIC STAR", 1, "Yüksek", "FLIR", "2026-09-14"),
            ("Yangın Dedektörü (Zone 3)", "M/V SAPHIRA", 2, "Normal", "Consilium", "2026-09-10"),
            ("İzolasyon Bandı", "Tüm Filo", 20, "Normal", "3M", "2026-09-09"),
            ("Acil Aydınlatma Balastı", "M/T MOON STAR", 4, "Acil", "Philips", "2026-09-20"),
            ("Rulman (Kompresör)", "M/V A380", 2, "Yüksek", "SKF", "2026-09-11"),
            ("Sigorta Seti (MSB Yedek)", "M/V MED STAR", 1, "Normal", "ABB", "2026-09-07"),
            ("Kontaktör (3TF52)", "M/V CHIEF SEATTLE", 3, "Yüksek", "Siemens", "2026-09-13"),
        ]
        cur.executemany("INSERT INTO materials(malzeme,gemi,miktar,oncelik,tedarikci,talep) VALUES (?,?,?,?,?,?)", seed_materials)

        conn.commit()

    # Sertifika tablosu için ayrı seed kontrolü (mevcut kurulumlarda ships/faults/materials
    # dolu olsa bile certificates tablosu boş olabileceğinden ayrı kontrol ediyoruz)
    cur.execute("SELECT COUNT(*) FROM certificates")
    if cur.fetchone()[0] == 0:
        t = datetime.date.today()
        seed_certs = [
            ("M/V MED STAR", "Safety Equipment", "Class NK", str(t - datetime.timedelta(days=350)), str(t + datetime.timedelta(days=15)), ""),
            ("M/V MED STAR", "Load Line", "Class NK", str(t - datetime.timedelta(days=185)), str(t + datetime.timedelta(days=180)), ""),
            ("M/T MOON STAR", "IOPP", "DNV", str(t - datetime.timedelta(days=355)), str(t + datetime.timedelta(days=5)), ""),
            ("M/T MOON STAR", "Safety Construction", "DNV", str(t - datetime.timedelta(days=125)), str(t + datetime.timedelta(days=240)), ""),
            ("M/T KUZEY STAR II", "ISSC", "Türk Loydu", str(t - datetime.timedelta(days=270)), str(t + datetime.timedelta(days=90)), ""),
            ("M/V ATLANTIC STAR", "IAPP", "ABS", str(t - datetime.timedelta(days=368)), str(t - datetime.timedelta(days=3)), "Yenileme bekleniyor"),
            ("M/V PACIFIC STAR", "Class Certificate", "ABS", str(t - datetime.timedelta(days=320)), str(t + datetime.timedelta(days=45)), ""),
            ("M/V SAPHIRA", "IOPP", "Bureau Veritas", str(t - datetime.timedelta(days=45)), str(t + datetime.timedelta(days=320)), ""),
        ]
        cur.executemany(
            "INSERT INTO certificates(gemi,sertifika,veren_kurum,duzenleme_tarihi,bitis,notlar) VALUES (?,?,?,?,?,?)",
            seed_certs,
        )
        conn.commit()

    conn.close()


init_db()


# ------------------------------------------------------------------
# VERİ ERİŞİM YARDIMCI FONKSİYONLARI
# ------------------------------------------------------------------
def df_from(query, params=()):
    conn = get_conn()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def run(query, params=()):
    conn = get_conn()
    conn.execute(query, params)
    conn.commit()
    conn.close()


def gemi_durumu_hesapla(gemi_adi):
    """Açık arızalara bakarak geminin Durum rozetini dinamik hesaplar."""
    faults_df = df_from(
        "SELECT aciliyet FROM faults WHERE gemi=? AND status='Açık'", (gemi_adi,)
    )
    if faults_df.empty:
        return "🟢 Uygun"
    if (faults_df["aciliyet"] == "Yüksek").any():
        return "🔴 Arıza"
    if (faults_df["aciliyet"] == "Orta").any():
        return "🟡 Bakım"
    return "🟢 Uygun"


def fleet_df_yukle():
    df = df_from("SELECT * FROM ships")
    df = df.rename(columns={
        "gemi": "Gemi", "imo": "IMO", "tip": "Tip", "dwt": "DWT", "grt": "GRT",
        "bayrak": "Bayrak", "yil": "Yıl", "loa": "LOA", "eto": "ETO",
        "giris": "Giris", "kontrat_bitis": "KontratBitis",
    })
    df["Durum"] = df["Gemi"].apply(gemi_durumu_hesapla)
    return df


def arizalar_yukle(sadece_acik=True):
    if sadece_acik:
        df = df_from("SELECT * FROM faults WHERE status='Açık' ORDER BY tespit DESC")
    else:
        df = df_from("SELECT * FROM faults ORDER BY tespit DESC")
    return df.rename(columns={
        "gemi": "Gemi", "ekipman": "Ekipman", "aciliyet": "Aciliyet",
        "tespit": "Tespit", "aciklama": "Aciklama", "status": "Durum",
    })


def denetlemeler_yukle():
    df = df_from("SELECT * FROM inspections ORDER BY tarih DESC")
    return df.rename(columns={
        "tarih": "Tarih", "gemi": "Gemi", "baslik": "Baslik",
        "aciklama": "Aciklama", "denetci": "Denetci",
    })


def malzeme_yukle():
    df = df_from("SELECT * FROM materials ORDER BY talep DESC")
    return df.rename(columns={
        "malzeme": "Malzeme", "gemi": "Gemi", "miktar": "Miktar",
        "oncelik": "Oncelik", "tedarikci": "Tedarikci", "talep": "Talep",
    })


@st.cache_data(show_spinner=False)
def gemi_resmi_base64(imo):
    """ship_images/ klasöründe IMO numarasıyla eşleşen bir resim varsa base64 data-uri olarak döner, yoksa None."""
    if not imo:
        return None
    ext_mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    for ext, mime in ext_mime.items():
        path = os.path.join(IMAGES_DIR, str(imo) + ext)
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return "data:" + mime + ";base64," + data
    return None


def kontrat_bilgi(giris_str, bitis_str):
    try:
        giris = datetime.date.fromisoformat(giris_str)
        bitis = datetime.date.fromisoformat(bitis_str)
    except Exception:
        return 0, 0, ""
    bugun = datetime.date.today()
    toplam = (bitis - giris).days
    kalan = (bitis - bugun).days
    if toplam <= 0:
        return 0, 0, ""
    gecen = (bugun - giris).days
    yuzde = max(0, min(100, int((gecen / toplam) * 100)))
    if kalan < 0 or kalan <= 30 or yuzde >= 85:
        cls = "err"
    elif kalan <= 90 or yuzde >= 65:
        cls = "warn"
    else:
        cls = ""
    return kalan, yuzde, cls


def sertifika_durum_hesapla(bitis_str):
    """Bitiş tarihine göre kalan gün ve durum rozetini dinamik hesaplar."""
    try:
        bitis = datetime.date.fromisoformat(bitis_str)
    except Exception:
        return 0, "🟢 Geçerli"
    kalan = (bitis - datetime.date.today()).days
    if kalan < 0:
        return kalan, "🔴 Süresi Geçti"
    if kalan <= 30:
        return kalan, "🔴 Kritik"
    if kalan <= 90:
        return kalan, "🟡 Yakında"
    return kalan, "🟢 Geçerli"


def sertifika_yukle():
    df = df_from("SELECT * FROM certificates ORDER BY bitis ASC")
    df = df.rename(columns={
        "gemi": "Gemi", "sertifika": "Sertifika", "veren_kurum": "VerenKurum",
        "duzenleme_tarihi": "DuzenlemeTarihi", "bitis": "Bitis", "notlar": "Notlar",
    })
    if df.empty:
        df["KalanGun"] = []
        df["Durum"] = []
        return df
    sonuc = df["Bitis"].apply(sertifika_durum_hesapla)
    df["KalanGun"] = sonuc.apply(lambda x: x[0])
    df["Durum"] = sonuc.apply(lambda x: x[1])
    return df


def ship_card_html(row):
    cls = ""
    if "Arıza" in row["Durum"]:
        cls = "err"
    elif "Bakım" in row["Durum"]:
        cls = "warn"
    emoji_map = {"Container": "📦", "Tanker": "🛢️", "Bulk Carrier": "⛏️", "Ro-Ro Cargo": "🚗", "General Cargo": "📦", "Live Stock": "🐄"}
    tip_emoji = emoji_map.get(row["Tip"], "🚢")
    kalan, yuzde, kcls = kontrat_bilgi(row["Giris"], row["KontratBitis"])
    if kalan < 0:
        kalan_text = "⚠️ Kontrat " + str(abs(kalan)) + " gün önce bitti"
    elif kalan == 0:
        kalan_text = "⏰ Kontrat bugün bitiyor"
    else:
        kalan_text = "⏳ " + str(kalan) + " gün kaldı (%" + str(yuzde) + ")"
    h = '<div class="ship-card"><div class="card-flex">'
    h += '<div class="eto-left">'
    h += '<div class="eto-avatar">👤</div>'
    h += '<div class="eto-name">👨‍✈️ ' + row["ETO"] + '</div>'
    h += '<div class="eto-role">Baş Elektrik Zabiti (ETO)</div>'
    h += '<div class="contract-box">'
    h += '<div class="contract-dates"><span>📅 ' + row["Giris"] + '</span><span>' + row["KontratBitis"] + '</span></div>'
    h += '<div class="progress-track"><div class="progress-fill ' + kcls + '" style="width:' + str(yuzde) + '%;"></div></div>'
    h += '<div class="contract-remaining ' + kcls + '">' + kalan_text + '</div>'
    h += '</div></div>'
    h += '<div class="ship-right">'
    resim = gemi_resmi_base64(row["IMO"])
    if resim:
        h += '<img class="ship-photo" src="' + resim + '" alt="' + row["Gemi"] + '"/>'
    else:
        h += '<div class="ship-photo-placeholder">' + tip_emoji + '</div>'
    h += '<div class="ship-name">' + tip_emoji + ' ' + row["Gemi"] + '</div>'
    h += '<div class="ship-imo">IMO: ' + row["IMO"] + ' · ' + row["Tip"] + '</div>'
    h += '<div class="ship-info">'
    h += '<b>Bayrak:</b> ' + row["Bayrak"] + '<br/>'
    h += '<b>DWT:</b> ' + row["DWT"] + ' | <b>GRT:</b> ' + row["GRT"] + '<br/>'
    h += '<b>Yıl:</b> ' + row["Yıl"] + ' | <b>LOA:</b> ' + row["LOA"]
    h += '</div>'
    h += '<div class="ship-status ' + cls + '">' + row["Durum"] + '</div>'
    h += '</div></div></div>'
    return h


def render_ariza(fleet_df):
    st.markdown('<div class="panel-card"><div class="panel-title">🔧 Gemilerde Bulunan Toplam Arızalar (Açık)</div>', unsafe_allow_html=True)
    ariza_df = arizalar_yukle(sadece_acik=True)
    y = int((ariza_df["Aciliyet"] == "Yüksek").sum()) if not ariza_df.empty else 0
    o = int((ariza_df["Aciliyet"] == "Orta").sum()) if not ariza_df.empty else 0
    d = int((ariza_df["Aciliyet"] == "Düşük").sum()) if not ariza_df.empty else 0
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam (Açık)", len(ariza_df))
    m2.metric("🔴 Yüksek", y)
    m3.metric("🟡 Orta", o)
    m4.metric("🟢 Düşük", d)
    st.markdown("---")
    if ariza_df.empty:
        st.info("Açık arıza kaydı yok.")
    for _, a in ariza_df.iterrows():
        cls = "low"
        if a["Aciliyet"] == "Yüksek":
            cls = "high"
        elif a["Aciliyet"] == "Orta":
            cls = "mid"
        line = '<div class="fault-item ' + cls + '">'
        line += '<div><b>' + a["Gemi"] + '</b> · ' + a["Ekipman"]
        line += '<div style="font-size:11px;color:#5a6b82;margin-top:3px;">' + a["Aciklama"] + '</div>'
        line += '<div style="font-size:10px;color:#7a8699;margin-top:3px;">Tespit: ' + a["Tespit"] + '</div></div>'
        line += '<span class="fault-badge">' + a["Aciliyet"] + '</span></div>'
        st.markdown(line, unsafe_allow_html=True)

    with st.expander("✅ Arıza Kapat (giderildi olarak işaretle)"):
        if not ariza_df.empty:
            secim_etiketleri = [
                str(r["id"]) + " — " + r["Gemi"] + " · " + r["Ekipman"] for _, r in ariza_df.iterrows()
            ]
            secim = st.selectbox("Kapatılacak arıza", secim_etiketleri, key="ariza_kapat_sec")
            if st.button("Kapat", key="ariza_kapat_btn"):
                fault_id = int(secim.split(" — ")[0])
                run("UPDATE faults SET status='Kapalı' WHERE id=?", (fault_id,))
                st.success("✅ Arıza kapatıldı, gemi durumu güncellendi.")
                st.rerun()
        else:
            st.caption("Kapatılacak açık arıza yok.")

    with st.expander("➕ Yeni Arıza Ekle"):
        with st.form("yeni_ariza_form"):
            c1, c2 = st.columns(2)
            with c1:
                gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="yeni_ariza_gemi")
                ekipman = st.text_input("Ekipman")
            with c2:
                aciliyet = st.selectbox("Aciliyet", ["Yüksek", "Orta", "Düşük"], key="yeni_ariza_aciliyet")
                tespit = st.date_input("Tespit Tarihi", datetime.date.today(), key="yeni_ariza_tarih")
            aciklama = st.text_area("Açıklama")
            if st.form_submit_button("Kaydet") and ekipman:
                run(
                    "INSERT INTO faults(gemi,ekipman,aciliyet,tespit,aciklama,status) VALUES (?,?,?,?,?, 'Açık')",
                    (gemi, ekipman, aciliyet, str(tespit), aciklama),
                )
                st.success("✅ Arıza eklendi.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def render_denetleme():
    st.markdown('<div class="panel-card"><div class="panel-title">📋 En Son Yapılan Denetlemeler ve Tespitler</div>', unsafe_allow_html=True)
    denet_df = denetlemeler_yukle()
    for _, d in denet_df.iterrows():
        line = '<div class="inspect-item">'
        line += '<div class="inspect-date">📅 ' + d["Tarih"] + ' · Denetçi: ' + d["Denetci"] + '</div>'
        line += '<div class="inspect-title">🚢 ' + d["Gemi"] + ' — ' + d["Baslik"] + '</div>'
        line += '<div class="inspect-desc">' + d["Aciklama"] + '</div></div>'
        st.markdown(line, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_malzeme():
    st.markdown('<div class="panel-card"><div class="panel-title">📦 Malzeme İhtiyaç Listesi</div>', unsafe_allow_html=True)
    mat_df = malzeme_yukle()
    a = int((mat_df["Oncelik"] == "Acil").sum()) if not mat_df.empty else 0
    y = int((mat_df["Oncelik"] == "Yüksek").sum()) if not mat_df.empty else 0
    n = int((mat_df["Oncelik"] == "Normal").sum()) if not mat_df.empty else 0
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam", len(mat_df))
    m2.metric("🔴 Acil", a)
    m3.metric("🟡 Yüksek", y)
    m4.metric("🟢 Normal", n)
    st.markdown("---")
    for _, m in mat_df.iterrows():
        cls = "normal"
        if m["Oncelik"] == "Acil":
            cls = "acil"
        elif m["Oncelik"] == "Yüksek":
            cls = "yuksek"
        line = '<div class="mat-row">'
        line += '<div><div class="mat-name">' + m["Malzeme"] + '</div>'
        line += '<div class="mat-ship">' + m["Gemi"] + ' · ' + m["Tedarikci"] + ' · Talep: ' + m["Talep"] + '</div></div>'
        line += '<div><span class="mat-qty">' + str(m["Miktar"]) + ' adet</span>'
        line += '<span class="mat-priority ' + cls + '">' + m["Oncelik"] + '</span></div></div>'
        st.markdown(line, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


menu = st.sidebar.radio(
    "📌 Navigasyon",
    ["🏠 Dashboard", "🚢 Filo Yönetimi", "📜 Sertifika & Survey", "🛒 Satınalma",
     "📚 Teknik Dokümanlar", "🎓 ETO Eğitim & PSC", "⚡ Megger Kayıtları", "📄 Raporlama"],
)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 TTS Ships · v3.9 (kalıcı veri + dinamik durum + sertifika DB + gemi fotoğrafları)")

fleet_df = fleet_df_yukle()

if menu == "🏠 Dashboard":
    st.subheader("📊 Filo Genel Durum")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Gemi", len(fleet_df))
    c2.metric("🟢 Uygun", (fleet_df["Durum"] == "🟢 Uygun").sum())
    c3.metric("🟡 Bakım", (fleet_df["Durum"] == "🟡 Bakım").sum())
    c4.metric("🔴 Arıza", (fleet_df["Durum"] == "🔴 Arıza").sum())
    st.markdown("---")

    with st.expander("🔍 Filtrele"):
        f1, f2 = st.columns(2)
        with f1:
            durum_filtre = st.multiselect(
                "Durum", ["🟢 Uygun", "🟡 Bakım", "🔴 Arıza"], default=[]
            )
        with f2:
            tip_filtre = st.multiselect(
                "Gemi Tipi", sorted(fleet_df["Tip"].unique().tolist()), default=[]
            )
    gosterilecek = fleet_df.copy()
    if durum_filtre:
        gosterilecek = gosterilecek[gosterilecek["Durum"].isin(durum_filtre)]
    if tip_filtre:
        gosterilecek = gosterilecek[gosterilecek["Tip"].isin(tip_filtre)]

    rows = gosterilecek.to_dict("records")
    for i in range(0, len(rows), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(rows):
                with col:
                    st.markdown(ship_card_html(rows[i + j]), unsafe_allow_html=True)
    st.markdown("---")
    ca, cb = st.columns([1, 1])
    with ca:
        render_ariza(fleet_df)
    with cb:
        render_malzeme()
    st.markdown("---")
    render_denetleme()

elif menu == "🚢 Filo Yönetimi":
    st.subheader("🚢 Filo Yönetimi (Tablo Görünümü)")
    st.dataframe(fleet_df, use_container_width=True)

elif menu == "📜 Sertifika & Survey":
    st.subheader("📜 Sertifika & Survey Takibi")
    cert_df = sertifika_yukle()
    kritik_sayisi = int((cert_df["Durum"].isin(["🔴 Kritik", "🔴 Süresi Geçti"])).sum()) if not cert_df.empty else 0
    yakinda_sayisi = int((cert_df["Durum"] == "🟡 Yakında").sum()) if not cert_df.empty else 0
    gecerli_sayisi = int((cert_df["Durum"] == "🟢 Geçerli").sum()) if not cert_df.empty else 0
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Toplam", len(cert_df))
    k2.metric("🔴 Kritik/Süresi Geçti", kritik_sayisi)
    k3.metric("🟡 Yakında", yakinda_sayisi)
    k4.metric("🟢 Geçerli", gecerli_sayisi)
    st.markdown("---")

    if not cert_df.empty:
        gosterim_df = cert_df[["Gemi", "Sertifika", "VerenKurum", "DuzenlemeTarihi", "Bitis", "KalanGun", "Durum", "Notlar"]]
        st.dataframe(gosterim_df, use_container_width=True)
    else:
        st.info("Kayıtlı sertifika yok.")

    with st.expander("♻️ Sertifika Yenile (bitiş tarihini güncelle)"):
        if not cert_df.empty:
            secim_etiketleri = [
                str(r["id"]) + " — " + r["Gemi"] + " · " + r["Sertifika"] + " (" + r["Bitis"] + ")"
                for _, r in cert_df.iterrows()
            ]
            secim = st.selectbox("Yenilenecek sertifika", secim_etiketleri, key="sert_yenile_sec")
            yeni_bitis = st.date_input(
                "Yeni Bitiş Tarihi", datetime.date.today() + datetime.timedelta(days=365), key="sert_yenile_tarih"
            )
            yenile_notlar = st.text_input("Not (opsiyonel)", key="sert_yenile_not")
            if st.button("Yenile", key="sert_yenile_btn"):
                cert_id = int(secim.split(" — ")[0])
                run(
                    "UPDATE certificates SET bitis=?, duzenleme_tarihi=?, notlar=? WHERE id=?",
                    (str(yeni_bitis), str(datetime.date.today()), yenile_notlar, cert_id),
                )
                st.success("✅ Sertifika yenilendi.")
                st.rerun()
        else:
            st.caption("Yenilenecek sertifika kaydı yok.")

    with st.expander("➕ Yeni Sertifika Ekle"):
        with st.form("yeni_sertifika_form"):
            c1, c2 = st.columns(2)
            with c1:
                gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="yeni_sert_gemi")
                sertifika = st.text_input("Sertifika Adı")
                veren_kurum = st.text_input("Veren Kurum (Class/Bayrak)")
            with c2:
                duzenleme_tarihi = st.date_input("Düzenleme Tarihi", datetime.date.today(), key="yeni_sert_duzenleme")
                bitis = st.date_input(
                    "Bitiş Tarihi", datetime.date.today() + datetime.timedelta(days=365), key="yeni_sert_bitis"
                )
            notlar = st.text_area("Notlar")
            if st.form_submit_button("Kaydet") and sertifika:
                run(
                    "INSERT INTO certificates(gemi,sertifika,veren_kurum,duzenleme_tarihi,bitis,notlar) VALUES (?,?,?,?,?,?)",
                    (gemi, sertifika, veren_kurum, str(duzenleme_tarihi), str(bitis), notlar),
                )
                st.success("✅ Sertifika eklendi.")
                st.rerun()

elif menu == "🛒 Satınalma":
    st.subheader("🛒 Satınalma Talepleri")
    with st.form("talep_form"):
        col1, col2 = st.columns(2)
        with col1:
            gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist())
            malzeme = st.text_input("Malzeme / Ekipman")
            miktar = st.number_input("Miktar", min_value=1, value=1)
        with col2:
            oncelik = st.selectbox("Öncelik", ["Normal", "Yüksek", "Acil"])
            tedarikci = st.text_input("Tedarikçi (opsiyonel)")
            notlar = st.text_area("Notlar")
        if st.form_submit_button("📨 Talep Oluştur") and malzeme:
            run(
                "INSERT INTO purchases(tarih,gemi,malzeme,miktar,oncelik,tedarikci,notlar,durum) VALUES (?,?,?,?,?,?,?,?)",
                (str(datetime.date.today()), gemi, malzeme, miktar, oncelik, tedarikci, notlar, "🕓 Bekliyor"),
            )
            st.success("✅ Talep oluşturuldu ve kalıcı olarak kaydedildi.")
            st.rerun()

    talep_df = df_from("SELECT * FROM purchases ORDER BY id DESC")
    if not talep_df.empty:
        st.markdown("### 📋 Talep Listesi")
        durum_secenekleri = ["🕓 Bekliyor", "🚚 Sipariş Edildi", "✅ Teslim Alındı", "❌ İptal"]
        for _, r in talep_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([3, 2, 2])
                c1.write("**" + r["malzeme"] + "** — " + r["gemi"] + " (" + str(r["miktar"]) + " adet, " + r["oncelik"] + ")")
                c2.caption("Talep: " + r["tarih"] + (" · " + r["tedarikci"] if r["tedarikci"] else ""))
                yeni_durum = c3.selectbox(
                    "Durum", durum_secenekleri,
                    index=durum_secenekleri.index(r["durum"]) if r["durum"] in durum_secenekleri else 0,
                    key="talep_durum_" + str(r["id"]),
                    label_visibility="collapsed",
                )
                if yeni_durum != r["durum"]:
                    run("UPDATE purchases SET durum=? WHERE id=?", (yeni_durum, r["id"]))
                    st.rerun()
        st.dataframe(talep_df, use_container_width=True)
    else:
        st.info("Henüz talep oluşturulmadı.")

elif menu == "📚 Teknik Dokümanlar":
    st.subheader("📚 Teknik Doküman Kütüphanesi")
    docs = pd.DataFrame([
        {"Kategori": "Manuel", "Doküman": "Ana Şalter Panosu Manual", "Gemi": "M/V MED STAR", "Rev": "R3"},
        {"Kategori": "Şema", "Doküman": "Tek Hat Şeması (SLD)", "Gemi": "M/V MED STAR", "Rev": "R5"},
        {"Kategori": "Manuel", "Doküman": "Jeneratör Kontrol Panosu Manual", "Gemi": "M/T MOON STAR", "Rev": "R2"},
        {"Kategori": "Şema", "Doküman": "Aydınlatma Şeması", "Gemi": "M/V ATLANTIC STAR", "Rev": "R1"},
        {"Kategori": "Test", "Doküman": "Megger Test Prosedürü", "Gemi": "Tüm Filo", "Rev": "R4"},
        {"Kategori": "Class", "Doküman": "Class Rules - Electrical", "Gemi": "Tüm Filo", "Rev": "2025"},
    ])
    st.dataframe(docs, use_container_width=True)

elif menu == "🎓 ETO Eğitim & PSC":
    st.subheader("🎓 ETO Eğitim & PSC Simülasyonu")
    quiz = [
        {"Soru": "AC devrede Insulation Resistance minimum kac MOhm olmalidir?",
         "Secenekler": ["0.1 MOhm", "0.5 MOhm", "1 MOhm", "5 MOhm"], "Cevap": "1 MOhm"},
        {"Soru": "Megaohmmetre testinde kullanilan gerilim hangisidir?",
         "Secenekler": ["12 V DC", "110 V AC", "500 V DC", "380 V AC"], "Cevap": "500 V DC"},
        {"Soru": "PSC'de 30 saniye kurali hangi konuyla ilgilidir?",
         "Secenekler": ["Emergency Generator", "Steering Gear", "Fire Pump", "Bilge Pump"], "Cevap": "Steering Gear"},
        {"Soru": "Emergency Switchboard hangi besleme kaynagini kullanir?",
         "Secenekler": ["Main Switchboard", "Emergency Generator", "Shore Power", "Bus Tie"], "Cevap": "Emergency Generator"},
        {"Soru": "Motor overload koruma cihazi hangisidir?",
         "Secenekler": ["MCB", "RCD", "Thermal Overload Relay", "Fuse"], "Cevap": "Thermal Overload Relay"},
    ]
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
        st.session_state.score = 0
    if st.session_state.quiz_idx < len(quiz):
        q = quiz[st.session_state.quiz_idx]
        st.markdown("**Soru " + str(st.session_state.quiz_idx + 1) + "/" + str(len(quiz)) + ":** " + q["Soru"])
        secim = st.radio("Cevap:", q["Secenekler"], key="q" + str(st.session_state.quiz_idx))
        if st.button("✅ Onayla"):
            if secim == q["Cevap"]:
                st.session_state.score += 1
                st.success("Doğru!")
            else:
                st.error("Yanlış. Doğru cevap: " + q["Cevap"])
            st.session_state.quiz_idx += 1
            st.rerun()
    else:
        st.balloons()
        st.success("🎉 Sinav tamamlandi! Skor: " + str(st.session_state.score) + "/" + str(len(quiz)))
        if st.button("🔄 Yeniden Başla"):
            st.session_state.quiz_idx = 0
            st.session_state.score = 0
            st.rerun()

elif menu == "⚡ Megger Kayıtları":
    st.subheader("⚡ Megger / Insulation Resistance Kayitlari")
    with st.form("megger_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="mg")
            devre = st.text_input("Devre / Ekipman")
        with col2:
            test_v = st.selectbox("Test Gerilimi", ["500 V DC", "1000 V DC", "2500 V DC"])
            ir_deger = st.number_input("IR Degeri (MOhm)", min_value=0.0, value=100.0, step=0.1)
        with col3:
            test_tarih = st.date_input("Test Tarihi", datetime.date.today())
            sonuc = st.selectbox("Sonuc", ["✅ Uygun", "⚠️ İzle", "❌ Uygun Değil"])
        if st.form_submit_button("💾 Kaydet") and devre:
            run(
                "INSERT INTO megger(tarih,gemi,devre,test_v,ir_deger,sonuc) VALUES (?,?,?,?,?,?)",
                (str(test_tarih), gemi, devre, test_v, ir_deger, sonuc),
            )
            st.success("✅ Kayit eklendi ve kalıcı olarak saklandı.")
            st.rerun()

    megger_df = df_from("SELECT * FROM megger ORDER BY id DESC")
    if not megger_df.empty:
        st.dataframe(megger_df, use_container_width=True)
    else:
        st.info("Henuz megger kaydi yok.")

elif menu == "📄 Raporlama":
    st.subheader("📄 Excel Raporlama")
    rapor_tipi = st.selectbox("Rapor Tipi", ["Filo Listesi", "Satınalma", "Megger Kayıtları", "Arızalar (Açık)", "Sertifika & Survey"])
    if rapor_tipi == "Filo Listesi":
        df_rapor = fleet_df
    elif rapor_tipi == "Satınalma":
        df_rapor = df_from("SELECT * FROM purchases ORDER BY id DESC")
        if df_rapor.empty:
            df_rapor = pd.DataFrame([{"Not": "Kayit yok"}])
    elif rapor_tipi == "Megger Kayıtları":
        df_rapor = df_from("SELECT * FROM megger ORDER BY id DESC")
        if df_rapor.empty:
            df_rapor = pd.DataFrame([{"Not": "Kayit yok"}])
    elif rapor_tipi == "Sertifika & Survey":
        df_rapor = sertifika_yukle()
        if df_rapor.empty:
            df_rapor = pd.DataFrame([{"Not": "Kayit yok"}])
    else:
        df_rapor = arizalar_yukle(sadece_acik=True)
        if df_rapor.empty:
            df_rapor = pd.DataFrame([{"Not": "Kayit yok"}])
    st.dataframe(df_rapor, use_container_width=True)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_rapor.to_excel(writer, index=False, sheet_name="Rapor")
    st.download_button(
        "⬇️ Excel İndir",
        data=buffer.getvalue(),
        file_name="tts_ships_rapor.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
