import streamlit as st
import pandas as pd
import datetime
import io
import os
import sqlite3
import base64
import glob

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
/* ---- Arızalar modülü ---- */
.dz-kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:10px;margin-bottom:12px}
.dz-kpi{background:#f8fafc;border:1px solid #e3e8ef;border-radius:10px;padding:10px 12px;min-width:0}
.dz-kpi .k{font-size:10px;color:#7a8699;letter-spacing:.4px;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dz-kpi .v{font-size:22px;font-weight:700;color:#0b3d91;margin-top:2px}
.dz-kpi.v-txt .v{font-size:13.5px;line-height:1.35;white-space:normal}
.dz-kpi.v-crit{border-left:4px solid #dc2626}.dz-kpi.v-crit .v{color:#dc2626}
.dz-kpi.v-high{border-left:4px solid #f97316}.dz-kpi.v-high .v{color:#c2410c}
.dz-kpi.v-warn{border-left:4px solid #d97706}.dz-kpi.v-warn .v{color:#b76e00}
.dz-kpi.v-info{border-left:4px solid #1e6fd9}
.dz-kpi.v-ok{border-left:4px solid #16a34a}.dz-kpi.v-ok .v{color:#16a34a}
.dz-badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;white-space:nowrap}
.dz-p-critical{background:#fdecea;color:#c0392b}
.dz-p-high{background:#fff0e3;color:#c05600}
.dz-p-medium{background:#fff8e1;color:#a16207}
.dz-p-low{background:#eef2f7;color:#5a6b82}
.dz-s-open{background:#fdecea;color:#c0392b}
.dz-s-in-progress{background:#e8f1fd;color:#0b3d91}
.dz-s-waiting-spare-part{background:#fff0e3;color:#c05600}
.dz-s-waiting-service{background:#eef2f7;color:#5a6b82}
.dz-s-resolved{background:#e6f4fa;color:#1e7e34}
.dz-s-closed{background:#e6f7ee;color:#16a34a}
.dz-section{background:#fff;border:1px solid #e3e8ef;border-radius:12px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:14px;min-width:0}
.dz-section h4{margin:0 0 10px;font-size:13px;color:#0b3d91;border-bottom:2px solid #e6ecf5;padding-bottom:6px}
.dz-donut-wrap{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.dz-donut{position:relative;width:140px;height:140px;border-radius:50%;flex:0 0 auto}
.dz-donut-hole{position:absolute;left:30px;top:30px;right:30px;bottom:30px;background:#fff;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center}
.dz-donut-num{font-size:20px;font-weight:700;color:#0b3d91;line-height:1}
.dz-donut-cap{font-size:9px;color:#7a8699;margin-top:2px}
.dz-legend{font-size:11.5px;color:#333;min-width:0;flex:1}
.dz-legend div{display:flex;align-items:center;gap:6px;margin-bottom:4px}
.dz-dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
.dz-legend .lv{margin-left:auto;font-weight:700;color:#0b3d91;white-space:nowrap}
.dz-bar-row{display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:11.5px}
.dz-bar-label{flex:0 0 135px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#333}
.dz-bar-track{flex:1;min-width:40px;background:#e6ecf5;border-radius:8px;height:12px;overflow:hidden}
.dz-bar-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#1e6fd9,#0b3d91)}
.dz-bar-fill.crit{background:linear-gradient(90deg,#f87171,#dc2626)}
.dz-bar-fill.high{background:linear-gradient(90deg,#fdba74,#ea580c)}
.dz-bar-val{flex:0 0 48px;text-align:right;font-weight:700;font-size:11px;color:#0b3d91;white-space:nowrap}
.dz-field-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px 14px;font-size:11.5px;color:#333}
.dz-field b{display:block;font-size:9.5px;color:#7a8699;text-transform:uppercase;letter-spacing:.3px;font-weight:600}
.dz-full{font-size:11.5px;color:#333;margin-top:8px}
.dz-full b{color:#0b3d91;font-size:9.5px;text-transform:uppercase;letter-spacing:.3px;display:block}
.dz-timeline{border-left:2px solid #e6ecf5;margin:6px 0 0 6px;padding-left:14px;font-size:11.5px;color:#333}
.dz-timeline .ev{position:relative;margin-bottom:8px}
.dz-timeline .ev:before{content:"●";position:absolute;left:-21px;top:0;color:#1e6fd9;font-size:10px}
.dz-timeline .ev .t{font-size:10px;color:#7a8699}
.dz-report{background:#f8fafc;border:1px solid #e3e8ef;border-radius:10px;padding:12px 16px;font-size:12.5px;line-height:1.75;color:#333}
.dz-svg-chart{width:100%;height:auto;display:block}
@media (max-width:768px){
    .dz-bar-label{flex:0 0 92px;font-size:10.5px}
    .dz-donut{width:120px;height:120px}
    .dz-donut-hole{left:26px;top:26px;right:26px;bottom:26px}
    .dz-kpi .v{font-size:19px}
}
/* ---- Arıza Analiz & Raporlama ---- */
.dz-aylik{display:flex;align-items:flex-end;gap:6px}
.dz-aylik-col{flex:1;min-width:0;text-align:center}
.dz-aylik-v{font-size:9.5px;font-weight:700;color:#0b3d91;margin-bottom:2px}
.dz-aylik-alan{display:flex;align-items:flex-end;height:120px}
.dz-aylik-bar{width:100%;border-radius:4px 4px 0 0;background:linear-gradient(180deg,#1e6fd9,#0b3d91);min-height:2px}
.dz-aylik-l{font-size:9px;color:#7a8699;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:768px){
    .dz-aylik-l{font-size:8px}
    .dz-aylik-v{font-size:8.5px}
}
/* ---- Dashboard tıklanabilir KPI kartları (kart tasarımı aynı kalır,
       üstüne binen şeffaf buton katmanı sayesinde tamamı tıklanabilir) ---- */
.dz-kpi-tikla{cursor:pointer}
div[data-testid="stColumn"]:has(.dz-kpi-tikla){position:relative}
div[data-testid="stColumn"]:has(.dz-kpi-tikla) div[data-testid="stButton"]{position:absolute;inset:0;margin:0;z-index:5}
div[data-testid="stColumn"]:has(.dz-kpi-tikla) div[data-testid="stButton"] > button{
    width:100%;height:100%;background:transparent;border:0;box-shadow:none;
    color:transparent;padding:0;cursor:pointer}
div[data-testid="stColumn"]:has(.dz-kpi-tikla) div[data-testid="stButton"] > button:hover{
    background:rgba(11,61,145,.07);border-radius:10px}
div[data-testid="stColumn"]:has(.dz-kpi-tikla) div[data-testid="stButton"] > button:focus{
    outline:none;box-shadow:none}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Filo Yönetim Paneli</h1>
<p>MarineTraffic · Sertifika/Survey · Satınalma · Teknik Doküman · Personel · Megger · Excel</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# VERİTABANI (SQLite) - Uygulama kapansa/yenilense bile veriler kalıcıdır
# ------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts_ships.db")

# Gemi fotoğrafları için klasör(ler): app.py ile aynı dizinde bulunan, adı "ship_images"
# veya "gemi isimleri" olan klasörler taranır. İçindeki dosyanın adı IMO numarasıyla
# BAŞLIYORSA (uzantı ne olursa olsun, çift uzantı olsa bile) otomatik eşleştirilir.
# Örn: 9337028.jpg, 9337028.jpg.jfif, 9337028.png -> hepsi M/V MED STAR (IMO 9337028) için geçerli.
IMAGES_DIRS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "ship_images"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "gemi isimleri"),
]


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

    cur.execute("""CREATE TABLE IF NOT EXISTS personnel(
        id INTEGER PRIMARY KEY AUTOINCREMENT, ad_soyad TEXT, gorev TEXT,
        durum TEXT DEFAULT 'Gemide', gemi TEXT, katilim TEXT, inis TEXT,
        izin_giris TEXT, izin_cikis TEXT, puan REAL, notlar TEXT
    )""")

    # Arızalar modülü: merkezi elektrik/elektronik arıza kayıtları ve durum geçmişi.
    # Mevcut `faults` tablosu (eski dashboard arızaları) ile birbirine dokunmadan,
    # paralel ve zengin şemayla çalışır.
    cur.execute("""CREATE TABLE IF NOT EXISTS defects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gemi TEXT, imo TEXT, sistem TEXT, alt_sistem TEXT, ekipman TEXT,
        baslik TEXT, aciklama TEXT, ariza_tarihi TEXT, bildiren TEXT, sorumlu TEXT,
        oncelik TEXT DEFAULT 'Medium', durum TEXT DEFAULT 'Open',
        kategori TEXT, kaynak TEXT,
        gecici_cozum TEXT, kalici_cozum TEXT,
        yedek_parcasi TEXT, parca_no TEXT, parca_mevcut TEXT DEFAULT 'Hayır',
        tekrarlayan TEXT DEFAULT 'Hayır', class_flag TEXT DEFAULT 'Hayır',
        is_emri TEXT, tahmini_kapanis TEXT, gercek_kapanis TEXT,
        downtime_saat REAL DEFAULT 0, maliyet REAL DEFAULT 0,
        ek_dosya TEXT DEFAULT '', notlar TEXT DEFAULT ''
    )""")

    # Arıza durum değişikliklerinin tarihçesi (ileride audit/izlenebilirlik altyapısı)
    cur.execute("""CREATE TABLE IF NOT EXISTS defect_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect_id INTEGER, tarih TEXT, islem TEXT, detay TEXT,
        eski_deger TEXT, yeni_deger TEXT
    )""")

    # Yedek Parça & Malzeme İhtiyaçları tablosu (ileride Dashboard'un ana veri kaynağı)
    cur.execute("""CREATE TABLE IF NOT EXISTS spare_parts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gemi TEXT, imo TEXT, sistem TEXT, ekipman TEXT,
        malzeme TEXT, parca_no TEXT, marka_model TEXT,
        ihtiyac_miktar INTEGER DEFAULT 1, mevcut_stok INTEGER DEFAULT 0,
        siparis_miktar INTEGER DEFAULT 0, birim TEXT DEFAULT 'adet',
        oncelik TEXT DEFAULT 'Medium', durum TEXT DEFAULT 'İhtiyaç',
        talep_tarihi TEXT, ihtiyac_tarihi TEXT,
        tedarikci TEXT, siparis_no TEXT, tahmini_teslim TEXT,
        kritik_parca TEXT DEFAULT 'Hayır', ariza_iliskili TEXT DEFAULT 'Hayır',
        ilgili_ariza_id INTEGER, notlar TEXT DEFAULT ''
    )""")

    # Eskimiş kayıtları güncel durum listesine hizala (Waiting Service artık seçenek değil;
    # sadece bu modülün kendi tablosuna dokunur, diğer verilere etkisi yoktur)
    cur.execute("UPDATE defects SET durum='In Progress' WHERE durum='Waiting Service'")

    conn.commit()

    # Bakım temizliği: M/V BOSPHORUS filoda yer almıyor, önceki sürümde yanlışlıkla
    # eklenmişti. Zaten mevcut olmayan kayıtlar için DELETE no-op olduğundan
    # bu blok her başlatmada güvenle çalışır (var olan DB'leri de otomatik düzeltir).
    for tbl in ("ships", "faults", "inspections", "materials", "purchases", "megger", "certificates", "personnel", "defects"):
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

    # Personel tablosu için ayrı seed kontrolü: 15 gemide görevli elektrik zabitini +
    # 7 izinde (gemi dışında) personeli örnek olarak yükler. Kontrat ve izin tarihleri
    # bugüne göre dinamik hesaplanır; kontrat süreleri gemi tipine göre seçilir
    # (tanker 4 ay, konteyner 5 ay, kuruyük 6 ay, hayvan 6 ay; Ro-Ro ve genel kargo
    # 5 ay) ve bitiş tarihleri daima gelecekte olacak şekilde üretilir.
    cur.execute("SELECT COUNT(*) FROM personnel")
    if cur.fetchone()[0] == 0:
        t0 = datetime.date.today()
        sure_gun = {
            "Container": 152,      # 5 ay
            "Tanker": 122,         # 4 ay
            "Ro-Ro Cargo": 152,    # 5 ay
            "General Cargo": 152,  # 5 ay
            "Bulk Carrier": 183,   # 6 ay
            "Live Stock": 183,     # 6 ay
        }
        tip_map = {}
        for g, tip in cur.execute("SELECT gemi, tip FROM ships").fetchall():
            tip_map[g] = tip

        # (ad_soyad, gorev, gemi, kontratbasi_gun_once, puan, notlar)
        gemideki_personel = [
            ("Ahmet YILMAZ", "ETO", "M/V MED STAR", 74, 88, "Deneyimli, PSC'de görev aldı."),
            ("Mehmet DEMİR", "Elektrik Zabiti", "M/T MOON STAR", 49, 76, "Megger eğitimini tamamladı."),
            ("Ali KAYA", "ETO", "M/T KUZEY STAR II", 22, 91, ""),
            ("Hasan ÇELİK", "Elektrik Zabiti", "M/V A380", 95, 72, "Yeni sözleşme, uyum sürecinde."),
            ("Emre ŞAHİN", "ETO", "M/V AKBABA", 38, 84, "Panel imalatı tecrübesi var."),
            ("Serkan AYDIN", "Elektrik Zabiti", "M/V ALEXANDRA I", 133, 70, ""),
            ("Burak ÖZTÜRK", "ETO", "M/V ALENA", 83, 79, ""),
            ("Kemal ARSLAN", "ETO", "M/V ATLANTIC STAR", 34, 95, "Termal kamera sertifikalı."),
            ("Onur YILDIZ", "Elektrik Zabiti", "M/V PACIFIC STAR", 100, 74, "Yangın alarm sistemleri uzmanı."),
            ("Volkan KOÇ", "ETO", "M/V CHIEF SEATTLE", 18, 86, ""),
            ("Cem POLAT", "Elektrik Zabiti", "M/V VENUS STAR", 66, 81, "Bow thruster bakımında deneyimli."),
            ("Barış TAŞ", "ETO", "M/V MERCUR STAR", 52, 77, "MSB bakımlarında sorumlu."),
            ("Tolga ERDOĞAN", "Elektrik Zabiti", "M/V DENIZ STAR", 13, 69, "Gemiye yeni katıldı, uyum sürecinde."),
            ("Yusuf KURT", "ETO", "M/V BLACKSEA STAR", 86, 83, ""),
            ("Murat AVCİ", "Elektrik Zabiti", "M/V SAPHIRA", 115, 90, "Jeneratör kontrol sistemlerine hâkim."),
        ]
        seed_personel = []
        for ad, gorev, gemi, gun_once, puan, notlar in gemideki_personel:
            giris = t0 - datetime.timedelta(days=gun_once)
            bitis = giris + datetime.timedelta(days=sure_gun.get(tip_map.get(gemi), 152))
            seed_personel.append((ad, gorev, "Gemide", gemi, str(giris), str(bitis), "", "", float(puan), notlar))

        # Gemide olmayan (izinde) 7 personel - izin tarihleri bugünü kapsar
        # (ad_soyad, gorev, izin_giris_gun_once, izin_cikis_gun_sonra, puan, notlar)
        izindeki_personel = [
            ("Mert ÖZDEMİR", "ETO", 18, 12, 82, "Yeni kontrat öncesi izinde."),
            ("Serkan ŞEN", "Elektrik Zabiti", 5, 9, 74, "Yedek personel, görev bekliyor."),
            ("Hüseyin AKSOY", "ETO", 13, 17, 89, "PSC deneyimi yüksek."),
            ("Furkan ÇETİN", "Elektrik Zabiti", 3, 11, 71, "Talep bekliyor."),
            ("Ozan KARACA", "ETO", 22, 7, 78, "Aile izni."),
            ("Erdem TAŞKIN", "Elektrik Zabiti", 8, 22, 85, "Kurs dönüşü, sertifikalar yenilendi."),
            ("Levent UÇAR", "ETO", 1, 13, 80, "Kısa izin dönüşü, gemi bekliyor."),
        ]
        for ad, gorev, gun_once, gun_sonra, puan, notlar in izindeki_personel:
            izin_g = t0 - datetime.timedelta(days=gun_once)
            izin_c = t0 + datetime.timedelta(days=gun_sonra)
            seed_personel.append((ad, gorev, "İzinde", "—", "", "", str(izin_g), str(izin_c), float(puan), notlar))

        cur.executemany(
            "INSERT INTO personnel(ad_soyad,gorev,durum,gemi,katilim,inis,izin_giris,izin_cikis,puan,notlar) VALUES (?,?,?,?,?,?,?,?,?,?)",
            seed_personel,
        )
        conn.commit()

    # ARIZALAR MODÜLÜ örnek veri seed (sadece defects boşsa; tüm gemilere yayılır)
    cur.execute("SELECT COUNT(*) FROM defects")
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT gemi, imo, eto FROM ships ORDER BY gemi")
        gemi_kayit = [(r[0], r[1], r[2]) for r in cur.fetchall()]
        if gemi_kayit:
            # (gemi_idx, gun_once, sistem, alt_sistem, ekipman, baslik, aciklama,
            #  oncelik, durum, kaynak, tekrarlayan, gecici_cozum, kalici_cozum,
            #  yedek_parcasi, parca_no, parca_mevcut, class_flag, downtime, maliyet)
            ornek_arizalar = [
                (0, 12, "Generator", "AVR / Voltage Regulation", "No.1 Jeneratör AVR", "Generator AVR fault", "1. ana jeneratör AVR arızası; çıkış gerilimleri dengesiz.", "High", "Closed", "Alarm", "Evet", "Jeneratör geçici olarak tek hatta çalıştırıldı.", "AVR modülü değiştirildi, yük testi yapıldı.", "AVR Modülü", "AVR-4400", "Evet", "Hayır", 6.5, 1480.0),
                (0, 47, "Main Switchboard", "Feeder", "MSB 4. Feeder Kesici", "Main switchboard breaker trip", "Ana pano 4. feeder kesicisi kısa devrede açıldı.", "Medium", "Closed", "Crew Report", "Evet", "Yük geçici olarak 5. hatta alındı.", "Kesici temizlendi, izolasyon ve kısa devre testi geçti.", "Kesici Mekanizması", "BRK-250A", "Hayır", "Hayır", 3.0, 420.0),
                (0, 96, "Lighting", "Deck Lighting", "Güvert Aydınlatma Devresi", "Lighting circuit earth fault", "Ana güvertede toprak kaçağı nedeniyle devre açıyor.", "Low", "Closed", "Inspection", "Hayır", "Arıza devre ayırıcıyla izole edildi.", "Kablo ucu yenilendi, izolasyon ölçümü geçti.", "Kablo Ucu Seti", "CLS-110", "Evet", "Hayır", 2.0, 180.0),
                (0, 6, "Battery / UPS", "UPS", "AC kW UPS Cihazı", "UPS battery low alarm", "UPS batarya voltajı düşük; yedekleme süresi kısaldı.", "High", "In Progress", "Alarm", "Hayır", "UPS bypass konumuna alındı.", "Batarya bankası değişimi planlandı.", "UPS Batarya 12V", "BAT-12100", "Hayır", "Hayır", 0.0, 2240.0),
                (1, 9, "Generator", "Cooling", "No.2 Jeneratör Soğutma", "Generator high temperature alarm", "2. jeneratör soğutma suyu sıcaklık alarmı devreye girdi.", "Critical", "Closed", "Alarm", "Hayır", "Jeneratör durduruldu, yük 1. jeneratöre alındı.", "Deniz suyu pompası segeli değiştirildi, test edildi.", "Pompa Segeli", "SEA-08N", "Evet", "Hayır", 8.0, 760.0),
                (1, 34, "Communication", "GMDSS", "VHF Set 1", "VHF communication fault", "VHF 1 cihazında ses iletişimi kesildi; TX sesi gelmiyor.", "High", "Waiting Spare Part", "Inspection", "Hayır", "Yedek handset ile geçici sağlandı.", "El mikrofonu değişimi bekleniyor.", "VHF Handset", "VHF-HS2", "Hayır", "Evet", 0.0, 640.0),
                (1, 62, "Boiler", "Burner Control", "Ekzozer Brülör Kontrol", "Boiler control fault", "Kazan brülör kontrol kartı arızası; otomatik ateşleme yapmıyor.", "Medium", "Closed", "ETO", "Evet", "Kazan manuel kontrolle devrede tutuldu.", "Kontrol kartı değiştirildi, brülör testi yapıldı.", "Brülör Kontrol Kartı", "BRC-300", "Evet", "Hayır", 5.0, 1320.0),
                (1, 247, "Navigation", "Gyro", "Gyro Puseta", "Gyro transmission error", "Gyro puseta transmisyon kutusunda hata alarmı.", "Medium", "Closed", "Inspection", "Hayır", "GF testiyle rota doğrulandı.", "Transmisyon kutusu kalibre edildi.", "Transmisyon Kutusu", "GYR-220", "Hayır", "Evet", 0.0, 980.0),
                (2, 18, "Generator", "AVR", "No.1 Jeneratör", "Generator low voltage", "1. jeneratörde düşük gerilim alarmı; voltaj %15 düşüyor.", "Critical", "In Progress", "Alarm", "Hayır", "Paralel dışı yükler tek jeneratöre alındı.", "AVR ve gerilim sensörü kontrolü sürüyor.", "Gerilim Sensörü", "AVR-S15", "Hayır", "Hayır", 4.0, 0.0),
                (2, 55, "Emergency Switchboard", "Feeder", "Acil Pano Besleme", "Emergency switchboard earth fault", "Acil pano besleme hattında toprak kaçağı alarmı.", "High", "Closed", "Inspection", "Hayır", "Topraklama hattı geçici izole edildi.", "Kablo testiyle kaçak noktası bulunup onarıldı.", "Kablo Bezi", "CBL-EE-09", "Evet", "Evet", 4.5, 1150.0),
                (2, 15, "Pump", "Ballast", "Sıyırıcı Pompa Motoru", "Pump motor insulation fault", "Sıyırıcı pompa motoru izolasyon direnci 0.2 MΩ'a düştü.", "High", "In Progress", "PMS", "Hayır", "Pompa devreden alındı, nakliye planlandı.", "Motor sarım servisi bekleniyor.", "Sargı Servisi", "MTR-SRV-1", "Hayır", "Hayır", 12.0, 3200.0),
                (3, 21, "HVAC", "Compressor", "Soğutma Kompresörü Motoru", "HVAC motor fault", "Klima kompresör motorunda rulman sesi ve akım dengesizliği.", "Medium", "Closed", "Crew Report", "Hayır", "Cihaz fan konumunda çalıştırıldı.", "Rulmanlar değiştirildi, akım dengesi sağlandı.", "Rulman Seti", "BRG-6205", "Evet", "Hayır", 3.5, 390.0),
                (3, 64, "PLC", "Remote I/O", "Güverte PLC I/O", "PLC communication failure", "PLC ile uzak I/O arasında Profinet haberleşmesi koptu.", "High", "Closed", "Alarm", "Evet", "Kritik ekipmanlar yerel kumandaya alındı.", "Switch port ve kablo uçları yenilendi.", "Patch Kablo", "PN-CAT6", "Evet", "Hayır", 5.5, 520.0),
                (3, 4, "Deck Equipment", "Windlass", "İnci Motoru Kumanda", "Windlass control electrical fault", "İnci motoru kumanda devresinde kontaktör arızası.", "Medium", "Open", "Master", "Hayır", "İnci işlemi manuel kumandayla yapıldı.", "Kontaktör değişimi bekleniyor.", "Kontaktör", "KTC-65", "Hayır", "Hayır", 0.0, 0.0),
                (4, 27, "Emergency Generator", "Battery / Starting", "Acil Jeneratör Bataryası", "Emergency generator battery fault", "Acil jeneratör start bataryası şarj almıyor; voltaj 21 V.", "Critical", "Closed", "Inspection", "Evet", "Batarya harici şarj cihazıyla desteklendi.", "Batarya ve şarj regülatörü değiştirildi.", "Start Bataryası", "BAT-1050", "Evet", "Evet", 6.0, 1690.0),
                (4, 73, "Automation", "Alarm Panel", "Aydınlatma Panosu Kumanda", "Lighting control automation fault", "Aydınlatma otomasyon paneli zaman saati hatalı çalışıyor.", "Low", "Closed", "ETO", "Hayır", "Aydınlatmalar manuel çalıştı.", "Zaman saati değiştirildi, program yüklendi.", "Zaman Saati", "TMR-24", "Evet", "Hayır", 1.5, 240.0),
                (4, 11, "Safety Equipment", "Fire Detection", "Yangın Algılama Paneli", "Fire detection loop fault", "Yangın algılama 2. loop'ta kısa devre alarmı.", "Critical", "In Progress", "Inspection", "Hayır", "Loop 2 geçici olarak devre dışı bırakıldı.", "Loop kablosu izolasyon testi sürüyor.", "Loop Kablosu", "FD-LOOP2", "Hayır", "Evet", 2.0, 0.0),
                (5, 39, "Motor", "Winch", "Vinç Travers Motoru", "Motor insulation fault", "Vinç travers motorunda izolasyon direnci sınırın altında.", "High", "Closed", "PMS", "Hayır", "Vinç kullanımı kısıtlandı.", "Motor sökülüp kurutuldu, vernik yenilendi.", "İzolasyon Verniği", "VRN-C10", "Evet", "Hayır", 9.0, 1850.0),
                (5, 76, "Battery / UPS", "Battery Bank", "Ana Batarya Bankası", "Battery cell short", "Batarya bankasında 1 hücre kısa devre; seviye düşüyor.", "Medium", "Closed", "Inspection", "Hayır", "Arızalı hücre izole edildi.", "Hücre değiştirildi, yük testi yapıldı.", "Batarya Hücresi", "CEL-2V800", "Hayır", "Hayır", 4.0, 1450.0),
                (5, 5, "Communication", "Gyro Repeater", "Asterisk Repeater", "Repeater signal loss", "Gyro tekrarlayıcı sinyali köprü üstünde kesiliyor.", "Medium", "In Progress", "Crew Report", "Hayır", "Analog rota göstergesi kullanılıyor.", "Sinyal hattı ölçümleri devam ediyor.", "Sinyal Kablosu", "SIG-09", "Hayır", "Hayır", 0.0, 0.0),
                (6, 31, "VFD / Inverter", "Drive", "Ventilatör VFD", "VFD overcurrent", "Fan VFD'sinde aşırı akım hatası; drive trip veriyor.", "High", "Closed", "Alarm", "Evet", "Fan manuel kontaktörle çalıştırıldı.", "Motor kabloları ölçüldü, parametreler güncellendi.", "Drive Modülü", "VFD-55K", "Hayır", "Hayır", 5.0, 1760.0),
                (6, 196, "Lighting", "Navigation Lights", "Seyir Lambaları Devresi", "Navigation light circuit fault", "Seyir lambaları devresinde sigorta sürekli eriyor.", "Medium", "Closed", "Master", "Hayır", "Yedek lamba devresi devreye alındı.", "Kısa devre noktası bulunup onarıldı.", "Sigorta Seti", "FUS-5A", "Evet", "Evet", 3.0, 260.0),
                (6, 15, "Cargo Equipment", "Grain System", "Havalandırma Fanı Kumanda", "Cargo fan starter fault", "Yük havalandırma fanı kontaktörü çekmiyor.", "Medium", "Waiting Spare Part", "Crew Report", "Hayır", "Fanlar sırayla tek tek çalıştırılıyor.", "24V kontaktör sipariş edildi.", "Kontaktör 24V", "KTC-24", "Hayır", "Hayır", 6.0, 480.0),
                (7, 2, "Main Switchboard", "Bus", "Ana Pano Bara", "MSB earth fault alarm", "Ana panoda topraklama hatasında arıza tespit edildi (bara altı).", "Critical", "Open", "Alarm", "Evet", "Yükler tek bara üzerinden besleniyor.", "Bölgesel izolasyon ölçümü planlandı.", "Megger Cihazı", "MEG-5K", "Hayır", "Evet", 0.0, 0.0),
                (7, 25, "Automation", "Power Management", "PMS Ünitesi", "PMS load sharing fault", "Yük paylaşım hatası; jeneratörler otomatik devreye girmiyor.", "High", "In Progress", "ETO", "Hayır", "Jeneratörler manuel paralelleme ile başlatılıyor.", "PMS kartı ve akım transformatörleri kontrol ediliyor.", "PMS Kontrol Kartı", "PMS-C4", "Hayır", "Hayır", 7.5, 0.0),
                (7, 58, "Alarm & Monitoring", "AMS", "Alarm Monitoring PC", "Alarm monitoring communication fault", "AMS ekranı ile alan cihazlar arasındaki haberleşme kesildi.", "High", "Closed", "Crew Report", "Evet", "Kritik alarmlar lokal panelden izlendi.", "Switch ve adresleme yenilendi, sistem test edildi.", "Network Switch", "SW-8P", "Evet", "Hayır", 5.0, 890.0),
                (7, 300, "Motor", "Bilge Pump", "Bilge Pompası Motoru", "Motor overload trip", "Bilge pompası motorunda aşırı yüklenme nedeniyle açıyor.", "Medium", "Closed", "PMS", "Hayır", "Pompa devreye periyodik olarak alındı.", "Rulman değişimi ve yük dengesi yapıldı.", "Rulman Seti", "BRG-6306", "Evet", "Hayır", 4.0, 540.0),
                (8, 20, "Generator", "Fuel Oil", "No.1 Jeneratör Yakıt Pompası", "Generator fuel pump fault", "1. jeneratör yakıt besleme pompası arızası; motor stop ediyor.", "Critical", "Closed", "Alarm", "Hayır", "Yük 2. jeneratöre devredildi.", "Yakıt pompası segeli ve filtre değiştirildi.", "Yakıt Pompası Segesi", "FOP-12", "Evet", "Hayır", 7.0, 1120.0),
                (8, 51, "HVAC", "Fan Motoru", "Kamaralar Klima Fanı", "HVAC fan motor fault", "Kamaralar kliması fan motoru yağlaması bitmiş, gürültülü.", "Low", "Closed", "Crew Report", "Hayır", "Cihaz kademeli çalıştırıldı.", "Motor bakımı yapıldı, yağ değişti.", "Fan Motoru", "MTR-F45", "Hayır", "Hayır", 2.5, 430.0),
                (8, 7, "PLC", "Engine Room PLC", "Makine Daire PLC", "PLC module failure", "PLC rack üzerindeki DI modülü arızalı, girişler okunmuyor.", "High", "Waiting Spare Part", "Alarm", "Hayır", "Ekipmanlar lokal kumandaya alındı.", "DI modülü sipariş edildi, teslim bekleniyor.", "DI Modül 32", "PLC-DI32", "Hayır", "Hayır", 9.0, 1580.0),
                (9, 36, "Navigation", "ECDIS", "ECDIS Cihazı", "ECDIS communication fault", "ECDIS ile AIS arasında hata mesajı, veri akışı kesildi.", "High", "Closed", "Inspection", "Hayır", "GPS verisi doğrudan ECDIS'e alındı.", "Seri port ve kablo yenilendi, test edildi.", "Seri Dönüştürücü", "CON-RS232", "Evet", "Hayır", 3.5, 610.0),
                (9, 236, "Communication", "MF/HF", "MF/HF Telsiz", "MF/HF PA fault", "MF/HF güç amplifikatörü arızası, TX yapılamıyor.", "Medium", "Closed", "Inspection", "Hayır", "Acil durumlar için VHF kullanıldı.", "PA modülü tamir edildi, çıkış gücü test edildi.", "PA Modül", "HF-PA250", "Hayır", "Evet", 6.5, 2150.0),
                (9, 14, "Emergency Switchboard", "Auto Changeover", "Acil Pano Otomatik Transfer", "Emergency switch auto transfer failure", "Acil şebeke-jeneratör otomatik transferi devreye girmiyor.", "Critical", "In Progress", "Inspection", "Evet", "Transfer manuel olarak yapıldı.", "Zaman rölesi ve kontrol kablosu kontrol ediliyor.", "Zaman Rölesi", "TR-8S", "Hayır", "Evet", 5.5, 0.0),
                (10, 29, "Generator", "Control", "No.2 Jeneratör Kontrol Paneli", "Generator controller fault", "Jeneratör kontrol ünitesi reboot döngüsünde.", "High", "Open", "Alarm", "Hayır", "Jeneratör kumandası kablolu start ile yürütülüyor.", "Kontrol ünitesi yedeği için talep açıldı.", "Kontrol Ünitesi", "GCU-220", "Hayır", "Hayır", 0.0, 0.0),
                (10, 63, "Boiler", "Photocell", "Kazan Fotosel", "Boiler flame failure", "Kazan alev fotoseli sinyal vermiyor; alev arızası.", "Medium", "Closed", "Alarm", "Evet", "Fotosel temizliği yapıldı, geçici çözüm.", "Fotosel değiştirildi, yanma testi geçti.", "Fotosel", "PCL-60", "Evet", "Hayır", 3.0, 350.0),
                (10, 3, "Battery / UPS", "Emergency Lighting", "Acil Aydınlatma Bataryası", "Emergency lighting battery fault", "Acil aydınlatma armatürlerinde batarya tutmuyor.", "Low", "In Progress", "Inspection", "Hayır", "Armatürler şebekeye bağlı çalıştırıldı.", "Batarya değişimi vardiya planına alındı.", "NiCd Batarya", "BAT-NICD", "Hayır", "Hayır", 0.0, 0.0),
                (11, 44, "Pump", "Fire Pump", "Yangın Pompası Motoru", "Fire pump motor fault", "Yangın pompası motorunda başlangıç akımı çok yüksek.", "Critical", "Closed", "PMS", "Hayır", "Yangın hattı basınçlandı, test yapıldı.", "Motor devreye alındı, start devresi yenilendi.", "Start Kondansatörü", "CAP-120", "Evet", "Evet", 6.0, 1260.0),
                (11, 283, "Main Switchboard", "Compensator", "Ana Pano Kondansatör Bankası", "Capacitor bank fault", "Kondansatör bankasında güvenli devre elemanı açtı.", "Medium", "Closed", "ETO", "Hayır", "Reaktif güç telafisi devre dışı bırakıldı.", "Arızalı kovan değiştirildi.", "Kapasitör Kovanı", "CAP-10K5", "Hayır", "Hayır", 2.5, 720.0),
                (11, 10, "Deck Equipment", "Crane", "Güverte Vinç Kumanda", "Crane control fault", "Vinç kumanda kolunda sinyal dalgalanması, hareket düzensiz.", "High", "In Progress", "Crew Report", "Hayır", "Vinç kullanımı durduruldu.", "Dış servis (joystick) değişimi planlandı.", "Joystick", "JST-4W", "Hayır", "Hayır", 10.0, 0.0),
                (12, 23, "VFD / Inverter", "Ballast VFD", "Balast Pompası Drive", "VFD DC bus overvoltage", "Balast pompası drive'ında DC bar aşırı gerilim hatası.", "Medium", "Closed", "Alarm", "Evet", "Pompa diğer hattan çalıştırıldı.", "Fren direnci ve parametreler kontrol edildi.", "Fren Direnci", "RES-30R", "Hayır", "Hayır", 4.0, 680.0),
                (12, 48, "Automation", "Remote Terminal", "Uzak Terminal Ünitesi", "RTU I/O failure", "RTU analog giriş kanalı arızalı; tank seviyeleri okunmuyor.", "High", "Closed", "Inspection", "Hayır", "Seviyeler elle okundu.", "Analog giriş kartı değiştirildi.", "Analog Giriş Kartı", "RTU-AI8", "Hayır", "Hayır", 5.5, 1490.0),
                (12, 1, "Battery / UPS", "Charger", "Batarya Şarj Cihazı", "Battery charger fault", "Şarj cihazında çıkış yok; batarya deşarj oluyor.", "Critical", "Open", "Alarm", "Hayır", "Geçici şarj cihazıyla batarya desteklendi.", "Şarj cihazı kartı incelenecek.", "Şarj Modülü", "CHG-24-50", "Hayır", "Hayır", 0.0, 0.0),
                (13, 16, "Motor", "Fan", "Jeneratör Soğutma Fanı", "Fan motor winding fault", "Soğutma fanı motoru sarımında nem/kısa devre şüphesi.", "High", "Waiting Spare Part", "PMS", "Hayır", "Fan devreden alındı, jeneratör yükü kısıldı.", "Yedek motor sipariş edildi.", "Fan Motoru 3kW", "MTR-F30", "Hayır", "Hayır", 11.0, 2650.0),
                (13, 318, "Safety Equipment", "Emergency Power", "Acil Aydınlatma Besleme", "Emergency power inverter fault", "Acil güç invertöründe fan arızası ve aşırı sıcaklık.", "Medium", "Closed", "Inspection", "Evet", "Invertör bypass'a alındı.", "Fan ve filtre değiştirildi, test edildi.", "Invertör Fanı", "INV-F12", "Evet", "Hayır", 3.0, 570.0),
                (13, 16, "Navigation", "Radar", "Radar Vericisi", "Radar transmitter fault", "Radar MRT hatası; verici tüp gücü düşüyor.", "High", "In Progress", "Master", "Hayır", "Yedek radar cihazından seyir yapıldı.", "MRT ve dalga kılavuzu kontrol ediliyor.", "MRT Ünitesi", "RDR-MRT", "Hayır", "Hayır", 6.5, 0.0),
                (14, 42, "Cargo Equipment", "Ventilation", "Yük Havalandırma Kumanda", "Cargo ventilation control fault", "Yük havalandırma panosunda kumanda rölesi arızalı.", "Medium", "Closed", "Crew Report", "Hayır", "Havalandırma manuel başlatıldı.", "Röle grubu değiştirildi.", "Röle Grubu", "RLY-8CH", "Evet", "Hayır", 3.5, 460.0),
                (14, 66, "Communication", "Internal Phone", "Dahili Telefon Santrali", "Internal phone line fault", "Dahili telefonda 3. kat hattı çalışmıyor.", "Low", "Resolved", "Crew Report", "Hayır", "Telsizle iletişim sağlandı.", "Kablo armatürü yenilendi.", "Telefon Armatürü", "TEL-J45", "Hayır", "Hayır", 1.5, 150.0),
                (14, 5, "Motor", "Pump Motor", "Su Pompası Motoru", "Pump motor bearing noise", "Su pompası motoru rulman sesi artmış, titreşim yüksek.", "Medium", "Open", "ETO", "Hayır", "Pompa periyodik kontrol altında.", "Rulman değişimi planlandı.", "Rulman Seti", "BRG-6308", "Hayır", "Hayır", 0.0, 0.0),
            ]
            bildirenler = ["Kaptan İsmail YÜCE", "Başmühendis Kadir ÖZKAN", "Kaptan Hakan ASLAN", "Başmühendis Tolga KARACA", "Kaptan Murat BOZKURT"]
            bugun_t0 = datetime.date.today()
            for i, satir in enumerate(ornek_arizalar):
                (gi, gun_once, sistem, alt_sistem, ekipman, baslik, aciklama,
                 oncelik, durum, kaynak, tekrarlayan, gecici, kalici,
                 parca, parca_no, parca_mevcut, class_flag, downtime, maliyet) = satir
                gemi, imo, eto = gemi_kayit[gi % len(gemi_kayit)]
                tarih = bugun_t0 - datetime.timedelta(days=gun_once)
                tahmini = str(tarih + datetime.timedelta(days=14))
                gercek = ""
                if durum in ("Closed", "Resolved"):
                    sure = {"Critical": 2, "High": 4, "Medium": 7, "Low": 10}.get(oncelik, 7) + (i % 4)
                    gercek = str(min(bugun_t0, tarih + datetime.timedelta(days=sure)))
                    downtime_kayit = float(downtime)
                else:
                    downtime_kayit = 0.0 if durum in ("Open", "In Progress") else float(downtime)
                if tekrarlayan == "Evet":
                    notlar = "Tekrarlayan arıza olarak işaretlendi; PMS takip listesine alındı."
                elif durum == "Waiting Spare Part":
                    notlar = "Yedek parça tedariki bekleniyor; Satınalma birimine bilgi verildi."
                elif durum in ("Open", "In Progress"):
                    notlar = "İnceleme devam ediyor; ETO vardiya defterinde takipte."
                else:
                    notlar = "ETO vardiya defterine işlendi."
                # Kategori, spesifikasyondaki kategori listesiyle hizalı tutulur
                kategori = {"Automation": "Automation / PLC", "PLC": "Automation / PLC",
                            "Deck Equipment": "Cargo Equipment"}.get(sistem, sistem)
                cur.execute(
                    """INSERT INTO defects(gemi,imo,sistem,alt_sistem,ekipman,baslik,aciklama,
                       ariza_tarihi,bildiren,sorumlu,oncelik,durum,kategori,kaynak,
                       gecici_cozum,kalici_cozum,yedek_parcasi,parca_no,parca_mevcut,
                       tekrarlayan,class_flag,is_emri,tahmini_kapanis,gercek_kapanis,
                       downtime_saat,maliyet,ek_dosya,notlar)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (gemi, imo, sistem, alt_sistem, ekipman, baslik, aciklama,
                     str(tarih), bildirenler[i % len(bildirenler)],
                     eto or "ETO Atama Yok", oncelik, durum, kategori, kaynak,
                     gecici, kalici, parca, parca_no, parca_mevcut,
                     tekrarlayan, class_flag, "WO-" + str(2600 + i), tahmini, gercek,
                     downtime_kayit, float(maliyet), "", notlar),
                )
                did = cur.lastrowid
                ts = str(tarih) + " 08:00"
                cur.execute(
                    "INSERT INTO defect_history(defect_id,tarih,islem,detay,eski_deger,yeni_deger) VALUES (?,?,?,?,?,?)",
                    (did, ts, "Oluşturuldu", "Arıza kaydı oluşturuldu", "", "Open"),
                )
                if durum != "Open":
                    cur.execute(
                        "INSERT INTO defect_history(defect_id,tarih,islem,detay,eski_deger,yeni_deger) VALUES (?,?,?,?,?,?)",
                        (did, (gercek or ts), "Durum değişikliği", "Arıza işleme süreci işlendi", "Open", durum),
                    )
            conn.commit()

    # Yedek Parça & Malzeme İhtiyaçları örnek veri seed (sadece spare_parts boşsa çalışır)
    cur.execute("SELECT COUNT(*) FROM spare_parts")
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT gemi, imo FROM ships ORDER BY gemi")
        gemi_kayit = [(r[0], r[1]) for r in cur.fetchall()]
        cur.execute("SELECT id FROM defects ORDER BY id")
        ariza_idler = [r[0] for r in cur.fetchall()]
        if gemi_kayit:
            # (gemi_idx, sistem, ekipman, malzeme, parca_no, marka, ihtiyac, stok,
            #  siparis, birim, oncelik, durum, talep_gun, ihtiyac_gun, tedarikci,
            #  siparis_no, teslim_gun(None=teslim tarihi yok), kritik, ariza_iliskili, notlar)
            ornek_spare = [
                (0, "Generator", "No.1 Jeneratör AVR", "AVR Modülü", "AVR-4400", "Basler", 1, 0, 1, "adet", "Critical", "Sipariş Verildi", 18, 12, "Marine Elektrik A.Ş.", "PO-2026-118", 8, "Evet", "Evet", "Açık arıza kaydı ile ilişkili; teslim bekleniyor."),
                (0, "Main Switchboard", "MSB 4. Feeder Kesici", "Kesici Mekanizması 250A", "BRK-250A", "Siemens", 2, 1, 1, "adet", "High", "Talep Edildi", 10, 25, "Deniz Pano Ltd.", "", None, "Hayır", "Hayır", "Yedek feeder kesici olarak talep edildi."),
                (1, "Generator", "No.2 Jeneratör Soğutma Fanı", "Fan Motoru 1.5kW", "MTR-F15", "ABB", 1, 0, 1, "adet", "High", "Sipariş Verildi", 22, 10, "Marine Elektrik A.Ş.", "PO-2026-112", 6, "Evet", "Evet", "Sıcaklık arızası sürecinde talep edildi."),
                (1, "Communication", "VHF Set 1", "VHF El Mikrofonu", "VHF-HS2", "Furuno", 2, 0, 2, "adet", "Medium", "Beklemede", 28, 20, "Navigasyon Denizcilik", "PO-2026-105", 12, "Hayır", "Evet", "Sipariş tedarikçi onayı bekliyor."),
                (2, "Battery / UPS", "AC kW UPS Cihazı", "UPS Aküsü 12V 100Ah", "BAT-12100", "Yuasa", 8, 2, 6, "adet", "Critical", "Sipariş Verildi", 14, 18, "Akü Sanayi A.Ş.", "PO-2026-124", 9, "Evet", "Hayır", "Kritik yedek parça; mevcut stok 2 adet."),
                (2, "Pump", "Sıyırıcı Pompa Motoru", "Pompa Motoru 5.5kW", "MTR-P55", "Weg", 1, 0, 1, "adet", "High", "Talep Edildi", 9, 30, "Motor Teknik Ltd.", "", None, "Evet", "Evet", "Sarım servisi ile eşzamanlı yedek aranıyor."),
                (3, "Automation / PLC", "Güverte PLC Rack", "PLC DI Modül 32", "PLC-DI32", "Siemens", 2, 0, 2, "adet", "High", "Sipariş Verildi", 20, 14, "Otomasyon Deniz", "PO-2026-117", 7, "Evet", "Evet", "Profinet haberleşme arızası ile ilişkili."),
                (3, "HVAC", "Kamaralar Kliması", "Rulman Seti 6205", "BRG-6205", "SKF", 4, 1, 4, "adet", "Low", "Geldi", 35, 0, "Rulman Ticaret", "PO-2026-099", -5, "Hayır", "Hayır", "Stok yenilendi."),
                (4, "Emergency Generator", "Acil Jeneratör Start", "Start Aküsü 12V 100Ah", "BAT-1050", "Varta", 2, 0, 2, "adet", "Critical", "Talep Edildi", 7, 10, "Akü Sanayi A.Ş.", "", None, "Evet", "Evet", "Acil jeneratör batarya arızası ile ilişkili."),
                (4, "Lighting", "Güvert Aydınlatma", "LED Deniz Armatürü", "LED-D12", "Eaton", 6, 0, 6, "adet", "Low", "İhtiyaç", 5, 40, "Deniz Aydınlatma", "", None, "Hayır", "Hayır", "Aydınlatma devresi çalışması için talep listesinde."),
                (5, "Navigation", "Gyro Puseta", "Transmisyon Kutusu", "GYR-220", "Furuno", 1, 0, 1, "adet", "Medium", "Sipariş Verildi", 26, 15, "Navigasyon Denizcilik", "PO-2026-109", 10, "Hayır", "Evet", "Kalibrasyon sonrası değişim planlandı."),
                (5, "Motor", "Vinç Travers Motoru", "İzolasyon Verniği", "VRN-C10", "Elantas", 2, 1, 1, "adet", "Medium", "Geldi", 40, 0, "Boya Kimya", "PO-2026-096", -10, "Hayır", "Hayır", "Sarım bakımı için kullanıldı."),
                (6, "VFD / Inverter", "Ventilatör VFD", "Drive Fan Modülü", "VFD-FAN55", "ABB", 1, 0, 1, "adet", "High", "Beklemede", 24, 16, "Otomasyon Deniz", "PO-2026-114", 20, "Evet", "Evet", "Modül yurt içi tedarik bekliyor."),
                (6, "Lighting", "Seyir Lambaları Devresi", "Sigorta 5×20 5A", "FUS-5A", "Littelfuse", 20, 8, 20, "adet", "Low", "Geldi", 50, 0, "Elektrik Malzeme Paz.", "PO-2026-091", -12, "Hayır", "Hayır", "Stok yeterli seviyeye getirildi."),
                (13, "Cargo Equipment", "Havalandırma Fanı Kumanda", "Kontaktör 24V DC", "KTC-24", "Schneider", 2, 0, 2, "adet", "Medium", "Talep Edildi", 12, 21, "Deniz Pano Ltd.", "", None, "Hayır", "Evet", "Fan starter arızası ile ilişkili."),
                (7, "Main Switchboard", "Ana Pano Topraklama", "Topraklama Şeridi 25mm²", "GND-25", "Prysmian", 30, 10, 20, "metre", "Medium", "İptal", 30, 18, "Kablo Denizcilik", "PO-2026-101", None, "Hayır", "Hayır", "Proje değişikliği nedeniyle iptal edildi."),
                (7, "Automation / PLC", "PMS Ünitesi", "PMS Kontrol Kartı", "PMS-C4", "ComAp", 1, 0, 1, "adet", "Critical", "Sipariş Verildi", 16, 9, "Otomasyon Deniz", "PO-2026-120", 14, "Evet", "Evet", "Load sharing arızası ile ilişkili."),
                (14, "Alarm & Monitoring", "AMS Alan Ünitesi", "Network Switch 8P", "SW-8P", "Moxa", 2, 0, 2, "adet", "Medium", "Talep Edildi", 11, 25, "Otomasyon Deniz", "", None, "Hayır", "Evet", "Haberleşme kopukluğu kayıtlı."),
                (8, "Generator", "No.1 Jeneratör Yakıt Pompası", "Yakıt Pompası Segesi", "FOP-12", "Caterpillar", 4, 2, 2, "adet", "High", "Geldi", 28, 0, "Yedek Parça A.Ş.", "PO-2026-098", -3, "Hayır", "Evet", "Mühür ve filtre ile birlikte değiştirildi."),
                (8, "PLC", "Makine Daire PLC", "DI Modül 32 Kanal", "PLC-DI32", "Siemens", 1, 0, 1, "adet", "High", "Sipariş Verildi", 19, 13, "Otomasyon Deniz", "PO-2026-122", 5, "Evet", "Evet", "DI kanal arızası raporlandı."),
                (9, "Navigation", "ECDIS Cihazı", "Seri Dönüştürücü RS232", "CON-RS232", "Moxa", 1, 1, 0, "adet", "Medium", "Geldi", 45, -2, "Navigasyon Denizcilik", "PO-2026-092", -8, "Hayır", "Hayır", "Takım değişiminde kuruldu."),
                (9, "Communication", "MF/HF Telsiz", "PA Modül 250W", "HF-PA250", "JRC", 1, 0, 1, "adet", "Medium", "Sipariş Verildi", 33, 20, "Navigasyon Denizcilik", "PO-2026-107", 16, "Hayır", "Evet", "Onarım yerine yedek tercih edildi."),
                (13, "Emergency Switchboard", "Acil Pano Transfer", "Zaman Rölesi 8P", "TR-8S", "Schneider", 2, 1, 1, "adet", "High", "Talep Edildi", 6, 14, "Deniz Pano Ltd.", "", None, "Evet", "Evet", "Otomatik transfer arızası ile ilişkili."),
                (10, "Generator", "No.2 Jeneratör Kontrol Paneli", "Kontrol Ünitesi GCU", "GCU-220", "Deep Sea", 1, 0, 1, "adet", "High", "Sipariş Verildi", 21, 12, "Otomasyon Deniz", "PO-2026-119", 10, "Evet", "Evet", "Reboot döngüsü arızası kayıtlı."),
                (10, "Boiler", "Kazan Brülör", "Fotosel", "PCL-60", "Honeywell", 2, 0, 2, "adet", "Medium", "Geldi", 38, -4, "Kazan Teknik", "PO-2026-095", -10, "Hayır", "Evet", "Değişim tamamlandı."),
                (14, "Battery / UPS", "Acil Aydınlatma", "NiCd Batarya Modülü", "BAT-NICD", "EnerSys", 6, 0, 6, "adet", "Low", "İhtiyaç", 4, 35, "Akü Sanayi A.Ş.", "", None, "Hayır", "Hayır", "Yıllık bakım planına eklendi."),
                (11, "Pump", "Yangın Pompası", "Start Kondansatörü 120µF", "CAP-120", "Vishay", 3, 1, 2, "adet", "Critical", "Talep Edildi", 8, 11, "Elektrik Malzeme Paz.", "", None, "Evet", "Evet", "Yangın pompası arızası ile ilişkili."),
                (11, "Main Switchboard", "Kondansatör Bankası", "Kapasitör Kovanı 10kVAr", "CAP-10K5", "EPCOS", 2, 0, 2, "adet", "Medium", "İptal", 27, 19, "Deniz Pano Ltd.", "", None, "Hayır", "Hayır", "Alternatif kompanzasyon çözümü nedeniyle iptal."),
                (12, "VFD / Inverter", "Balast Pompası Drive", "Fren Direnci 30R", "RES-30R", "ABB", 1, 0, 1, "adet", "Medium", "İhtiyaç", 7, 28, "Otomasyon Deniz", "", None, "Hayır", "Evet", "DC bar arıza kaydı ile ilişkili."),
                (12, "Battery / UPS", "Batarya Şarj Cihazı", "Şarj Modülü 24V/50A", "CHG-24-50", "Eltek", 1, 0, 1, "adet", "Critical", "Kısmi Geldi", 13, 10, "Güç Sistemleri", "PO-2026-123", 4, "Evet", "Evet", "Kısmi teslim edildi; kart bekleniyor."),
            ]
            bugun_s = datetime.date.today()
            sql_spare = ("INSERT INTO spare_parts(gemi,imo,sistem,ekipman,malzeme,parca_no,marka_model,"
                         "ihtiyac_miktar,mevcut_stok,siparis_miktar,birim,oncelik,durum,"
                         "talep_tarihi,ihtiyac_tarihi,tedarikci,siparis_no,tahmini_teslim,"
                         "kritik_parca,ariza_iliskili,ilgili_ariza_id,notlar) VALUES ("
                         + ",".join(["?"] * 22) + ")")
            for i, satir in enumerate(ornek_spare):
                (gi, sistem, ekipman, malzeme, parca_no, marka, ihtiyac, stok,
                 siparis, birim, oncelik, durum, talep_gun, ihtiyac_gun, tedarikci,
                 siparis_no, teslim_gun, kritik, ariza_iliskili, notlar) = satir
                gemi, imo = gemi_kayit[gi % len(gemi_kayit)]
                talep_t = str(bugun_s - datetime.timedelta(days=talep_gun))
                ihtiyac_t = str(bugun_s + datetime.timedelta(days=ihtiyac_gun))
                teslim_t = "" if teslim_gun is None else str(bugun_s + datetime.timedelta(days=teslim_gun))
                ilgili = None
                if ariza_iliskili == "Evet" and ariza_idler:
                    ilgili = ariza_idler[i % len(ariza_idler)]
                cur.execute(sql_spare, (
                    gemi, imo, sistem, ekipman, malzeme, parca_no, marka,
                    int(ihtiyac), int(stok), int(siparis), birim, oncelik, durum,
                    talep_t, ihtiyac_t, tedarikci, siparis_no, teslim_t,
                    kritik, ariza_iliskili, ilgili, notlar,
                ))
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
    # ETO ve kontrat bilgileri Personel modülünden beslenir (tek kaynak budur)
    p = df_from("SELECT gemi, ad_soyad, katilim, inis FROM personnel WHERE durum='Gemide'")
    pmap = {r["gemi"]: r for _, r in p.iterrows()}
    df["ETO"] = df["Gemi"].apply(lambda g: pmap[g]["ad_soyad"] if g in pmap else "Atama Yok")
    df["Giris"] = df["Gemi"].apply(lambda g: pmap[g]["katilim"] if g in pmap else "")
    df["KontratBitis"] = df["Gemi"].apply(lambda g: pmap[g]["inis"] if g in pmap else "")
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
    """IMAGES_DIRS altındaki klasörlerde IMO numarasıyla BAŞLAYAN bir dosya arar
    (uzantı/çift uzantı fark etmez) ve bulursa base64 data-uri olarak döner.
    Görsel türü dosya adındaki uzantıya değil, dosyanın gerçek byte imzasına bakılarak belirlenir
    (yükleme sırasında yanlış/çift uzantı verilmiş dosyalarda bile doğru çalışır)."""
    if not imo:
        return None
    for klasor in IMAGES_DIRS:
        if not os.path.isdir(klasor):
            continue
        eslesenler = sorted(glob.glob(os.path.join(klasor, str(imo) + "*")))
        for path in eslesenler:
            if not os.path.isfile(path):
                continue
            try:
                with open(path, "rb") as f:
                    veri = f.read()
            except Exception:
                continue
            if veri[:3] == b"\xff\xd8\xff":
                mime = "image/jpeg"
            elif veri[:8] == b"\x89PNG\r\n\x1a\n":
                mime = "image/png"
            elif veri[:4] == b"RIFF" and veri[8:12] == b"WEBP":
                mime = "image/webp"
            elif veri[:6] in (b"GIF87a", b"GIF89a"):
                mime = "image/gif"
            else:
                continue  # tanınmayan/bozuk dosya, atla
            data = base64.b64encode(veri).decode()
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


def _tarih_iso(d):
    """date_input'tan gelen değeri ISO (YYYY-MM-DD) metnine çevirir; boşsa '' döner."""
    if d is None or d == "":
        return ""
    if isinstance(d, datetime.datetime):
        return d.date().isoformat()
    if isinstance(d, datetime.date):
        return d.isoformat()
    try:
        return datetime.date.fromisoformat(str(d)).isoformat()
    except Exception:
        return ""


def _iso_tarih(s):
    """ISO metnini date_input için date nesnesine çevirir; boş/geçersizse None döner."""
    try:
        return datetime.date.fromisoformat(str(s))
    except Exception:
        return None


# ------------------------------------------------------------------
# ARIZALAR MODÜLÜ SABİT/YARDIMCILARI
# ------------------------------------------------------------------
ARIZA_ONCELIK = ["Critical", "High", "Medium", "Low"]
ARIZA_DURUMLAR = ["Open", "In Progress", "Waiting Spare Part", "Resolved", "Closed"]
ARIZA_ACIK_DURUMLAR = ["Open", "In Progress", "Waiting Spare Part"]
ARIZA_KATEGORILER = [
    "Generator", "Main Switchboard", "Emergency Generator", "Emergency Switchboard",
    "Motor", "Pump", "VFD / Inverter", "Automation / PLC", "Alarm & Monitoring",
    "Navigation", "Communication", "Battery / UPS", "Lighting", "Boiler", "HVAC",
    "Cargo Equipment", "Safety Equipment", "Other",
]
ARIZA_KAYNAKLAR = [
    "ETO", "Chief Engineer", "Master", "PMS", "Inspection", "Alarm",
    "Crew Report", "Class", "Port State Control", "Other",
]
# Sistem seçenekleri: kategori listesi + örnek veride kullanılan ayrı sistem adları
ARIZA_SISTEMLER = sorted(set(ARIZA_KATEGORILER + ["Automation", "PLC", "Deck Equipment"]))
# Yedek Parça & Malzeme İhtiyaçları durum seçenekleri (öncelik için ARIZA_ONCELIK kullanılır)
SPAR_DURUMLAR = ["İhtiyaç", "Talep Edildi", "Sipariş Verildi", "Kısmi Geldi",
                 "Geldi", "Beklemede", "İptal"]


def defects_yukle():
    """defects tablosunu ekran adlarıyla yükler (Arızalar modülünün tek veri kaynağı)."""
    df = df_from("SELECT * FROM defects ORDER BY ariza_tarihi DESC, id DESC")
    return df.rename(columns={
        "id": "ID", "gemi": "Gemi", "imo": "IMO", "sistem": "Sistem",
        "alt_sistem": "AltSistem", "ekipman": "Ekipman", "baslik": "Ariza",
        "aciklama": "Aciklama", "ariza_tarihi": "Tarih", "bildiren": "Bildiren",
        "sorumlu": "Sorumlu", "oncelik": "Oncelik", "durum": "Durum",
        "kategori": "Kategori", "kaynak": "Kaynak", "gecici_cozum": "GeciciCozum",
        "kalici_cozum": "KaliciCozum", "yedek_parcasi": "YedekParca",
        "parca_no": "ParcaNo", "parca_mevcut": "ParcaMevcut",
        "tekrarlayan": "Tekrarlayan", "class_flag": "ClassFlag",
        "is_emri": "IsEmri", "tahmini_kapanis": "TahminiKapanis",
        "gercek_kapanis": "GercekKapanis", "downtime_saat": "Downtime",
        "maliyet": "Maliyet", "ek_dosya": "EkDosya", "notlar": "Notlar",
    })


def defect_gecmis_yukle(defect_id):
    """Seçili arızanın durum/işlem tarihçesini yükler."""
    return df_from(
        "SELECT * FROM defect_history WHERE defect_id=? ORDER BY id ASC",
        (int(defect_id),),
    )


def defect_gecmis_ekle(defect_id, islem, detay="", eski="", yeni=""):
    """Arıza için audit/tarihçe kaydı yazar (durum değişiklikleri dahil)."""
    run(
        "INSERT INTO defect_history(defect_id,tarih,islem,detay,eski_deger,yeni_deger) VALUES (?,?,?,?,?,?)",
        (int(defect_id), datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
         islem, detay, eski, yeni),
    )


def spare_parts_yukle():
    """spare_parts tablosunu ekran adlarıyla yükler (Yedek Parça modülünün tek veri kaynağı)."""
    df = df_from("SELECT * FROM spare_parts ORDER BY id DESC")
    return df.rename(columns={
        "id": "ID", "gemi": "Gemi", "imo": "IMO", "sistem": "Sistem",
        "ekipman": "Ekipman", "malzeme": "Malzeme", "parca_no": "ParcaNo",
        "marka_model": "Marka", "ihtiyac_miktar": "Ihtiyac", "mevcut_stok": "Stok",
        "siparis_miktar": "Siparis", "birim": "Birim", "oncelik": "Oncelik",
        "durum": "Durum", "talep_tarihi": "TalepTarihi", "ihtiyac_tarihi": "IhtiyacTarihi",
        "tedarikci": "Tedarikci", "siparis_no": "SiparisNo", "tahmini_teslim": "TeslimTarihi",
        "kritik_parca": "Kritik", "ariza_iliskili": "ArizaIliskili",
        "ilgili_ariza_id": "IlgiliAriza", "notlar": "Notlar",
    })


def sp_detay_html(r):
    """Seçili malzeme/ihtiyaç kaydının tüm alanlarını gösterir."""

    def temiz(alan):
        v = r[alan]
        try:
            if pd.isna(v):
                return "—"
        except Exception:
            pass
        s = str(v).strip()
        return "—" if s in ("", "nan", "None") else s

    h = '<div class="dz-section"><h4>📦 Malzeme Detayı #' + str(r["ID"]) + " · " + temiz("Malzeme") + "</h4>"
    h += '<div class="dz-field-grid">'
    alanlar = [
        ("Gemi", temiz("Gemi")), ("IMO No", temiz("IMO")),
        ("Sistem", temiz("Sistem")), ("Ekipman", temiz("Ekipman")),
        ("Parça No", temiz("ParcaNo")), ("Marka / Model", temiz("Marka")),
        ("İhtiyaç Miktarı", temiz("Ihtiyac") + " " + temiz("Birim")),
        ("Mevcut Stok", temiz("Stok") + " " + temiz("Birim")),
        ("Sipariş Miktarı", temiz("Siparis") + " " + temiz("Birim")),
        ("Öncelik", dz_oncelik_badge(temiz("Oncelik"))), ("Durum", temiz("Durum")),
        ("Talep Tarihi", temiz("TalepTarihi")), ("İhtiyaç Tarihi", temiz("IhtiyacTarihi")),
        ("Tedarikçi", temiz("Tedarikci")), ("Sipariş No", temiz("SiparisNo")),
        ("Tahmini Teslim", temiz("TeslimTarihi")), ("Kritik Yedek Parça", temiz("Kritik")),
        ("Arıza ile İlişkili", temiz("ArizaIliskili")), ("İlgili Arıza ID", temiz("IlgiliAriza")),
    ]
    for k, v in alanlar:
        h += '<div class="dz-field"><b>' + k + "</b>" + v + "</div>"
    h += "</div>"
    h += '<div class="dz-full"><b>Notlar</b>' + temiz("Notlar") + "</div></div>"
    return h


def dz_oncelik_badge(oncelik):
    return '<span class="dz-badge dz-p-' + str(oncelik).lower() + '">' + str(oncelik) + "</span>"


def dz_durum_badge(durum):
    return '<span class="dz-badge dz-s-' + str(durum).lower().replace(" ", "-") + '">' + str(durum) + "</span>"


def dz_kpi_html(kartlar):
    """(etiket, değer, css_sinifi) listesinden özet kartı ızgarası üretir."""
    h = '<div class="dz-kpi-grid">'
    for etiket, deger, sinif in kartlar:
        h += ('<div class="dz-kpi ' + sinif + '"><div class="k">' + str(etiket) +
              '</div><div class="v">' + str(deger) + "</div></div>")
    return h + "</div>"


def ariza_detay_html(r, hist):
    """Seçili arızanın tüm alanlarını, çözüm/parça/maliyet bilgilerini ve tarihçesini basar."""

    def temiz(alan):
        v = r[alan]
        try:
            if pd.isna(v):
                return "—"
        except Exception:
            pass
        s = str(v).strip()
        return "—" if s in ("", "nan", "None") else s

    h = '<div class="dz-section"><h4>🔍 Arıza Detayı #' + str(r["ID"]) + " · " + temiz("Ariza") + "</h4>"
    h += '<div class="dz-field-grid">'
    alanlar = [
        ("Gemi", temiz("Gemi")), ("IMO No", temiz("IMO")),
        ("Sistem", temiz("Sistem")), ("Alt Sistem", temiz("AltSistem")),
        ("Ekipman", temiz("Ekipman")), ("Kategori", temiz("Kategori")),
        ("Arıza Tarihi", temiz("Tarih")), ("Arıza Kaynağı", temiz("Kaynak")),
        ("Bildiren Kişi", temiz("Bildiren")), ("Sorumlu Kişi", temiz("Sorumlu")),
        ("Öncelik", dz_oncelik_badge(temiz("Oncelik"))), ("Durum", dz_durum_badge(temiz("Durum"))),
        ("İş Emri No", temiz("IsEmri")), ("Class / Flag Bildirimi", temiz("ClassFlag")),
        ("Tahmini Kapanış", temiz("TahminiKapanis")), ("Gerçek Kapanış", temiz("GercekKapanis")),
        ("Downtime (saat)", temiz("Downtime")), ("Maliyet (USD)", temiz("Maliyet")),
        ("Tekrarlayan Arıza", temiz("Tekrarlayan")), ("Yedek Parça Mevcut", temiz("ParcaMevcut")),
        ("Ek Dosyalar", temiz("EkDosya")),
    ]
    for k, v in alanlar:
        h += '<div class="dz-field"><b>' + k + "</b>" + v + "</div>"
    h += "</div>"
    for baslik, alan in (
        ("Arıza Açıklaması", "Aciklama"),
        ("Geçici Çözüm", "GeciciCozum"),
        ("Kalıcı Çözüm", "KaliciCozum"),
        ("Kullanılan Yedek Parça", "YedekParca"),
        ("Parça Numarası", "ParcaNo"),
        ("Notlar", "Notlar"),
    ):
        h += '<div class="dz-full"><b>' + baslik + "</b>" + temiz(alan) + "</div>"
    h += '<div class="dz-full" style="margin-top:12px"><b>🕙 Tarihçe / Yapılan İşlemler</b></div>'
    h += '<div class="dz-timeline">'
    if hist is None or len(hist) == 0:
        h += '<div class="ev">Bu arıza için henüz işlem kaydı yok.</div>'
    else:
        for _, e in hist.iterrows():
            olay = ('<div class="ev"><span class="t">' + str(e.get("tarih", "")) + "</span> · <b>" +
                    str(e.get("islem", "")) + "</b>")
            detay = str(e.get("detay", "") or "")
            if detay.strip():
                olay += " — " + detay
            eski = str(e.get("eski_deger", "") or "")
            yeni = str(e.get("yeni_deger", "") or "")
            if eski.strip() or yeni.strip():
                olay += " (" + (eski or "-") + " → " + (yeni or "-") + ")"
            h += olay + "</div>"
    h += "</div></div>"
    return h


def ra_bar_html(satirlar, en_fazla=20):
    """Arıza Analiz modülü için yatay bar grafiği; satirlar: [(etiket, deger, renk)] (renk None olabilir)."""
    if not satirlar:
        return '<div style="font-size:11.5px;color:#7a8699;">Veri yok</div>'
    satirlar = [(str(e), float(v), r) for e, v, r in satirlar][:en_fazla]
    maks = max([v for _, v, _ in satirlar] + [0.0])
    h = ""
    for etiket, deger, renk in satirlar:
        gz = (deger / maks * 100.0) if maks > 0 else 0.0
        stil = 'style="width:' + format(gz, ".1f") + '%"' + ((";background:" + renk) if renk else "")
        h += ('<div class="dz-bar-row"><span class="dz-bar-label" title="' + etiket + '">' + etiket + "</span>"
              '<div class="dz-bar-track"><div class="dz-bar-fill" ' + stil + "></div></div>"
              '<span class="dz-bar-val">' + str(int(deger)) + "</span></div>")
    return h


def ra_aylik_html(etiketler, degerler):
    """Aylık trend için dikey kolon grafik (CSS: dz-aylik*)."""
    if not degerler:
        return '<div style="font-size:11.5px;color:#7a8699;">Veri yok</div>'
    maks = max(list(degerler) + [1])
    h = '<div class="dz-aylik">'
    for e, v in zip(etiketler, degerler):
        yuzde = (float(v) / maks * 100.0) if maks > 0 else 0.0
        if v and yuzde < 5:
            yuzde = 5.0
        h += ('<div class="dz-aylik-col"><div class="dz-aylik-v">' + str(int(v)) + "</div>"
              '<div class="dz-aylik-alan"><div class="dz-aylik-bar" style="height:' + format(yuzde, ".1f") + '%"></div></div>'
              '<div class="dz-aylik-l">' + str(e) + "</div></div>")
    return h + "</div>"


def personel_df_yukle():
    """personnel tablosunu yükler; kontrat süresi ve kalan süreyi türetir."""
    df = df_from(
        "SELECT * FROM personnel "
        "ORDER BY CASE WHEN durum='Gemide' THEN 0 ELSE 1 END, gemi ASC, ad_soyad ASC"
    )
    df = df.rename(columns={
        "id": "id", "ad_soyad": "AdSoyad", "gorev": "Gorev", "durum": "Durum",
        "gemi": "Gemi", "katilim": "Katilim", "inis": "Inis",
        "izin_giris": "IzinGiris", "izin_cikis": "IzinCikis",
        "puan": "Puan", "notlar": "Notlar",
    })
    if df.empty:
        df["KontratSure"] = []
        df["Kalan"] = []
        return df
    sure_list = []
    kalan_list = []
    for _, r in df.iterrows():
        if r["Durum"] == "Gemide" and r["Katilim"] and r["Inis"]:
            try:
                bas = datetime.date.fromisoformat(r["Katilim"])
                bit = datetime.date.fromisoformat(r["Inis"])
                toplam = (bit - bas).days
                if toplam > 0:
                    sure_list.append(str(max(1, round(toplam / 30.44))) + " ay")
                    kalan = (bit - datetime.date.today()).days
                    if kalan < 0:
                        kalan_list.append("🔴 " + str(abs(kalan)) + " gün önce bitti")
                    elif kalan <= 30:
                        kalan_list.append("🔴 " + str(kalan) + " gün")
                    elif kalan <= 90:
                        kalan_list.append("🟡 " + str(kalan) + " gün")
                    else:
                        kalan_list.append("🟢 " + str(kalan) + " gün")
                    continue
            except Exception:
                pass
        sure_list.append("—")
        kalan_list.append("—")
    df["KontratSure"] = sure_list
    df["Kalan"] = kalan_list
    return df


def ship_card_html(row, pers=None):
    cls = ""
    if "Arıza" in row["Durum"]:
        cls = "err"
    elif "Bakım" in row["Durum"]:
        cls = "warn"
    emoji_map = {"Container": "📦", "Tanker": "🛢️", "Bulk Carrier": "⛏️", "Ro-Ro Cargo": "🚗", "General Cargo": "📦", "Live Stock": "🐄"}
    tip_emoji = emoji_map.get(row["Tip"], "🚢")
    h = '<div class="ship-card"><div class="card-flex">'
    h += '<div class="eto-left">'
    h += '<div class="eto-avatar">👤</div>'
    # Personel adı, görevi ve kontrat barı Personel modülünden gelir (pers=None ise atama yoktur)
    if pers is not None:
        h += '<div class="eto-name">👨‍✈️ ' + str(pers["AdSoyad"]) + '</div>'
        h += '<div class="eto-role">' + str(pers["Gorev"]) + '</div>'
        kalan, yuzde, kcls = kontrat_bilgi(str(pers["Katilim"]), str(pers["Inis"]))
        if kalan < 0:
            kalan_text = "⚠️ Kontrat " + str(abs(kalan)) + " gün önce bitti"
        elif kalan == 0:
            kalan_text = "⏰ Kontrat bugün bitiyor"
        else:
            kalan_text = "⏳ " + str(kalan) + " gün kaldı (%" + str(yuzde) + ")"
        h += '<div class="contract-box">'
        h += '<div class="contract-dates"><span>📅 ' + str(pers["Katilim"]) + '</span><span>' + str(pers["Inis"]) + '</span></div>'
        h += '<div class="progress-track"><div class="progress-fill ' + kcls + '" style="width:' + str(yuzde) + '%;"></div></div>'
        h += '<div class="contract-remaining ' + kcls + '">' + kalan_text + '</div>'
        h += '</div>'
    else:
        h += '<div class="eto-name">👤 Atama Yok</div>'
        h += '<div class="eto-role">Personel atanmadı</div>'
        h += '<div class="contract-box"><div class="contract-remaining warn">Personel ataması bekleniyor</div></div>'
    # Yalnızca eto-left'ı kapat; card-flex açık kalmalı ki ship-right (resim + gemi
    # bilgisi) avatarın HEMEN YANINDAKİ sıralı boşluğa yerleşsin, altına düşmesin.
    h += '</div>'
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


def render_dashboard_ariza_kartlari():
    """Dashboard ARIZALAR kartları: gerçek sayılar, yalnızca başlık + büyük sayı.
    Kartın tamamı tıklanabilir; tıklanınca ⚠️ Arızalar modülü ilgili filtreyle açılır."""
    dz = defects_yukle()
    if dz.empty:
        st.info("Kayıtlı arıza yok.")
        return
    acik = int(dz["Durum"].isin(ARIZA_ACIK_DURUMLAR).sum())
    kritik = int((dz["Oncelik"] == "Critical").sum())
    high = int((dz["Oncelik"] == "High").sum())
    ilerleme = int((dz["Durum"] == "In Progress").sum())
    yedek = int((dz["Durum"] == "Waiting Spare Part").sum())
    tekr = int((dz["Tekrarlayan"] == "Evet").sum())
    kartlar = [
        ("🔴 Açık Arızalar", acik, "v-crit", {"durum": ARIZA_ACIK_DURUMLAR}),
        ("🚨 Critical", kritik, "v-crit", {"oncelik": ["Critical"]}),
        ("🟠 High", high, "v-high", {"oncelik": ["High"]}),
        ("🔧 In Progress", ilerleme, "v-info", {"durum": ["In Progress"]}),
        ("📦 Waiting Spare Part", yedek, "v-warn", {"durum": ["Waiting Spare Part"]}),
        ("🔁 Tekrarlayan Arızalar", tekr, "v-info", {}),
    ]
    kolonlar = st.columns(6)
    for i, (baslik, deger, sinif, filtre) in enumerate(kartlar):
        with kolonlar[i]:
            st.markdown(
                '<div class="dz-kpi ' + sinif + ' dz-kpi-tikla"><div class="k">' + baslik +
                '</div><div class="v">' + str(deger) + "</div></div>",
                unsafe_allow_html=True,
            )
            if st.button(" ", key="dz_dash_kart_" + str(i), use_container_width=True):
                if filtre:
                    st.session_state["dz_hizli_filtre"] = filtre
                else:
                    st.session_state.pop("dz_hizli_filtre", None)
                st.session_state["nav_menu"] = "⚠️ Arızalar"
                st.rerun()


menu = st.sidebar.radio(
    "📌 Navigasyon",
    ["🏠 Dashboard", "🚢 Filo Yönetimi", "📜 Sertifika & Survey", "🛒 Satınalma",
     "📚 Teknik Dokümanlar", "Personel (Elektrik Zabitleri)", "⚡ Megger Kayıtları", "📄 Raporlama",
     "⚠️ Arızalar", "📈 Arıza Analiz & Raporlama", "📦 Yedek Parça & Malzeme İhtiyaçları"],
    key="nav_menu",
)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 TTS Ships · v4.0 (kalıcı veri + personel modülü + dinamik durum + sertifika DB + gemi fotoğrafları)")

fleet_df = fleet_df_yukle()
personel_df = personel_df_yukle()
personel_map = {}
for _, _p in personel_df.iterrows():
    if _p["Durum"] == "Gemide" and _p["Gemi"] not in personel_map:
        personel_map[_p["Gemi"]] = _p

if menu == "🏠 Dashboard":
    st.subheader("📊 Filo Genel Durum")
    # Tek sade kart: başlık + büyük sayı (alt etiketler kaldırıldı)
    st.metric("Toplam Gemi", len(fleet_df))
    st.markdown("---")

    # ARIZALAR — doğrudan defects verisinden beslenen, tıklanabilir Dashboard kartları
    render_dashboard_ariza_kartlari()
    st.markdown("---")

    rows = fleet_df.to_dict("records")
    for i in range(0, len(rows), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(rows):
                with col:
                    satir = rows[i + j]
                    st.markdown(ship_card_html(satir, personel_map.get(satir["Gemi"])), unsafe_allow_html=True)
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

elif menu == "Personel (Elektrik Zabitleri)":
    st.subheader("👤 Personel (Elektrik Zabitleri)")
    p_df = personel_df
    gemide_sayi = int((p_df["Durum"] == "Gemide").sum()) if not p_df.empty else 0
    izinde_sayi = int((p_df["Durum"] == "İzinde").sum()) if not p_df.empty else 0
    try:
        ort_puan = round(float(p_df["Puan"].mean()), 1) if not p_df.empty else 0.0
    except Exception:
        ort_puan = 0.0
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Toplam Personel", len(p_df))
    g2.metric("🚢 Gemide", gemide_sayi)
    g3.metric("🌴 İzinde", izinde_sayi)
    g4.metric("⭐ Ortalama Puan", ort_puan)
    st.markdown("---")

    if p_df.empty:
        st.info("Kayıtlı personel yok.")
    else:
        goster = p_df[[
            "AdSoyad", "Gorev", "Durum", "Gemi", "Katilim", "Inis", "KontratSure",
            "Kalan", "Puan", "IzinGiris", "IzinCikis", "Notlar",
        ]].replace("", "—")
        st.dataframe(goster, use_container_width=True)

    gemi_listesi = fleet_df["Gemi"].tolist()
    gorev_secenekleri = ["Elektrik Zabiti", "ETO"]
    durum_secenekleri = ["Gemide", "İzinde"]

    # --- Yeni personel ekle ---
    with st.expander("➕ Yeni Personel Ekle"):
        with st.form("yeni_personel_form"):
            n1, n2, n3 = st.columns(3)
            with n1:
                ad_soyad = st.text_input("Ad Soyad")
                gorev = st.selectbox("Görev Tanımı", gorev_secenekleri, key="np_gorev")
                durum = st.selectbox("Durum", durum_secenekleri, key="np_durum")
            with n2:
                gemi = st.selectbox("Gemi", gemi_listesi, key="np_gemi")
                katilim = st.date_input("Gemiye Katılım Tarihi", value=None, key="np_katilim")
                inis = st.date_input("İniş / Kontrat Bitiş", value=None, key="np_inis")
            with n3:
                izin_giris = st.date_input("İzin Giriş Tarihi", value=None, key="np_izin_giris")
                izin_cikis = st.date_input("İzin Çıkış Tarihi", value=None, key="np_izin_cikis")
                puan = st.number_input("Genel Değerlendirme Puanı (0-100)", min_value=0, max_value=100, value=75, step=1, key="np_puan")
            notlar = st.text_area("Notlar")
            st.caption("Gemideki personel için katılım/iniş, izindeki personel için izin giriş/çıkış tarihleri girilir.")
            if st.form_submit_button("💾 Kaydet") and ad_soyad:
                hata = ""
                if durum == "Gemide":
                    if katilim is None or inis is None:
                        hata = "Gemideki personel için katılım ve iniş tarihleri zorunludur."
                    else:
                        mevcut = df_from("SELECT ad_soyad FROM personnel WHERE gemi=? AND durum='Gemide'", (gemi,))
                        if not mevcut.empty:
                            hata = "⚠️ " + gemi + " gemisinde zaten " + str(mevcut.iloc[0]["ad_soyad"]) + " görevli. Önce o personeli 'İzinde' yapın."
                elif izin_giris is None or izin_cikis is None:
                    hata = "İzindeki personel için izin giriş ve çıkış tarihleri zorunludur."
                if hata:
                    st.error(hata)
                else:
                    run(
                        "INSERT INTO personnel(ad_soyad,gorev,durum,gemi,katilim,inis,izin_giris,izin_cikis,puan,notlar) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (
                            ad_soyad, gorev, durum,
                            "—" if durum == "İzinde" else gemi,
                            _tarih_iso(katilim) if durum == "Gemide" else "",
                            _tarih_iso(inis) if durum == "Gemide" else "",
                            _tarih_iso(izin_giris) if durum == "İzinde" else "",
                            _tarih_iso(izin_cikis) if durum == "İzinde" else "",
                            float(puan), notlar,
                        ),
                    )
                    st.success("✅ Personel eklendi ve kalıcı olarak saklandı.")
                    st.rerun()

    # --- Personel güncelle / sil ---
    if not p_df.empty:
        with st.expander("✏️ Personel Güncelle"):
            if "pers_guncelle_rev" not in st.session_state:
                st.session_state["pers_guncelle_rev"] = 0
            rev = st.session_state["pers_guncelle_rev"]
            secim_etiketleri = [
                str(r["id"]) + " — " + str(r["AdSoyad"]) + (" · " + str(r["Gemi"]) if r["Durum"] == "Gemide" else " · İzinde")
                for _, r in p_df.iterrows()
            ]
            secim = st.selectbox("Güncellenecek personel", secim_etiketleri, key="pers_guncelle_sec")
            secim_id = int(secim.split(" — ")[0])
            kayit = p_df[p_df["id"] == secim_id].iloc[0]
            kk = "_" + str(secim_id) + "_" + str(rev)
            try:
                mevcut_puan = int(kayit["Puan"])
            except Exception:
                mevcut_puan = 75
            with st.form("personel_guncelle_form"):
                u1, u2, u3 = st.columns(3)
                with u1:
                    u_ad = st.text_input("Ad Soyad", value=str(kayit["AdSoyad"]), key="ug_ad" + kk)
                    u_gorev = st.selectbox(
                        "Görev Tanımı", gorev_secenekleri,
                        index=gorev_secenekleri.index(kayit["Gorev"]) if kayit["Gorev"] in gorev_secenekleri else 0,
                        key="ug_gorev" + kk,
                    )
                    u_durum = st.selectbox(
                        "Durum", durum_secenekleri,
                        index=durum_secenekleri.index(kayit["Durum"]) if kayit["Durum"] in durum_secenekleri else 0,
                        key="ug_durum" + kk,
                    )
                with u2:
                    u_gemi = st.selectbox(
                        "Gemi", gemi_listesi,
                        index=gemi_listesi.index(kayit["Gemi"]) if kayit["Gemi"] in gemi_listesi else 0,
                        key="ug_gemi" + kk,
                    )
                    u_kat = st.date_input("Gemiye Katılım Tarihi", value=_iso_tarih(kayit["Katilim"]), key="ug_kat" + kk)
                    u_inis = st.date_input("İniş / Kontrat Bitiş", value=_iso_tarih(kayit["Inis"]), key="ug_inis" + kk)
                with u3:
                    u_ig = st.date_input("İzin Giriş Tarihi", value=_iso_tarih(kayit["IzinGiris"]), key="ug_ig" + kk)
                    u_ic = st.date_input("İzin Çıkış Tarihi", value=_iso_tarih(kayit["IzinCikis"]), key="ug_ic" + kk)
                    u_puan = st.number_input(
                        "Genel Değerlendirme Puanı (0-100)", min_value=0, max_value=100,
                        value=mevcut_puan, step=1, key="ug_puan" + kk,
                    )
                u_not = st.text_area(
                    "Notlar",
                    value=str(kayit["Notlar"]) if isinstance(kayit["Notlar"], str) else "",
                    key="ug_not" + kk,
                )
                st.caption("Gemideki personel için katılım/iniş, izindeki personel için izin giriş/çıkış tarihleri geçerlidir.")
                if st.form_submit_button("💾 Güncelle"):
                    hata = ""
                    if u_durum == "Gemide":
                        if u_kat is None or u_inis is None:
                            hata = "Gemideki personel için katılım ve iniş tarihleri zorunludur."
                        else:
                            mevcut = df_from(
                                "SELECT ad_soyad FROM personnel WHERE gemi=? AND durum='Gemide' AND id<>?",
                                (u_gemi, secim_id),
                            )
                            if not mevcut.empty:
                                hata = "⚠️ " + u_gemi + " gemisinde zaten " + str(mevcut.iloc[0]["ad_soyad"]) + " görevli. Önce o personeli 'İzinde' yapın."
                    elif u_ig is None or u_ic is None:
                        hata = "İzindeki personel için izin giriş ve çıkış tarihleri zorunludur."
                    if hata:
                        st.error(hata)
                    else:
                        run(
                            "UPDATE personnel SET ad_soyad=?, gorev=?, durum=?, gemi=?, katilim=?, inis=?, izin_giris=?, izin_cikis=?, puan=?, notlar=? WHERE id=?",
                            (
                                u_ad, u_gorev, u_durum,
                                "—" if u_durum == "İzinde" else u_gemi,
                                _tarih_iso(u_kat) if u_durum == "Gemide" else "",
                                _tarih_iso(u_inis) if u_durum == "Gemide" else "",
                                _tarih_iso(u_ig) if u_durum == "İzinde" else "",
                                _tarih_iso(u_ic) if u_durum == "İzinde" else "",
                                float(u_puan), u_not, secim_id,
                            ),
                        )
                        st.session_state["pers_guncelle_rev"] = rev + 1
                        st.success("✅ Personel güncellendi ve kalıcı olarak saklandı.")
                        st.rerun()

        with st.expander("🗑️ Personel Sil"):
            sil_etiketleri = [
                str(r["id"]) + " — " + str(r["AdSoyad"]) + (" · " + str(r["Gemi"]) if r["Durum"] == "Gemide" else " · İzinde")
                for _, r in p_df.iterrows()
            ]
            secim_sil = st.selectbox("Silinecek personel", sil_etiketleri, key="pers_sil_sec")
            if st.button("Sil", key="pers_sil_btn"):
                run("DELETE FROM personnel WHERE id=?", (int(secim_sil.split(" — ")[0]),))
                st.success("✅ Personel silindi.")
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


# ==================================================================
# MODÜL: ARIZALAR — filodaki tüm elektrik/elektronik arızaların merkezi takibi
# ==================================================================
elif menu == "⚠️ Arızalar":
    st.subheader("⚠️ Arızalar (Elektrik / Elektronik Arıza Takip)")

    # Dashboard'daki tıklanabilir KPI kartlarından gelen hızlı filtre ön yüklemesi
    _hz = st.session_state.pop("dz_hizli_filtre", None)
    if _hz:
        if "oncelik" in _hz:
            st.session_state["dzf_oncelik"] = list(_hz["oncelik"])
        if "durum" in _hz:
            st.session_state["dzf_durum"] = list(_hz["durum"])

    def _metin(v, varsayilan="—"):
        try:
            if pd.isna(v):
                return varsayilan
        except Exception:
            pass
        s = str(v).strip()
        return varsayilan if s in ("", "nan", "None") else s

    dz = defects_yukle()
    bugun = datetime.date.today()

    # ---------------- ÖZET KARTLARI ----------------
    toplam = len(dz)
    if toplam:
        acik = int(dz["Durum"].isin(ARIZA_ACIK_DURUMLAR).sum())
        kritik = int((dz["Oncelik"] == "Critical").sum())
        high = int((dz["Oncelik"] == "High").sum())
        yedek = int((dz["Durum"] == "Waiting Spare Part").sum())
    else:
        acik = kritik = high = yedek = 0
    st.markdown(dz_kpi_html([
        ("TOPLAM ARIZA", toplam, "v-info"),
        ("AÇIK ARIZA", acik, "v-warn"),
        ("CRITICAL", kritik, "v-crit"),
        ("HIGH", high, "v-high"),
        ("WAITING SPARE", yedek, "v-warn"),
    ]), unsafe_allow_html=True)

    # ---------------- FİLTRELEME (birbirleriyle kombine çalışır) ----------------
    dzf = dz.copy()
    with st.expander("🔍 Filtrele"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            f_gemi = st.multiselect(
                "Gemi", sorted(dz["Gemi"].astype(str).unique().tolist()) if toplam else [], key="dzf_gemi")
        with fc2:
            f_sistem = st.multiselect(
                "Sistem", sorted(dz["Sistem"].astype(str).unique().tolist()) if toplam else [], key="dzf_sistem")
        with fc3:
            f_kategori = st.multiselect(
                "Kategori", sorted(dz["Kategori"].astype(str).unique().tolist()) if toplam else [], key="dzf_kategori")
        fd1, fd2 = st.columns(2)
        with fd1:
            f_oncelik = st.multiselect("Öncelik", ARIZA_ONCELIK, key="dzf_oncelik")
        with fd2:
            f_durum = st.multiselect("Durum", ARIZA_DURUMLAR, key="dzf_durum")
        ft1, ft2 = st.columns(2)
        with ft1:
            f_bas = st.date_input("Tarih aralığı — Başlangıç", value=None, key="dzf_bas")
        with ft2:
            f_bit = st.date_input("Tarih aralığı — Bitiş", value=None, key="dzf_bit")

    if toplam:
        if f_gemi:
            dzf = dzf[dzf["Gemi"].isin(f_gemi)]
        if f_sistem:
            dzf = dzf[dzf["Sistem"].isin(f_sistem)]
        if f_kategori:
            dzf = dzf[dzf["Kategori"].isin(f_kategori)]
        if f_oncelik:
            dzf = dzf[dzf["Oncelik"].isin(f_oncelik)]
        if f_durum:
            dzf = dzf[dzf["Durum"].isin(f_durum)]
        tarih_dt = pd.to_datetime(dzf["Tarih"], errors="coerce")
        if f_bas is not None:
            maske = tarih_dt >= pd.Timestamp(f_bas)
            dzf = dzf[maske]
            tarih_dt = tarih_dt[maske]
        if f_bit is not None:
            maske = tarih_dt <= (pd.Timestamp(f_bit) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            dzf = dzf[maske]

    # ---------------- ARIZA TABLOSU ----------------
    st.caption("📋 " + str(len(dzf)) + " arıza kaydı listeleniyor")
    if dzf.empty:
        st.info("Filtrelere uyan arıza kaydı yok.")
    else:
        goster = dzf[["ID", "Gemi", "Sistem", "Ekipman", "Ariza", "Oncelik", "Durum",
                      "Tarih", "Sorumlu"]].rename(columns={"Ariza": "Arıza", "Oncelik": "Öncelik"})
        st.dataframe(goster, use_container_width=True,
                     height=min(500, 60 + 35 * len(goster)))

    # ---------------- SEÇİLİ ARIZANIN DETAYI ----------------
    if not dzf.empty:
        etiketler = [
            "#" + str(_s["ID"]) + " — " + str(_s["Gemi"]) + " · " + str(_s["Ariza"])
            for _, _s in dzf.iterrows()
        ]
        odak = st.session_state.pop("ariza_odak", None)
        idx = 0
        if odak is not None:
            for i, e in enumerate(etiketler):
                if e.startswith("#" + str(odak) + " —"):
                    idx = i
                    break
        secim = st.selectbox("🔎 Detayı görüntülenecek arıza satırı", etiketler,
                             index=idx, key="dz_detay_secim")
        did = int(secim.split(" — ")[0].replace("#", ""))
        kayit = dz[dz["ID"] == did].iloc[0]
        hist = defect_gecmis_yukle(did)
        st.markdown(ariza_detay_html(kayit, hist), unsafe_allow_html=True)

        du1, du2 = st.columns(2)
        with du1:
            with st.expander("✏️ Arıza Düzenle"):
                with st.form("ariza_guncelle_" + str(did)):
                    g1, g2, g3 = st.columns(3)
                    with g1:
                        u_durum = st.selectbox(
                            "Durum", ARIZA_DURUMLAR,
                            index=ARIZA_DURUMLAR.index(str(kayit["Durum"])) if str(kayit["Durum"]) in ARIZA_DURUMLAR else 0,
                            key="ug_durum_" + str(did))
                        u_oncelik = st.selectbox(
                            "Öncelik", ARIZA_ONCELIK,
                            index=ARIZA_ONCELIK.index(str(kayit["Oncelik"])) if str(kayit["Oncelik"]) in ARIZA_ONCELIK else 2,
                            key="ug_oncelik_" + str(did))
                        u_sorumlu = st.text_input(
                            "Sorumlu Kişi", value=_metin(kayit["Sorumlu"], ""),
                            key="ug_sorumlu_" + str(did))
                    with g2:
                        u_tahmin = st.date_input(
                            "Tahmini Kapanış Tarihi", value=_iso_tarih(kayit["TahminiKapanis"]),
                            key="ug_tahmin_" + str(did))
                        u_gercek = st.date_input(
                            "Gerçek Kapanış Tarihi", value=_iso_tarih(kayit["GercekKapanis"]),
                            key="ug_gercek_" + str(did))
                        u_is_emri = st.text_input(
                            "İş Emri No", value=_metin(kayit["IsEmri"], ""),
                            key="ug_isemri_" + str(did))
                    with g3:
                        u_downtime = st.number_input(
                            "Downtime / Duruş (saat)", min_value=0.0,
                            value=(float(kayit["Downtime"]) if pd.notna(kayit["Downtime"]) else 0.0),
                            step=0.5, key="ug_dt_" + str(did))
                        u_maliyet = st.number_input(
                            "Maliyet (USD)", min_value=0.0,
                            value=(float(kayit["Maliyet"]) if pd.notna(kayit["Maliyet"]) else 0.0),
                            step=10.0, key="ug_maliyet_" + str(did))
                        u_tekr = st.selectbox(
                            "Tekrarlayan Arıza", ["Hayır", "Evet"],
                            index=1 if str(kayit["Tekrarlayan"]) == "Evet" else 0,
                            key="ug_tekr_" + str(did))
                    u_gecici = st.text_area(
                        "Geçici Çözüm", value=_metin(kayit["GeciciCozum"], ""),
                        key="ug_gecici_" + str(did))
                    u_kalici = st.text_area(
                        "Kalıcı Çözüm", value=_metin(kayit["KaliciCozum"], ""),
                        key="ug_kalici_" + str(did))
                    u_notlar = st.text_area(
                        "Notlar", value=_metin(kayit["Notlar"], ""),
                        key="ug_notlar_" + str(did))
                    if st.form_submit_button("💾 Güncelle"):
                        gercek_str = _tarih_iso(u_gercek)
                        if u_durum in ("Closed", "Resolved") and not gercek_str:
                            gercek_str = str(bugun)
                        run(
                            """UPDATE defects SET durum=?, oncelik=?, sorumlu=?,
                               tahmini_kapanis=?, gercek_kapanis=?, is_emri=?,
                               downtime_saat=?, maliyet=?, tekrarlayan=?,
                               gecici_cozum=?, kalici_cozum=?, notlar=? WHERE id=?""",
                            (u_durum, u_oncelik, u_sorumlu.strip(),
                             _tarih_iso(u_tahmin), gercek_str, u_is_emri.strip(),
                             float(u_downtime), float(u_maliyet), u_tekr,
                             u_gecici, u_kalici, u_notlar, did),
                        )
                        if u_durum != str(kayit["Durum"]):
                            defect_gecmis_ekle(did, "Durum değişikliği", "Durum güncellendi",
                                               str(kayit["Durum"]), u_durum)
                        defect_gecmis_ekle(did, "Arıza güncellendi",
                                           "Alanlar güncellendi (düzenleme formu)")
                        st.success("✅ Arıza #" + str(did) + " güncellendi ve tarihçeye işlendi.")
                        st.rerun()
        with du2:
            with st.expander("✅ Arıza Kapat"):
                st.caption("Kapatma işlemi gerçek kapanış tarihini işler ve durum tarihçesine yazar.")
                k_tarih = st.date_input("Gerçek Kapanış Tarihi", value=bugun,
                                        key="dz_kapa_tarih_" + str(did))
                if st.button("Kapat", key="dz_kapa_btn_" + str(did)):
                    run("UPDATE defects SET durum='Closed', gercek_kapanis=? WHERE id=?",
                        (str(k_tarih), did))
                    defect_gecmis_ekle(did, "Arıza kapatıldı", "Kapatma işlemi yapıldı",
                                       str(kayit["Durum"]), "Closed")
                    st.success("✅ Arıza #" + str(did) + " kapatıldı.")
                    st.rerun()

    # ---------------- YENİ ARIZA EKLEME ----------------
    with st.expander("➕ Yeni Arıza"):
        with st.form("yeni_ariza_form"):
            n1, n2, n3 = st.columns(3)
            with n1:
                y_gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="na_gemi")
                y_sistem = st.selectbox("Sistem", ARIZA_SISTEMLER, key="na_sistem")
                y_kategori = st.selectbox("Arıza Kategorisi", ARIZA_KATEGORILER, key="na_kategori")
                y_alt = st.text_input("Alt Sistem", key="na_alt")
            with n2:
                y_ekipman = st.text_input("Ekipman", key="na_ekipman")
                y_baslik = st.text_input("Arıza Başlığı", key="na_baslik")
                y_tarih = st.date_input("Arıza Tarihi", value=bugun, key="na_tarih")
                y_bildiren = st.text_input("Arızayı Bildiren Kişi", value="ETO", key="na_bildiren")
            with n3:
                y_sorumlu = st.text_input("Sorumlu Kişi", value="ETO", key="na_sorumlu")
                y_oncelik = st.selectbox("Öncelik", ARIZA_ONCELIK, index=2, key="na_oncelik")
                y_durum = st.selectbox("Durum", ARIZA_DURUMLAR, key="na_durum")
                y_kaynak = st.selectbox("Arıza Kaynağı", ARIZA_KAYNAKLAR, key="na_kaynak")
            y_aciklama = st.text_area("Arıza Açıklaması", key="na_aciklama")
            n4, n5, n6 = st.columns(3)
            with n4:
                y_gecici = st.text_input("Geçici Çözüm", key="na_gecici")
                y_kalici = st.text_input("Kalıcı Çözüm", key="na_kalici")
            with n5:
                y_parca = st.text_input("Kullanılan Yedek Parça", key="na_parca")
                y_parca_no = st.text_input("Parça Numarası", key="na_parcano")
                y_parca_var = st.selectbox("Yedek Parça Mevcut mu?", ["Hayır", "Evet"], key="na_parcavar")
            with n6:
                y_tekr = st.selectbox("Tekrarlayan Arıza mı?", ["Hayır", "Evet"], key="na_tekr")
                y_class = st.selectbox("Class / Flag Bildirimi Gerekiyor mu?", ["Hayır", "Evet"], key="na_class")
                y_is_emri = st.text_input("İş Emri Numarası", key="na_isemri")
            n7, n8, n9 = st.columns(3)
            with n7:
                y_tahmin = st.date_input("Tahmini Kapanış Tarihi", value=None, key="na_tahmin")
            with n8:
                y_downtime = st.number_input("Downtime / Duruş Süresi (saat)",
                                             min_value=0.0, value=0.0, step=0.5, key="na_dt")
            with n9:
                y_maliyet = st.number_input("Maliyet (USD)", min_value=0.0, value=0.0,
                                            step=10.0, key="na_maliyet")
            y_notlar = st.text_area("Notlar", key="na_notlar")
            dosyalar = st.file_uploader(
                "Fotoğraf / Ek dosya (altyapı: dosya adları kayıt altına alınır)",
                accept_multiple_files=True, key="na_dosya")
            st.caption("IMO No gemi seçiminden otomatik alınır. Gerçek kapanış tarihi "
                       "gerekirse detay ekranındaki Düzenle/Kapat bölümlerinden işlenir.")
            if st.form_submit_button("💾 Kaydet"):
                if not str(y_baslik).strip():
                    st.error("⚠️ Arıza başlığı zorunludur.")
                else:
                    try:
                        imo = str(fleet_df[fleet_df["Gemi"] == y_gemi].iloc[0]["IMO"])
                    except Exception:
                        imo = ""
                    ek = ", ".join([f.name for f in (dosyalar or [])])
                    conn = get_conn()
                    cur2 = conn.cursor()
                    cur2.execute(
                        """INSERT INTO defects(gemi,imo,sistem,alt_sistem,ekipman,baslik,aciklama,
                           ariza_tarihi,bildiren,sorumlu,oncelik,durum,kategori,kaynak,
                           gecici_cozum,kalici_cozum,yedek_parcasi,parca_no,parca_mevcut,
                           tekrarlayan,class_flag,is_emri,tahmini_kapanis,gercek_kapanis,
                           downtime_saat,maliyet,ek_dosya,notlar)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (y_gemi, imo, y_sistem, y_alt, y_ekipman, y_baslik, y_aciklama,
                         str(y_tarih), y_bildiren, y_sorumlu, y_oncelik, y_durum,
                         y_kategori, y_kaynak, y_gecici, y_kalici, y_parca, y_parca_no,
                         y_parca_var, y_tekr, y_class, y_is_emri, _tarih_iso(y_tahmin), "",
                         float(y_downtime), float(y_maliyet), ek, y_notlar),
                    )
                    yeni_id = cur2.lastrowid
                    conn.commit()
                    conn.close()
                    defect_gecmis_ekle(yeni_id, "Oluşturuldu", "Arıza kaydı oluşturuldu", "", y_durum)
                    st.success("✅ Yeni arıza #" + str(yeni_id) + " kaydedildi.")
                    st.rerun()


# ==================================================================
# MODÜL: ARIZA ANALİZ & RAPORLAMA — defects verisinden otomatik analiz
# (manuel veri girişi yok; tüm rakamlar filtreli veriden hesaplanır)
# ==================================================================
elif menu == "📈 Arıza Analiz & Raporlama":
    st.subheader("📈 Arıza Analiz & Raporlama")

    dz = defects_yukle()
    bugun = datetime.date.today()

    renk_oncelik = {"Critical": "#dc2626", "High": "#f97316", "Medium": "#eab308", "Low": "#94a3b8"}
    renk_durum = {"Open": "#dc2626", "In Progress": "#1e6fd9", "Waiting Spare Part": "#f59e0b",
                  "Resolved": "#0d9488", "Closed": "#16a34a"}
    sistem_grup = {"Automation": "Automation / PLC", "PLC": "Automation / PLC",
                   "Deck Equipment": "Cargo Equipment"}
    ay_kisa = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

    # ---------------- FİLTRELER (tüm rakam ve grafikleri besler) ----------------
    f1, f2, f3, f4 = st.columns([1.3, 1.3, 1.2, 1.2])
    gemi_secenekler = ["Tüm gemiler"] + (sorted(dz["Gemi"].astype(str).unique().tolist()) if not dz.empty else [])
    sistem_secenekler = ["Tüm sistemler"] + (sorted(dz["Sistem"].astype(str).unique().tolist()) if not dz.empty else [])
    sec_gemi = f1.selectbox("Gemi", gemi_secenekler, key="ra_gemi")
    sec_sistem = f2.selectbox("Sistem", sistem_secenekler, key="ra_sistem")
    f_bas = f3.date_input("Tarih Başlangıç", value=None, key="ra_bas")
    f_bit = f4.date_input("Tarih Bitiş", value=None, key="ra_bit")

    dzf = dz.copy()
    if not dzf.empty:
        if sec_gemi != "Tüm gemiler":
            dzf = dzf[dzf["Gemi"] == sec_gemi]
        if sec_sistem != "Tüm sistemler":
            dzf = dzf[dzf["Sistem"] == sec_sistem]
        tarih_dt = pd.to_datetime(dzf["Tarih"], errors="coerce")
        if f_bas is not None:
            maske = tarih_dt >= pd.Timestamp(f_bas)
            dzf = dzf[maske]
            tarih_dt = tarih_dt[maske]
        if f_bit is not None:
            maske = tarih_dt <= (pd.Timestamp(f_bit) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            dzf = dzf[maske]

    # ---------------- 1) GENEL ÖZET ----------------
    toplam = len(dzf)
    if toplam:
        acik = int(dzf["Durum"].isin(ARIZA_ACIK_DURUMLAR).sum())
        kritik = int((dzf["Oncelik"] == "Critical").sum())
        high = int((dzf["Oncelik"] == "High").sum())
        yedek = int((dzf["Durum"] == "Waiting Spare Part").sum())
        kapanan = int(dzf["Durum"].isin(["Resolved", "Closed"]).sum())
    else:
        acik = kritik = high = yedek = kapanan = 0
    st.markdown(dz_kpi_html([
        ("TOPLAM ARIZA", toplam, "v-info"),
        ("AÇIK ARIZA", acik, "v-warn"),
        ("CRITICAL", kritik, "v-crit"),
        ("HIGH", high, "v-high"),
        ("WAITING SPARE PART", yedek, "v-warn"),
        ("ÇÖZÜLEN / KAPANAN", kapanan, "v-ok"),
    ]), unsafe_allow_html=True)

    # ---------------- 2) AYLIK ANALİZ (son 12 ay) ----------------
    pencereler = []
    for k in range(11, -1, -1):
        ay_no = bugun.month - k
        yil = bugun.year
        while ay_no <= 0:
            ay_no += 12
            yil -= 1
        pencereler.append((yil, ay_no))
    dt_f = pd.to_datetime(dzf["Tarih"], errors="coerce")
    aylik_etiket = []
    aylik_deger = []
    for yil, ay_no in pencereler:
        aylik_etiket.append(ay_kisa[ay_no - 1])
        if toplam:
            aylik_deger.append(int(((dt_f.dt.year == yil) & (dt_f.dt.month == ay_no)).sum()))
        else:
            aylik_deger.append(0)
    st.markdown('<div class="dz-section"><h4>📅 Aylık Analiz — Son 12 Ay</h4>' +
                ra_aylik_html(aylik_etiket, aylik_deger) + "</div>", unsafe_allow_html=True)

    # ---------------- 3-4) GEMİ / SİSTEM ANALİZİ ----------------
    s1, s2 = st.columns(2)
    with s1:
        gemi_satirlar = []
        if toplam:
            gemi_satirlar = [(str(g), int(v), None) for g, v in dzf["Gemi"].value_counts().items()]
        st.markdown('<div class="dz-section"><h4>🚢 Gemi Analizi (çoktan aza)</h4>' +
                    ra_bar_html(gemi_satirlar, en_fazla=15) + "</div>", unsafe_allow_html=True)
    with s2:
        sistem_satirlar = []
        if toplam:
            gruplu = dzf["Sistem"].astype(str).map(lambda s: sistem_grup.get(s, s))
            sayim = gruplu.value_counts()
            for ad in ARIZA_KATEGORILER:
                sistem_satirlar.append((ad, int(sayim.get(ad, 0)), None))
            for ad, v in sayim.items():
                if ad not in ARIZA_KATEGORILER:
                    sistem_satirlar.append((str(ad), int(v), "#94a3b8"))
        st.markdown('<div class="dz-section"><h4>⚙️ Sistem Analizi</h4>' +
                    ra_bar_html(sistem_satirlar, en_fazla=25) + "</div>", unsafe_allow_html=True)

    # ---------------- 5-6) ÖNCELİK / DURUM ANALİZİ ----------------
    s3, s4 = st.columns(2)
    with s3:
        oncelik_satirlar = []
        if toplam:
            for o in ARIZA_ONCELIK:
                oncelik_satirlar.append((o, int((dzf["Oncelik"] == o).sum()), renk_oncelik[o]))
        st.markdown('<div class="dz-section"><h4>🎯 Öncelik Analizi</h4>' +
                    ra_bar_html(oncelik_satirlar, en_fazla=4) + "</div>", unsafe_allow_html=True)
    with s4:
        durum_satirlar = []
        if toplam:
            for d in ARIZA_DURUMLAR:
                durum_satirlar.append((d, int((dzf["Durum"] == d).sum()), renk_durum[d]))
        st.markdown('<div class="dz-section"><h4>📊 Durum Analizi</h4>' +
                    ra_bar_html(durum_satirlar, en_fazla=5) + "</div>", unsafe_allow_html=True)

    # ---------------- 7) TEKRARLAYAN ARIZALAR ----------------
    st.markdown("#### 🔁 Tekrarlayan Arızalar")
    tekr_df = dzf[dzf["Tekrarlayan"] == "Evet"] if toplam else dzf.iloc[0:0]
    if tekr_df.empty:
        st.info("Filtrelere uyan tekrarlayan arıza kaydı yok.")
    else:
        goster = tekr_df[["Gemi", "Sistem", "Ekipman", "Ariza", "Tarih"]].rename(
            columns={"Ariza": "Arıza"})
        st.dataframe(goster, use_container_width=True,
                     height=min(420, 60 + 35 * len(goster)))


# ==================================================================
# MODÜL: YEDEK PARÇA & MALZEME İHTİYAÇLARI — spare_parts SQLite verisi
# (ileride Dashboard'u besleyecek ana veri kaynağı)
# ==================================================================
elif menu == "📦 Yedek Parça & Malzeme İhtiyaçları":
    st.subheader("📦 Yedek Parça & Malzeme İhtiyaçları")

    def _temiz(v, varsayilan="—"):
        try:
            if pd.isna(v):
                return varsayilan
        except Exception:
            pass
        s = str(v).strip()
        return varsayilan if s in ("", "nan", "None") else s

    sp = spare_parts_yukle()

    # ---------------- ÖZET KARTLARI ----------------
    toplam = len(sp)
    if toplam:
        kritik_o = int((sp["Oncelik"] == "Critical").sum())
        high_o = int((sp["Oncelik"] == "High").sum())
        siparis_bekleyen = int(sp["Durum"].isin(["İhtiyaç", "Talep Edildi"]).sum())
        teslim_bekleyen = int(sp["Durum"].isin(["Sipariş Verildi", "Kısmi Geldi", "Beklemede"]).sum())
        kritik_parca = int((sp["Kritik"] == "Evet").sum())
    else:
        kritik_o = high_o = siparis_bekleyen = teslim_bekleyen = kritik_parca = 0
    st.markdown(dz_kpi_html([
        ("TOPLAM MALZEME İHTİYACI", toplam, "v-info"),
        ("CRITICAL", kritik_o, "v-crit"),
        ("HIGH", high_o, "v-high"),
        ("SİPARİŞ BEKLEYEN", siparis_bekleyen, "v-warn"),
        ("TESLİM BEKLEYEN", teslim_bekleyen, "v-warn"),
        ("KRİTİK YEDEK PARÇA", kritik_parca, "v-crit"),
    ]), unsafe_allow_html=True)

    # ---------------- FİLTRELER (birlikte çalışır) ----------------
    spf = sp.copy()
    with st.expander("🔍 Filtrele"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            f_gemi = st.multiselect(
                "Gemi", sorted(sp["Gemi"].astype(str).unique().tolist()) if toplam else [], key="spf_gemi")
        with fc2:
            f_sistem = st.multiselect(
                "Sistem", sorted(sp["Sistem"].astype(str).unique().tolist()) if toplam else [], key="spf_sistem")
        with fc3:
            f_oncelik = st.multiselect("Öncelik", ARIZA_ONCELIK, key="spf_oncelik")
        fd1, fd2 = st.columns(2)
        with fd1:
            f_durum = st.multiselect("Durum", SPAR_DURUMLAR, key="spf_durum")
        with fd2:
            f_kritik = st.checkbox("Sadece kritik yedek parçalar", key="spf_kritik")
        ft1, ft2 = st.columns(2)
        with ft1:
            f_bas = st.date_input("Tarih Başlangıç", value=None, key="spf_bas")
        with ft2:
            f_bit = st.date_input("Tarih Bitiş", value=None, key="spf_bit")

    if toplam:
        if f_gemi:
            spf = spf[spf["Gemi"].isin(f_gemi)]
        if f_sistem:
            spf = spf[spf["Sistem"].isin(f_sistem)]
        if f_oncelik:
            spf = spf[spf["Oncelik"].isin(f_oncelik)]
        if f_durum:
            spf = spf[spf["Durum"].isin(f_durum)]
        if f_kritik:
            spf = spf[spf["Kritik"] == "Evet"]
        tarih_dt = pd.to_datetime(spf["IhtiyacTarihi"], errors="coerce")
        if f_bas is not None:
            maske = tarih_dt >= pd.Timestamp(f_bas)
            spf = spf[maske]
            tarih_dt = tarih_dt[maske]
        if f_bit is not None:
            maske = tarih_dt <= (pd.Timestamp(f_bit) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            spf = spf[maske]

    # ---------------- ANA TABLO ----------------
    st.caption("📋 " + str(len(spf)) + " malzeme/ihtiyaç kaydı listeleniyor")
    if spf.empty:
        st.info("Filtrelere uyan kayıt yok.")
    else:
        goster = spf[["ID", "Gemi", "Sistem", "Ekipman", "Malzeme", "ParcaNo",
                      "Ihtiyac", "Oncelik", "Durum", "IhtiyacTarihi"]].rename(columns={
            "ParcaNo": "Parça No", "Ihtiyac": "Miktar", "Oncelik": "Öncelik",
            "IhtiyacTarihi": "İhtiyaç Tarihi"})
        st.dataframe(goster, use_container_width=True,
                     height=min(500, 60 + 35 * len(goster)))

    # ---------------- SEÇİLİ KAYDIN DETAYI ----------------
    if not spf.empty:
        etiketler = [
            "#" + str(r["ID"]) + " — " + str(r["Gemi"]) + " · " + str(r["Malzeme"])
            for _, r in spf.iterrows()
        ]
        secim = st.selectbox("🔎 Detayı görüntülenecek kayıt", etiketler, key="sp_detay_secim")
        sid = int(secim.split(" — ")[0].replace("#", ""))
        kayit = sp[sp["ID"] == sid].iloc[0]
        st.markdown(sp_detay_html(kayit), unsafe_allow_html=True)

        du1, du2 = st.columns(2)
        with du1:
            with st.expander("✏️ Düzenle"):
                with st.form("sp_guncelle_" + str(sid)):
                    g1, g2, g3 = st.columns(3)
                    with g1:
                        u_durum = st.selectbox(
                            "Durum", SPAR_DURUMLAR,
                            index=SPAR_DURUMLAR.index(str(kayit["Durum"])) if str(kayit["Durum"]) in SPAR_DURUMLAR else 0,
                            key="su_durum_" + str(sid))
                        u_oncelik = st.selectbox(
                            "Öncelik", ARIZA_ONCELIK,
                            index=ARIZA_ONCELIK.index(str(kayit["Oncelik"])) if str(kayit["Oncelik"]) in ARIZA_ONCELIK else 2,
                            key="su_oncelik_" + str(sid))
                        u_kritik = st.selectbox(
                            "Kritik Yedek Parça", ["Hayır", "Evet"],
                            index=1 if str(kayit["Kritik"]) == "Evet" else 0,
                            key="su_kritik_" + str(sid))
                    with g2:
                        u_iht = st.number_input(
                            "İhtiyaç Miktarı", min_value=0,
                            value=(int(kayit["Ihtiyac"]) if pd.notna(kayit["Ihtiyac"]) else 0),
                            key="su_iht_" + str(sid))
                        u_stok = st.number_input(
                            "Mevcut Stok", min_value=0,
                            value=(int(kayit["Stok"]) if pd.notna(kayit["Stok"]) else 0),
                            key="su_stok_" + str(sid))
                        u_sip = st.number_input(
                            "Sipariş Miktarı", min_value=0,
                            value=(int(kayit["Siparis"]) if pd.notna(kayit["Siparis"]) else 0),
                            key="su_sip_" + str(sid))
                    with g3:
                        u_talep = st.date_input("Talep Tarihi", value=_iso_tarih(kayit["TalepTarihi"]),
                                                key="su_talep_" + str(sid))
                        u_iht_t = st.date_input("İhtiyaç Tarihi", value=_iso_tarih(kayit["IhtiyacTarihi"]),
                                                key="su_ihtt_" + str(sid))
                        u_teslim = st.date_input("Tahmini Teslim Tarihi", value=_iso_tarih(kayit["TeslimTarihi"]),
                                                 key="su_teslim_" + str(sid))
                    r1, r2, r3 = st.columns(3)
                    with r1:
                        u_tedarikci = st.text_input("Tedarikçi", value=_temiz(kayit["Tedarikci"], ""),
                                                    key="su_ted_" + str(sid))
                        u_siparis_no = st.text_input("Sipariş No", value=_temiz(kayit["SiparisNo"], ""),
                                                     key="su_pono_" + str(sid))
                    with r2:
                        u_parca = st.text_input("Parça No", value=_temiz(kayit["ParcaNo"], ""),
                                                key="su_parca_" + str(sid))
                        u_marka = st.text_input("Marka / Model", value=_temiz(kayit["Marka"], ""),
                                                key="su_marka_" + str(sid))
                    with r3:
                        u_iliskili = st.selectbox(
                            "Arıza ile İlişkili", ["Hayır", "Evet"],
                            index=1 if str(kayit["ArizaIliskili"]) == "Evet" else 0,
                            key="su_iliski_" + str(sid))
                        u_ilgili = st.number_input(
                            "İlgili Arıza ID", min_value=0,
                            value=(int(kayit["IlgiliAriza"]) if pd.notna(kayit["IlgiliAriza"]) else 0),
                            key="su_arizaid_" + str(sid))
                    u_notlar = st.text_area("Notlar", value=_temiz(kayit["Notlar"], ""),
                                            key="su_not_" + str(sid))
                    if st.form_submit_button("💾 Güncelle"):
                        run(
                            """UPDATE spare_parts SET durum=?, oncelik=?, ihtiyac_miktar=?, mevcut_stok=?,
                               siparis_miktar=?, talep_tarihi=?, ihtiyac_tarihi=?, tahmini_teslim=?,
                               tedarikci=?, siparis_no=?, parca_no=?, marka_model=?,
                               kritik_parca=?, ariza_iliskili=?, ilgili_ariza_id=?, notlar=? WHERE id=?""",
                            (u_durum, u_oncelik, int(u_iht), int(u_stok), int(u_sip),
                             _tarih_iso(u_talep), _tarih_iso(u_iht_t), _tarih_iso(u_teslim),
                             u_tedarikci.strip(), u_siparis_no.strip(), u_parca.strip(),
                             u_marka.strip(), u_kritik, u_iliskili, int(u_ilgili),
                             u_notlar, sid),
                        )
                        st.success("✅ Kayıt #" + str(sid) + " güncellendi.")
                        st.rerun()
        with du2:
            with st.expander("✅ Kapat"):
                st.caption("Kapatma: kayıt 'Geldi' (teslim alındı) veya 'İptal' olarak işaretlenir.")
                k_kapanis = st.selectbox("Kapanış Durumu", ["Geldi", "İptal"],
                                         key="sp_kapa_durum_" + str(sid))
                if st.button("Kapat", key="sp_kapa_btn_" + str(sid)):
                    run("UPDATE spare_parts SET durum=? WHERE id=?", (k_kapanis, sid))
                    st.success("✅ Kayıt #" + str(sid) + " '" + k_kapanis + "' olarak kapatıldı.")
                    st.rerun()

    # ---------------- YENİ MALZEME İHTİYACI ----------------
    with st.expander("➕ Yeni Malzeme İhtiyacı"):
        with st.form("yeni_spare_form"):
            n1, n2, n3 = st.columns(3)
            with n1:
                y_gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="nsp_gemi")
                y_sistem = st.selectbox("Sistem", ARIZA_SISTEMLER, key="nsp_sistem")
                y_ekipman = st.text_input("Ekipman", key="nsp_ekipman")
                y_malzeme = st.text_input("Malzeme / Yedek Parça", key="nsp_malzeme")
            with n2:
                y_parca = st.text_input("Parça No", key="nsp_parca")
                y_marka = st.text_input("Marka / Model", key="nsp_marka")
                y_birim = st.selectbox("Birim", ["adet", "metre", "paket", "lt"], key="nsp_birim")
                y_oncelik = st.selectbox("Öncelik", ARIZA_ONCELIK, index=2, key="nsp_oncelik")
            with n3:
                y_durum = st.selectbox("Durum", SPAR_DURUMLAR, key="nsp_durum")
                y_talep = st.date_input("Talep Tarihi", value=datetime.date.today(), key="nsp_talep")
                y_iht_t = st.date_input("İhtiyaç Tarihi", value=None, key="nsp_iht")
                y_teslim = st.date_input("Tahmini Teslim Tarihi", value=None, key="nsp_teslim")
            m1, m2, m3 = st.columns(3)
            with m1:
                y_iht = st.number_input("İhtiyaç Miktarı", min_value=0, value=1, step=1, key="nsp_ihtiac")
                y_stok = st.number_input("Mevcut Stok", min_value=0, value=0, step=1, key="nsp_stok")
            with m2:
                y_sip = st.number_input("Sipariş Miktarı", min_value=0, value=0, step=1, key="nsp_siparis")
                y_tedarikci = st.text_input("Tedarikçi", key="nsp_tedarikci")
            with m3:
                y_pono = st.text_input("Sipariş No", key="nsp_pono")
                y_kritik = st.selectbox("Kritik Yedek Parça", ["Hayır", "Evet"], key="nsp_kritik")
            k1, k2 = st.columns(2)
            with k1:
                y_iliskili = st.selectbox("Arıza ile İlişkili", ["Hayır", "Evet"], key="nsp_iliski")
            with k2:
                y_ilgili = st.number_input("İlgili Arıza ID (0 = yok)", min_value=0, value=0,
                                           key="nsp_arizaid")
            y_notlar = st.text_area("Notlar", key="nsp_notlar")
            st.caption("IMO No gemi seçiminden otomatik alınır. İlgili Arıza ID, varsa Arızalar "
                       "modülündeki kayıt numarası olabilir.")
            if st.form_submit_button("💾 Kaydet"):
                if not str(y_malzeme).strip():
                    st.error("⚠️ Malzeme / Yedek Parça adı zorunludur.")
                else:
                    try:
                        imo = str(fleet_df[fleet_df["Gemi"] == y_gemi].iloc[0]["IMO"])
                    except Exception:
                        imo = ""
                    sql_yeni = ("INSERT INTO spare_parts(gemi,imo,sistem,ekipman,malzeme,parca_no,marka_model,"
                                "ihtiyac_miktar,mevcut_stok,siparis_miktar,birim,oncelik,durum,"
                                "talep_tarihi,ihtiyac_tarihi,tedarikci,siparis_no,tahmini_teslim,"
                                "kritik_parca,ariza_iliskili,ilgili_ariza_id,notlar) VALUES ("
                                + ",".join(["?"] * 22) + ")")
                    run(sql_yeni, (
                        y_gemi, imo, y_sistem, y_ekipman.strip(), y_malzeme.strip(),
                        y_parca.strip(), y_marka.strip(), int(y_iht), int(y_stok),
                        int(y_sip), y_birim, y_oncelik, y_durum,
                        _tarih_iso(y_talep), _tarih_iso(y_iht_t), y_tedarikci.strip(),
                        y_pono.strip(), _tarih_iso(y_teslim), y_kritik, y_iliskili,
                        int(y_ilgili), y_notlar,
                    ))
                    st.success("✅ Yeni malzeme ihtiyacı kaydedildi.")
                    st.rerun()
