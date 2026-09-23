import streamlit as st
import pandas as pd
import datetime
import io
import os
import sqlite3

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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
.crit-badge{font-size:10px;padding:2px 8px;border-radius:10px;font-weight:700;margin-left:6px}
.crit-badge.unsafe{background:#fdecea;color:#c0392b}
.crit-badge.nearmiss{background:#fff4e0;color:#b76e00}
.crit-badge.normal{background:#e6f4ea;color:#1e7e34}
.recurring-badge{background:#fde8e8;color:#b91c1c;font-size:10px;padding:2px 8px;border-radius:10px;font-weight:700;margin-left:6px;white-space:nowrap}
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
# SABİT LİSTELER (Arıza formu için)
# ------------------------------------------------------------------
KOK_NEDEN_LIST = [
    "Seçilmedi",
    "İnsan Hatası / Operasyonel Hata",
    "Periyodik Bakım Eksikliği / Gecikmesi",
    "Malzeme / Yedek Parça Kalitesi (Ömrünü Tamamlama)",
    "Çevresel Faktörler (Aşırı nem, tuzlu su, ağır deniz şartları)",
    "Kestirilemeyen / Beklenmeyen Parça Ömrü",
    "Diğer",
]

KRITIKLIK_LIST = [
    "Normal",
    "⚠️ Unsafe Condition (Emniyetsiz Durum)",
    "🔶 Near-Miss (Kıl Payı Kurtulma)",
]

DEPARTMAN_LIST = [
    "Elektro-Teknik Zabit (ETO)",
    "Başmühendis",
    "Çarkçıbaşı",
    "Güverte Zabiti",
    "Dış Servis / Yüklenici",
    "Diğer",
]

PARA_BIRIMI_LIST = ["TRY", "USD", "EUR"]

# ------------------------------------------------------------------
# VERİTABANI (SQLite) - Uygulama kapansa/yenilense bile veriler kalıcıdır
# ------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts_ships.db")


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

    # Not: Yeni kurulumlarda arıza kök-neden/maliyet/kritiklik alanları dahildir.
    # Mevcut (eski) bir tts_ships.db dosyası varsa, migrate_db() bu sütunları sonradan ekler.
    cur.execute("""CREATE TABLE IF NOT EXISTS faults(
        id INTEGER PRIMARY KEY AUTOINCREMENT, gemi TEXT, ekipman TEXT,
        aciliyet TEXT, tespit TEXT, aciklama TEXT, status TEXT DEFAULT 'Açık',
        kok_neden TEXT DEFAULT '', kritiklik TEXT DEFAULT 'Normal',
        tekrarlayan TEXT DEFAULT 'Hayır', parca_maliyeti REAL DEFAULT 0,
        iscilik_maliyeti REAL DEFAULT 0, para_birimi TEXT DEFAULT 'TRY',
        downtime_saat REAL DEFAULT 0, mudahale_eden TEXT DEFAULT '',
        mudahale_departman TEXT DEFAULT '', kapanis_tarihi TEXT DEFAULT ''
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

    conn.commit()

    # İlk çalıştırmada seed (örnek) veriyi yükle - sadece tablo boşsa
    cur.execute("SELECT COUNT(*) FROM ships")
    if cur.fetchone()[0] == 0:
    seed_ships = [
    ("M/V MED STAR", "9337028", "Container", "27254", "23633", "Panama", "2004", "191,10 m", "Ahmet YILMAZ", "2025-06-15", "2026-06-15"),
    ("M/T MOON STAR", "8667823", "Tanker", "68687", "28640", "Liberia", "2011", "183 m", "Mehmet DEMİR", "2025-11-01", "2026-11-01"),
    ("M/T KUZEY STAR II", "9496175", "Tanker", "8107", "4031", "Malta", "2020", "106,10 m", "Ali KAYA", "2026-01-20", "2027-01-20"),
    ("M/V ARRO", "9310915", "Ro-Ro Cargo", "1500", "1266", "Liberia", "2003", "75 m", "Hasan ÇELİK", "2025-09-05", "2026-09-05"),
    ("M/V AKBABA", "9151473", "Ro-Ro Cargo", "1500", "281", "Liberia", "2004", "75 m", "Emre ŞAHİN", "2025-12-01", "2026-09-01"),
    ("M/V ALEXANDRIA I", "8903540", "Bulk Carrier", "8000", "4049", "Panama", "1991", "135,40 m", "Serkan AYDIN", "2025-07-12", "2026-07-12"),
    ("M/V ALENA", "8667772", "Bulk Carrier", "6068", "4958", "Panama", "1981", "100,45 m", "Burak ÖZTÜRK", "2025-08-20", "2026-08-20"),
    ("M/V ATLANTIC STAR", "9473327", "Bulk Carrier", "75000.58", "41074", "Liberia", "2011", "225 m", "Kemal ARSLAN", "2026-02-10", "2027-02-10"),
    ("M/V PACIFIC STAR", "9470867", "Bulk Carrier", "39128", "41718", "Liberia", "2013", "224,50 m", "Onur YILDIZ", "2025-10-01", "2026-04-01"),
    ("M/V CHIEF SEATTLE", "8270761", "Bulk Carrier", "50429", "30074", "Panama", "2005", "106.83 m", "Volkan KOÇ", "2025-05-18", "2026-05-18"),
    ("M/V VENUS STAR", "9609134", "Bulk Carrier", "80688", "44025", "Liberia", "2011", "229 m", "Cem POLAT", "2025-03-01", "2027-03-01"),
    ("M/V MERCUR STAR", "9800287", "Bulk Carrier", "75920", "43501", "Malta", "2016", "229 m", "Barış TAŞ", "2025-11-15", "2026-06-15"),
    ("M/V DENIZ STAR", "1077472", "General Cargo", "8300", "8844", "Liberia", "2008", "142 m", "Tolga ERDOĞAN", "2026-01-01", "2026-10-03"),
    ("M/V BLACK SEA STAR", "9740171", "General Cargo", "8330", "6752", "Liberia", "2008", "142 m", "Yusuf KURT", "2026-02-20", "2026-11-20"),
    ("M/V SAPHIRA", "7824405", "Live Stock", "12600", "36668", "Antigua-Barbuda", "1995", "105.02 m", "Murat AVCI", "2025-04-10", "2026-04-10")
]
        cur.executemany("INSERT INTO ships VALUES (?,?,?,?,?,?,?,?,?,?,?)", seed_ships)

        seed_faults = [
            ("M/V BOSPHORUS", "Ana Jeneratör No:2", "Yüksek", "2026-09-18", "Sargı izolasyon direnci düşük (0.6 MOhm).", "Açık",
             "Periyodik Bakım Eksikliği / Gecikmesi", "⚠️ Unsafe Condition (Emniyetsiz Durum)", "Hayır", 8500, 3200, "TRY", 6, "Deniz KARA", "Elektro-Teknik Zabit (ETO)", ""),
            ("M/V MED STAR", "Bow Thruster Kumanda Panosu", "Orta", "2026-09-15", "Kumanda kartı arızalı.", "Açık",
             "Malzeme / Yedek Parça Kalitesi (Ömrünü Tamamlama)", "Normal", "Hayır", 1200, 0, "USD", 12, "Ahmet YILMAZ", "Elektro-Teknik Zabit (ETO)", ""),
            ("M/T MOON STAR", "Acil Aydınlatma Devresi", "Yüksek", "2026-09-20", "Toprak kaçağı tespit edildi.", "Açık",
             "Çevresel Faktörler (Aşırı nem, tuzlu su, ağır deniz şartları)", "🔶 Near-Miss (Kıl Payı Kurtulma)", "Evet", 300, 0, "TRY", 3, "Mehmet DEMİR", "Elektro-Teknik Zabit (ETO)", ""),
            ("M/V A380", "Soğutma Kompresörü Motoru", "Düşük", "2026-09-10", "Rulman sesi artmış.", "Açık",
             "Kestirilemeyen / Beklenmeyen Parça Ömrü", "Normal", "Hayır", 450, 200, "TRY", 0, "Hasan ÇELİK", "Çarkçıbaşı", ""),
            ("M/V ATLANTIC STAR", "MSB Bus-Bar Bağlantısı", "Yüksek", "2026-09-12", "Sıcak nokta tespit edildi (85 C).", "Açık",
             "Periyodik Bakım Eksikliği / Gecikmesi", "⚠️ Unsafe Condition (Emniyetsiz Durum)", "Hayır", 0, 5000, "USD", 24, "Kemal ARSLAN", "Başmühendis", ""),
            ("M/V SAPHIRA", "Yangın Alarm Panosu", "Orta", "2026-09-08", "Zone 3 dedektörü arızalı.", "Açık",
             "Malzeme / Yedek Parça Kalitesi (Ömrünü Tamamlama)", "Normal", "Hayır", 600, 0, "TRY", 0, "Murat AVCİ", "Elektro-Teknik Zabit (ETO)", ""),
        ]
        cur.executemany("""INSERT INTO faults(gemi,ekipman,aciliyet,tespit,aciklama,status,
            kok_neden,kritiklik,tekrarlayan,parca_maliyeti,iscilik_maliyeti,para_birimi,
            downtime_saat,mudahale_eden,mudahale_departman,kapanis_tarihi)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", seed_faults)

        seed_inspections = [
            ("2026-09-20", "M/T MOON STAR", "Aylık Elektrik Denetimi", "MSB, acil jeneratör kontrol edildi. Acil aydınlatmada toprak kaçağı bulundu.", "Ahmet YILMAZ"),
            ("2026-09-18", "M/V BOSPHORUS", "Yıllık Class Survey", "Alternatör No:2 izolasyon testleri tamamlandı.", "Mehmet DEMİR"),
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

    conn.close()


def migrate_db():
    """Var olan (eski) tts_ships.db dosyalarında eksik olan yeni arıza sütunlarını ekler.
    Böylece daha önce kurulmuş ve içinde veri olan panelde veri kaybı yaşanmaz."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(faults)")
    existing_cols = {row[1] for row in cur.fetchall()}
    new_cols = {
        "kok_neden": "TEXT DEFAULT ''",
        "kritiklik": "TEXT DEFAULT 'Normal'",
        "tekrarlayan": "TEXT DEFAULT 'Hayır'",
        "parca_maliyeti": "REAL DEFAULT 0",
        "iscilik_maliyeti": "REAL DEFAULT 0",
        "para_birimi": "TEXT DEFAULT 'TRY'",
        "downtime_saat": "REAL DEFAULT 0",
        "mudahale_eden": "TEXT DEFAULT ''",
        "mudahale_departman": "TEXT DEFAULT ''",
        "kapanis_tarihi": "TEXT DEFAULT ''",
    }
    for col, coltype in new_cols.items():
        if col not in existing_cols:
            cur.execute("ALTER TABLE faults ADD COLUMN " + col + " " + coltype)
    conn.commit()
    conn.close()


init_db()
migrate_db()


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


FAULT_RENAME = {
    "gemi": "Gemi", "ekipman": "Ekipman", "aciliyet": "Aciliyet",
    "tespit": "Tespit", "aciklama": "Aciklama", "status": "Durum",
    "kok_neden": "KokNeden", "kritiklik": "Kritiklik", "tekrarlayan": "Tekrarlayan",
    "parca_maliyeti": "ParcaMaliyeti", "iscilik_maliyeti": "IscilikMaliyeti",
    "para_birimi": "ParaBirimi", "downtime_saat": "DowntimeSaat",
    "mudahale_eden": "MudahaleEden", "mudahale_departman": "MudahaleDepartman",
    "kapanis_tarihi": "KapanisTarihi",
}


def arizalar_yukle(sadece_acik=True):
    if sadece_acik:
        df = df_from("SELECT * FROM faults WHERE status='Açık' ORDER BY tespit DESC")
    else:
        df = df_from("SELECT * FROM faults ORDER BY tespit DESC")
    return df.rename(columns=FAULT_RENAME)


def hesapla_tekrar_sayisi(gemi, ekipman, gun=90):
    """Aynı gemi + ekipman için son `gun` gün içindeki geçmiş arıza sayısını döndürür
    (yeni eklenecek kayıt hariç). 0'dan büyükse yeni kayıt 'tekrarlayan' sayılır."""
    if not gemi or not ekipman:
        return 0
    gecmis = df_from("SELECT tespit FROM faults WHERE gemi=? AND ekipman=?", (gemi, ekipman))
    if gecmis.empty:
        return 0
    sinir = datetime.date.today() - datetime.timedelta(days=gun)
    sayac = 0
    for t in gecmis["tespit"]:
        try:
            tarih = datetime.date.fromisoformat(str(t)[:10])
            if tarih >= sinir:
                sayac += 1
        except Exception:
            continue
    return sayac


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
        krit_cls = "normal"
        krit_deger = str(a.get("Kritiklik", "") or "")
        if "Unsafe" in krit_deger:
            krit_cls = "unsafe"
        elif "Near-Miss" in krit_deger:
            krit_cls = "nearmiss"
        line = '<div class="fault-item ' + cls + '">'
        line += '<div><b>' + a["Gemi"] + '</b> · ' + a["Ekipman"]
        if krit_deger and krit_deger != "Normal":
            line += '<span class="crit-badge ' + krit_cls + '">' + krit_deger + '</span>'
        if str(a.get("Tekrarlayan", "")) == "Evet":
            line += '<span class="recurring-badge">🔁 Tekrarlayan</span>'
        line += '<div style="font-size:11px;color:#5a6b82;margin-top:3px;">' + a["Aciklama"] + '</div>'
        alt_bilgi = 'Tespit: ' + a["Tespit"]
        if a.get("KokNeden") and a["KokNeden"] not in ("", "Seçilmedi"):
            alt_bilgi += ' · Kök Neden: ' + a["KokNeden"]
        line += '<div style="font-size:10px;color:#7a8699;margin-top:3px;">' + alt_bilgi + '</div></div>'
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
                run("UPDATE faults SET status='Kapalı', kapanis_tarihi=? WHERE id=?",
                    (str(datetime.date.today()), fault_id))
                st.success("✅ Arıza kapatıldı. Dashboard'dan kaldırıldı; detaylı kayıt 'Gemi Arızaları' panelinde saklanmaya devam ediyor.")
                st.rerun()
        else:
            st.caption("Kapatılacak açık arıza yok.")

    with st.expander("➕ Yeni Arıza Ekle"):
        cg, ce = st.columns(2)
        with cg:
            gemi_sec = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="yeni_ariza_gemi_sec")
        with ce:
            ekipman_sec = st.text_input("Ekipman", key="yeni_ariza_ekipman_sec")

        tekrar_sayisi = hesapla_tekrar_sayisi(gemi_sec, ekipman_sec)
        if tekrar_sayisi > 0:
            st.warning(
                "⚠️ Bu ekipmanda (" + ekipman_sec + ") son 90 günde " + str(tekrar_sayisi) +
                ". kez arıza kaydı bulunuyor. Kaydedilirse bu arıza **tekrarlayan** olarak işaretlenecek."
            )

        with st.form("yeni_ariza_form"):
            c1, c2 = st.columns(2)
            with c1:
                aciliyet = st.selectbox("Aciliyet", ["Yüksek", "Orta", "Düşük"], key="yeni_ariza_aciliyet")
                tespit = st.date_input("Tespit Tarihi", datetime.date.today(), key="yeni_ariza_tarih")
                kok_neden = st.selectbox("Kök Neden (Root Cause)", KOK_NEDEN_LIST, key="yeni_ariza_kok")
                kritiklik = st.selectbox("Kritiklik / Emniyet Etkisi", KRITIKLIK_LIST, key="yeni_ariza_kritiklik")
            with c2:
                mudahale_eden = st.text_input("Müdahale Eden Personel", key="yeni_ariza_personel")
                mudahale_departman = st.selectbox("Departman", DEPARTMAN_LIST, key="yeni_ariza_departman")
                para_birimi = st.selectbox("Para Birimi", PARA_BIRIMI_LIST, key="yeni_ariza_para")

            aciklama = st.text_area("Açıklama", key="yeni_ariza_aciklama")

            st.markdown("**💰 Maliyet ve Duruş Bilgileri**")
            m1, m2, m3 = st.columns(3)
            with m1:
                parca_maliyeti = st.number_input("Yedek Parça Maliyeti", min_value=0.0, value=0.0, step=50.0, key="yeni_ariza_parca_mal")
            with m2:
                iscilik_maliyeti = st.number_input("Servis / İşçilik Maliyeti", min_value=0.0, value=0.0, step=50.0, key="yeni_ariza_iscilik_mal")
            with m3:
                downtime_saat = st.number_input("Duruş (Down-time) Süresi (saat)", min_value=0.0, value=0.0, step=0.5, key="yeni_ariza_downtime")

            if st.form_submit_button("Kaydet") and ekipman_sec:
                tekrarlayan = "Evet" if tekrar_sayisi > 0 else "Hayır"
                run(
                    """INSERT INTO faults(gemi,ekipman,aciliyet,tespit,aciklama,status,
                       kok_neden,kritiklik,tekrarlayan,parca_maliyeti,iscilik_maliyeti,
                       para_birimi,downtime_saat,mudahale_eden,mudahale_departman,kapanis_tarihi)
                       VALUES (?,?,?,?,?,'Açık',?,?,?,?,?,?,?,?,?,'')""",
                    (gemi_sec, ekipman_sec, aciliyet, str(tespit), aciklama,
                     kok_neden, kritiklik, tekrarlayan, parca_maliyeti, iscilik_maliyeti,
                     para_birimi, downtime_saat, mudahale_eden, mudahale_departman),
                )
                st.success("✅ Arıza eklendi ve 'Gemi Arızaları' analiz panelinde kalıcı olarak kayıt altına alındı.")
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


def render_fault_analytics():
    st.subheader("📊 Gemi Arızaları - Analiz ve Raporlama Paneli")
    st.caption("Bu panel tüm arıza kayıtlarını (açık + kapalı) kalıcı olarak listeler. "
               "Dashboard'da bir arıza kapatıldığında buradan silinmez; sadece açık arıza listesinden kaldırılır.")

    tum_df = df_from("SELECT * FROM faults ORDER BY tespit DESC")
    if tum_df.empty:
        st.info("Henüz arıza kaydı yok.")
        return

    tum_df = tum_df.rename(columns=FAULT_RENAME)
    tum_df["ParcaMaliyeti"] = pd.to_numeric(tum_df["ParcaMaliyeti"], errors="coerce").fillna(0)
    tum_df["IscilikMaliyeti"] = pd.to_numeric(tum_df["IscilikMaliyeti"], errors="coerce").fillna(0)
    tum_df["DowntimeSaat"] = pd.to_numeric(tum_df["DowntimeSaat"], errors="coerce").fillna(0)
    tum_df["ToplamMaliyet"] = tum_df["ParcaMaliyeti"] + tum_df["IscilikMaliyeti"]

    with st.expander("🔍 Filtrele", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            gemi_f = st.multiselect("Gemi", sorted(tum_df["Gemi"].unique().tolist()), default=[], key="fa_gemi")
        with f2:
            durum_f = st.multiselect("Durum", sorted(tum_df["Durum"].unique().tolist()), default=[], key="fa_durum")
        with f3:
            kritiklik_f = st.multiselect("Kritiklik", sorted(tum_df["Kritiklik"].unique().tolist()), default=[], key="fa_krit")
        with f4:
            kok_secenekleri = sorted([k for k in tum_df["KokNeden"].unique().tolist() if k and k != "Seçilmedi"])
            kok_f = st.multiselect("Kök Neden", kok_secenekleri, default=[], key="fa_kok")

    df = tum_df.copy()
    if gemi_f:
        df = df[df["Gemi"].isin(gemi_f)]
    if durum_f:
        df = df[df["Durum"].isin(durum_f)]
    if kritiklik_f:
        df = df[df["Kritiklik"].isin(kritiklik_f)]
    if kok_f:
        df = df[df["KokNeden"].isin(kok_f)]

    if df.empty:
        st.warning("Seçilen filtrelere uyan kayıt yok.")
        return

    acik_sayi = int((df["Durum"] == "Açık").sum())
    kapali_sayi = int((df["Durum"] == "Kapalı").sum())
    tekrar_sayi = int((df["Tekrarlayan"] == "Evet").sum())
    unsafe_sayi = int(df["Kritiklik"].astype(str).str.contains("Unsafe").sum())
    nearmiss_sayi = int(df["Kritiklik"].astype(str).str.contains("Near-Miss").sum())
    toplam_downtime = float(df["DowntimeSaat"].sum())

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Toplam Arıza", len(df))
    k2.metric("🔓 Açık", acik_sayi)
    k3.metric("🔒 Kapalı", kapali_sayi)
    k4.metric("🔁 Tekrarlayan", tekrar_sayi)
    k5.metric("⚠️ Unsafe/Near-Miss", unsafe_sayi + nearmiss_sayi)
    k6.metric("⏱️ Toplam Duruş (saat)", round(toplam_downtime, 1))

    # ortalama çözüm süresi (yalnız kapanış tarihi girilmiş kapalı arızalar için)
    kapali_df = df[(df["Durum"] == "Kapalı") & (df["KapanisTarihi"].astype(str) != "")]
    ort_cozum_suresi = None
    if not kapali_df.empty:
        sureler = []
        for _, r in kapali_df.iterrows():
            try:
                t1 = datetime.date.fromisoformat(str(r["Tespit"])[:10])
                t2 = datetime.date.fromisoformat(str(r["KapanisTarihi"])[:10])
                sureler.append((t2 - t1).days)
            except Exception:
                continue
        if sureler:
            ort_cozum_suresi = sum(sureler) / len(sureler)

    if ort_cozum_suresi is not None:
        st.caption("📈 Ortalama arıza çözüm süresi: **" + f"{ort_cozum_suresi:.1f}" + " gün** (kapatılan arızalar için)")

    st.markdown("#### 💰 Para Birimine Göre Toplam Maliyet")
    maliyet_ozet = df.groupby("ParaBirimi")["ToplamMaliyet"].sum().reset_index()
    if not maliyet_ozet.empty:
        mcols = st.columns(max(len(maliyet_ozet), 1))
        for i, (_, row) in enumerate(maliyet_ozet.iterrows()):
            mcols[i].metric(row["ParaBirimi"], f'{row["ToplamMaliyet"]:,.0f}')
    else:
        st.caption("Maliyet verisi yok.")

    st.markdown("---")

    if not PLOTLY_AVAILABLE:
        st.warning("Grafikleri görüntülemek için `plotly` kütüphanesi gerekli. Terminalde `pip install plotly` çalıştırıp uygulamayı yeniden başlatın.")
    else:
        g1, g2 = st.columns(2)
        with g1:
            kok_ozet = df[(df["KokNeden"] != "") & (df["KokNeden"] != "Seçilmedi")]["KokNeden"].value_counts().reset_index()
            kok_ozet.columns = ["KokNeden", "Adet"]
            if not kok_ozet.empty:
                fig1 = px.pie(kok_ozet, names="KokNeden", values="Adet", title="Kök Neden Dağılımı", hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.caption("Kök neden verisi girilmemiş.")
        with g2:
            krit_ozet = df["Kritiklik"].value_counts().reset_index()
            krit_ozet.columns = ["Kritiklik", "Adet"]
            fig2 = px.pie(krit_ozet, names="Kritiklik", values="Adet", title="Kritiklik / Emniyet Etkisi Dağılımı", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)

        g3, g4 = st.columns(2)
        with g3:
            gemi_ozet = df["Gemi"].value_counts().reset_index()
            gemi_ozet.columns = ["Gemi", "Adet"]
            fig3 = px.bar(gemi_ozet, x="Gemi", y="Adet", title="Gemi Bazında Arıza Sayısı", color="Adet", color_continuous_scale="Blues")
            st.plotly_chart(fig3, use_container_width=True)
        with g4:
            dep_ozet = df[df["MudahaleDepartman"] != ""]["MudahaleDepartman"].value_counts().reset_index()
            dep_ozet.columns = ["Departman", "Adet"]
            if not dep_ozet.empty:
                fig4 = px.bar(dep_ozet, x="Departman", y="Adet", title="Departman Bazında Müdahale Sayısı", color="Adet", color_continuous_scale="Oranges")
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.caption("Müdahale eden departman verisi girilmemiş.")

        df_trend = df.copy()
        df_trend["Ay"] = pd.to_datetime(df_trend["Tespit"], errors="coerce").dt.to_period("M").astype(str)
        trend_ozet = df_trend.dropna(subset=["Ay"]).groupby("Ay").size().reset_index(name="Adet")
        if not trend_ozet.empty:
            fig5 = px.line(trend_ozet, x="Ay", y="Adet", markers=True, title="Aylık Arıza Trendi")
            st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Tüm Arıza Kayıtları (Detaylı)")

    def satir_renklendir(row):
        if row["Durum"] == "Kapalı":
            return ["background-color: #f1f5f9"] * len(row)
        if "Unsafe" in str(row["Kritiklik"]):
            return ["background-color: #fdecea"] * len(row)
        if "Near-Miss" in str(row["Kritiklik"]):
            return ["background-color: #fff4e0"] * len(row)
        if row["Tekrarlayan"] == "Evet":
            return ["background-color: #fff7e6"] * len(row)
        return [""] * len(row)

    goster_kolonlar = ["Gemi", "Ekipman", "Aciliyet", "Kritiklik", "Durum", "Tespit", "KapanisTarihi",
                        "KokNeden", "Tekrarlayan", "ParcaMaliyeti", "IscilikMaliyeti", "ParaBirimi",
                        "DowntimeSaat", "MudahaleEden", "MudahaleDepartman", "Aciklama"]
    goster_df = df[goster_kolonlar]
    try:
        st.dataframe(goster_df.style.apply(satir_renklendir, axis=1), use_container_width=True)
    except Exception:
        st.dataframe(goster_df, use_container_width=True)

    with st.expander("📝 Yönetici Özeti (Sunum için kopyalanabilir metin)"):
        ozet_metin = (
            "Seçili dönemde toplam " + str(len(df)) + " arıza kaydı bulunmaktadır. "
            + str(acik_sayi) + " tanesi hâlâ açık, " + str(kapali_sayi) + " tanesi kapatılmıştır. "
            + str(tekrar_sayi) + " arıza tekrarlayan nitelikte olup, " + str(unsafe_sayi)
            + " adet Unsafe Condition ve " + str(nearmiss_sayi) + " adet Near-Miss vakası kaydedilmiştir. "
            "Arızalar toplamda " + f"{round(toplam_downtime, 1)}" + " saatlik operasyonel duruşa neden olmuştur."
        )
        if ort_cozum_suresi is not None:
            ozet_metin += " Ortalama arıza çözüm süresi " + f"{ort_cozum_suresi:.1f}" + " gündür."
        st.text_area("Özet", ozet_metin, height=120, key="fa_ozet_metin")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        goster_df.to_excel(writer, index=False, sheet_name="GemiArizalari")
    st.download_button(
        "⬇️ Excel Olarak İndir (Sunum için)",
        data=buffer.getvalue(),
        file_name="gemi_arizalari_analiz.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="fa_excel_indir",
    )


menu = st.sidebar.radio(
    "📌 Navigasyon",
    ["🏠 Dashboard", "📊 Gemi Arızaları", "🚢 Filo Yönetimi", "📜 Sertifika & Survey", "🛒 Satınalma",
     "📚 Teknik Dokümanlar", "🎓 ETO Eğitim & PSC", "⚡ Megger Kayıtları", "📄 Raporlama"],
)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 TTS Ships · v3.8 (kalıcı veri + dinamik durum + arıza analiz paneli)")

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

elif menu == "📊 Gemi Arızaları":
    render_fault_analytics()

elif menu == "🚢 Filo Yönetimi":
    st.subheader("🚢 Filo Yönetimi (Tablo Görünümü)")
    st.dataframe(fleet_df, use_container_width=True)

elif menu == "📜 Sertifika & Survey":
    st.subheader("📜 Sertifika & Survey Takibi")
    t = datetime.date.today()
    cd = [
        {"Gemi": "M/V MED STAR", "Sertifika": "Safety Equipment", "Bitis": str(t + datetime.timedelta(days=15)), "Durum": "🟡 Yakında"},
        {"Gemi": "M/V MED STAR", "Sertifika": "Load Line", "Bitis": str(t + datetime.timedelta(days=180)), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/T MOON STAR", "Sertifika": "IOPP", "Bitis": str(t + datetime.timedelta(days=5)), "Durum": "🔴 Kritik"},
        {"Gemi": "M/T MOON STAR", "Sertifika": "Safety Construction", "Bitis": str(t + datetime.timedelta(days=240)), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/T KUZEY STAR II", "Sertifika": "ISSC", "Bitis": str(t + datetime.timedelta(days=90)), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/V ATLANTIC STAR", "Sertifika": "IAPP", "Bitis": str(t - datetime.timedelta(days=3)), "Durum": "🔴 Süresi Geçti"},
        {"Gemi": "M/V PACIFIC STAR", "Sertifika": "Class Certificate", "Bitis": str(t + datetime.timedelta(days=45)), "Durum": "🟡 Yakında"},
        {"Gemi": "M/V SAPHIRA", "Sertifika": "IOPP", "Bitis": str(t + datetime.timedelta(days=320)), "Durum": "🟢 Geçerli"},
    ]
    cert_df = pd.DataFrame(cd)
    kritik_sayisi = sum(1 for d in cd if "Kritik" in d["Durum"] or "Süresi" in d["Durum"])
    yakinda_sayisi = sum(1 for d in cd if "Yakında" in d["Durum"])
    k1, k2, k3 = st.columns(3)
    k1.metric("Toplam", len(cert_df))
    k2.metric("Kritik", kritik_sayisi)
    k3.metric("Yakında", yakinda_sayisi)
    st.dataframe(cert_df, use_container_width=True)

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
    rapor_tipi = st.selectbox("Rapor Tipi", ["Filo Listesi", "Satınalma", "Megger Kayıtları", "Arızalar (Açık)", "Arızalar (Tüm - Detaylı)"])
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
    elif rapor_tipi == "Arızalar (Tüm - Detaylı)":
        df_rapor = arizalar_yukle(sadece_acik=False)
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
