import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="TTS Ships Panel", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.main-header{background:linear-gradient(90deg,#0b3d91 0%,#1e6fd9 100%);padding:20px;border-radius:10px;color:white;margin-bottom:20px}
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
.fault-badge{font-size:10.5px;padding:2px 8px;border-radius:10px;background:#0b3d91;color:#fff;font-weight:600;white-space:nowrap}
.inspect-item{padding:10px 12px;border-radius:8px;margin-bottom:8px;background:#f8fafc;border-left:4px solid #1e6fd9;font-size:12.5px}
.inspect-date{font-size:10.5px;color:#7a8699;margin-bottom:3px}
.inspect-title{font-weight:700;color:#0b3d91;margin-bottom:4px}
.inspect-desc{color:#333;line-height:1.5}
.mat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;border-bottom:1px solid #eef2f7;font-size:12.5px}
.mat-row:last-child{border-bottom:none}
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

if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "megger_records" not in st.session_state:
    st.session_state.megger_records = []

fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Container", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", "Giris": "2025-06-15", "KontratBitis": "2026-06-15"},
    {"Gemi": "M/T MOON STAR", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberia", "Yıl": "2013", "LOA": "183 m", "Durum": "🟢 Uygun", "ETO": "Mehmet DEMİR", "Giris": "2025-11-02", "KontratBitis": "2026-08-02"},
    {"Gemi": "M/T KUZEY STAR II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟢 Uygun", "ETO": "Ali KAYA", "Giris": "2026-01-20", "KontratBitis": "2027-01-20"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Cargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberia", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Hasan ÇELİK", "Giris": "2025-09-05", "KontratBitis": "2026-03-05"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Cargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberia", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", "Giris": "2025-12-01", "KontratBitis": "2026-09-01"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Bulk Carrier", "DWT": "6005", "GRT": "4949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Serkan AYDIN", "Giris": "2025-07-12", "KontratBitis": "2026-07-12"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Bulk Carrier", "DWT": "6059", "GRT": "4949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Burak ÖZTÜRK", "Giris": "2025-08-20", "KontratBitis": "2026-05-20"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Bulk Carrier", "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberia", "Yıl": "2011", "LOA": "225 m", "Durum": "🟢 Uygun", "ETO": "Kemal ARSLAN", "Giris": "2026-02-10", "KontratBitis": "2027-02-10"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Bulk Carrier", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberia", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Onur YILDIZ", "Giris": "2025-10-01", "KontratBitis": "2026-04-01"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Bulk Carrier", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,89 m", "Durum": "🟢 Uygun", "ETO": "Volkan KOÇ", "Giris": "2025-05-18", "KontratBitis": "2026-05-18"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Bulk Carrier", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberia", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Cem POLAT", "Giris": "2026-03-01", "KontratBitis": "2027-03-01"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Bulk Carrier", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Barış TAŞ", "Giris": "2025-12-15", "KontratBitis": "2026-06-15"},
    {"Gemi": "M/V DENIZ STAR", "IMO": "1071472", "Tip": "General Cargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberia", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Tolga ERDOĞAN", "Giris": "2026-01-05", "KontratBitis": "2026-10-05"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "General Cargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberia", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Yusuf KURT", "Giris": "2026-02-20", "KontratBitis": "2026-11-20"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Live Stock", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟢 Uygun", "ETO": "Murat AVCİ", "Giris": "2025-04-10", "KontratBitis": "2026-04-10"},
]
fleet_df = pd.DataFrame(fleet_data)

arizalar = [
    {"Gemi": "M/V BOSPHORUS", "Ekipman": "Ana Jeneratör No:2 - Alternatör", "Aciliyet": "Yüksek", "Tespit": "2026-09-18", "Aciklama": "Sargı izolasyon direnci düşük (0.6 MOhm), megger testi tekrar edilecek."},
    {"Gemi": "M/V MED STAR", "Ekipman": "Bow Thruster Kumanda Panosu", "Aciliyet": "Orta", "Tespit": "2026-09-15", "Aciklama": "Kumanda kartı arızalı, yedek kart bekleniyor."},
    {"Gemi": "M/T MOON STAR", "Ekipman": "Acil Aydınlatma Devresi", "Aciliyet": "Yüksek", "Tespit": "2026-09-20", "Aciklama": "Köprüüstü acil aydınlatma devresinde toprak kaçağı tespit edildi."},
    {"Gemi": "M/V A380", "Ekipman": "Soğutma Kompresörü Motoru", "Aciliyet": "Düşük", "Tespit": "2026-09-10", "Aciklama": "Rulman sesi artmış, izleme listesinde."},
    {"Gemi": "M/V ATLANTIC STAR", "Ekipman": "MSB Bus-Bar Bağlantısı", "Aciliyet": "Yüksek", "Tespit": "2026-09-12", "Aciklama": "Termal kamera ile sıcak nokta tespit edildi (85 C)."},
    {"Gemi": "M/V SAPHIRA", "Ekipman": "Yangın Alarm Panosu", "Aciliyet": "Orta", "Tespit": "2026-09-08", "Aciklama": "Zone 3 dedektörü arızalı, değişim gerekiyor."},
]

denetlemeler = [
    {"Tarih": "2026-09-20", "Gemi": "M/T MOON STAR", "Baslik": "Aylık Elektrik Denetimi", "Aciklama": "Ana şalter panosu, acil jeneratör ve MSB kontrol edildi. Acil aydınlatma devresinde toprak kaçağı bulundu. Aksiyon açıldı.", "Denetci": "Ahmet YILMAZ"},
    {"Tarih": "2026-09-18", "Gemi": "M/V BOSPHORUS", "Baslik": "Yıllık Class Survey", "Aciklama": "Alternatör No:2 izolasyon testleri tamamlandı. Class surveyör raporu bekleniyor.", "Denetci": "Mehmet DEMİR"},
    {"Tarih": "2026-09-15", "Gemi": "M/V MED STAR", "Baslik": "PSC Öncesi Öz Denetim", "Aciklama": "Steering gear, emergency generator ve yangın pompası elektrik devreleri kontrol edildi. Bow thruster kumanda kartı arızası tespit edildi.", "Denetci": "Ali KAYA"},
    {"Tarih": "2026-09-12", "Gemi": "M/V ATLANTIC STAR", "Baslik": "Termal Kamera Taraması", "Aciklama": "MSB ve MCC panolarında termal tarama yapıldı. Bus-bar bağlantısında sıcak nokta tespit edildi.", "Denetci": "Kemal ARSLAN"},
    {"Tarih": "2026-09-08", "Gemi": "M/V SAPHIRA", "Baslik": "Yangın Alarm Testi", "Aciklama": "Tüm zone dedektörleri test edildi. Zone 3 dedektörü cevap vermedi.", "Denetci": "Murat AVCİ"},
    {"Tarih": "2026-09-05", "Gemi": "M/V A380", "Baslik": "Rutin Elektrik Kontrolü", "Aciklama": "Aydınlatma, jeneratör ve ana pano kontrol edildi. Soğutma kompresörü rulman sesi not edildi.", "Denetci": "Hasan ÇELİK"},
]

malzeme_ihtiyac = [
    {"Malzeme": "Bow Thruster Kumanda Kartı", "Gemi": "M/V MED STAR", "Miktar": 1, "Oncelik": "Acil", "Tedarikci": "Kongsberg", "Talep": "2026-09-16"},
    {"Malzeme": "Termal Kamera Kartuşu", "Gemi": "M/V ATLANTIC STAR", "Miktar": 1, "Oncelik": "Yüksek", "Tedarikci": "FLIR", "Talep": "2026-09-14"},
    {"Malzeme": "Yangın Dedektörü (Zone 3)", "Gemi": "M/V SAPHIRA", "Miktar": 2, "Oncelik": "Normal", "Tedarikci": "Consilium", "Talep": "2026-09-10"},
    {"Malzeme": "İzolasyon Bandı (Yüksek Sıcaklık)", "Gemi": "Tüm Filo", "Miktar": 20, "Oncelik": "Normal", "Tedarikci": "3M", "Talep": "2026-09-09"},
    {"Malzeme": "Acil Aydınlatma Balastı", "Gemi": "M/T MOON STAR", "Miktar": 4, "Oncelik": "Acil", "Tedarikci": "Philips", "Talep": "2026-09-20"},
    {"Malzeme": "Rulman (Kompresör Motoru)", "Gemi": "M/V A380", "Miktar": 2, "Oncelik": "Yüksek", "Tedarikci": "SKF", "Talep": "2026-09-11"},
    {"Malzeme": "Sigorta Seti (MSB Yedek)", "Gemi": "M/V MED STAR", "Miktar": 1, "Oncelik": "Normal", "Tedarikci": "ABB", "Talep": "2026-09-07"},
    {"Malzeme": "Kontaktör (3TF52)", "Gemi": "M/V CHIEF SEATTLE", "Miktar": 3, "Oncelik": "Yüksek", "Tedarikci": "Siemens", "Talep": "2026-09-13"},
]


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
    if "Arıza" in row["Durum"] or "Süresi" in row["Durum"]:
        cls = "err"
    elif "Bakım" in row["Durum"] or "Yakında" in row["Durum"]:
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


def render_ariza():
    st.markdown('<div class="panel-card"><div class="panel-title">🔧 Gemilerde Bulunan Toplam Arızalar</div>', unsafe_allow_html=True)
    y = sum(1 for a in arizalar if a["Aciliyet"] == "Yüksek")
    o = sum(1 for a in arizalar if a["Aciliyet"] == "Orta")
    d = sum(1 for a in arizalar if a["Aciliyet"] == "Düşük")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam", len(arizalar))
    m2.metric("🔴 Yüksek", y)
    m3.metric("🟡 Orta", o)
    m4.metric("🟢 Düşük", d)
    st.markdown("---")
    for a in arizalar:
        cls = "high" if a["Aciliyet"] == "Yüksek" else ("mid" if a["Aciliyet"] == "Orta" else "low")
        line = '<div class="fault-item ' + cls + '">'
        line += '<div><b>' + a["Gemi"] + '</b> · ' + a["Ekipman"]
        line += '<div style="font-size:11px;color:#5a6b82;margin-top:3px;">' + a["Aciklama"] + '</div>'
        line += '<div style="font-size:10px;color:#7a8699;margin-top:3px;">Tespit: ' + a["Tespit"] + '</div></div>'
        line += '<span class="fault-badge">' + a["Aciliyet"] + '</span></div>'
        st.markdown(line, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_denetleme():
    st.markdown('<div class="panel-card"><div class="panel-title">📋 En Son Yapılan Denetlemeler ve Tespitler</div>', unsafe_allow_html=True)
    for d in denetlemeler:
        line = '<div class="inspect-item">'
        line += '<div class="inspect-date">📅 ' + d["Tarih"] + ' · Denetçi: ' + d["Denetci"] + '</div>'
        line += '<div class="inspect-title">🚢 ' + d["Gemi"] + ' — ' + d["Baslik"] + '</div>'
        line += '<div class="inspect-desc">' + d["Aciklama"] + '</div></div>'
        st.markdown(line, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_malzeme():
    st.markdown('<div class="panel-card"><div class="panel-title">📦 Malzeme İhtiyaç Listesi</div>', unsafe_allow_html=True)
    a = sum(1 for m in malzeme_ihtiyac if m["Oncelik"] == "Acil")
    y = sum(1 for m in malzeme_ihtiyac if m["Oncelik"] == "Yüksek")
    n = sum(1 for m in malzeme_ihtiyac if m["Oncelik"] == "Normal")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam", len(malzeme_ihtiyac))
    m2.metric("🔴 Acil", a)
    m3.metric("🟡 Yüksek", y)
    m4.metric("🟢 Normal", n)
    st.markdown("---")
    for m in malzeme_ihtiyac:
        cls = m["Oncelik"].lower().replace("ü", "u")
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
st.sidebar.caption("© 2026 TTS Ships · v3.5")

if menu == "🏠 Dashboard":
    st.subheader("📊 Filo Genel Durum")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Gemi", len(fleet_df))
    c2.metric("Uygun", (fleet_df["Durum"] == "🟢 Uygun").sum())
    c3.metric("Bakım", (fleet_df["Durum"] == "🟡 Bakım").sum())
    c4.metric("Arıza", (fleet_df["Durum"] == "🔴 Arıza").sum())
    st.markdown("---")
    rows = fleet_df.to_dict("records")
    for i in range(0, len(rows), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(rows):
                with col:
                    st.markdown(ship_card_html(rows[i + j]), unsafe_allow_html=True)
    st.markdown("---")
    ca, cb = st.columns([1, 1])
    with ca:
        render_ariza()
    with cb:
        render_malzeme()
    st.markdown("---")
    render_denetleme()

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
        {"Gemi": "M/V VENUS STAR", "Sertifika": "Safety Equipment", "Bitis": str(t + datetime.timedelta(days=200)), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/V MERCUR STAR", "Sertifika": "Load Line", "Bitis": str(t + datetime.timedelta(days=12)), "Durum": "🟡 Yakında"},
        {"Gemi": "M/V SAPHIRA", "Sertifika": "IOPP", "Bitis": str(t + datetime.timedelta(days=320)), "Durum": "🟢 Geçerli"},
    ]
    cert_df = pd.DataFrame(cd)
    k1, k2, k3 = st.columns(3)
    k1.metric("Toplam", len(cert_df))
    k2.metric("Kritik", ((cert_df["Durum"] == "🔴 Kritik") |
