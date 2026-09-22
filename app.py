import streamlit as st
import pandas as pd
import datetime
import io
from fpdf import FPDF

# ---------- Sayfa Yapılandırması ----------
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CSS ----------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0b3d91 0%, #1e6fd9 100%);
        padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;
    }
    .main-header h1 { margin: 0; font-size: 26px; }
    .main-header p { margin: 5px 0 0 0; opacity: 0.9; font-size: 14px; }

    .ship-card {
        background: #ffffff;
        border: 1px solid #e3e8ef;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 15px;
        height: 100%;
    }
    .ship-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(30,111,217,0.25);
    }
    .card-flex {
        display: flex;
        gap: 14px;
        align-items: flex-start;
    }
    .eto-left {
        flex: 0 0 130px;
        text-align: center;
    }
    .eto-photo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #1e6fd9;
        box-shadow: 0 2px 8px rgba(30,111,217,0.3);
    }
    .eto-placeholder {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1e6fd9 0%, #0b3d91 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        font-weight: 700;
        margin: 0 auto;
        border: 3px solid #0b3d91;
    }
    .eto-name {
        font-size: 11.5px;
        font-weight: 700;
        color: #0b3d91;
        margin-top: 8px;
        line-height: 1.3;
    }
    .eto-role {
        font-size: 10px;
        color: #7a8699;
        margin-top: 2px;
    }
    .contract-box {
        margin-top: 8px;
        font-size: 10.5px;
    }
    .contract-dates {
        display: flex;
        justify-content: space-between;
        color: #5a6b82;
        font-size: 10px;
        margin-bottom: 4px;
    }
    .progress-track {
        background: #e6ecf5;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        position: relative;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
        transition: width 0.4s ease;
    }
    .progress-fill.warn { background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%); }
    .progress-fill.err  { background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%); }
    .contract-remaining {
        text-align: center;
        font-size: 10.5px;
        margin-top: 5px;
        font-weight: 600;
        color: #16a34a;
    }
    .contract-remaining.warn { color: #d97706; }
    .contract-remaining.err  { color: #b91c1c; }

    .ship-right { flex: 1; min-width: 0; }
    .ship-name {
        font-weight: 700;
        font-size: 15px;
        color: #0b3d91;
        margin-bottom: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ship-imo {
        font-size: 11px;
        color: #7a8699;
        margin-bottom: 8px;
    }
    .ship-info {
        font-size: 11.5px;
        color: #333;
        line-height: 1.55;
    }
    .ship-info b { color: #0b3d91; }
    .ship-status {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 10px;
        font-size: 10px;
        font-weight: 600;
        background: #e6f4ea;
        color: #1e7e34;
        margin-top: 8px;
    }
    .ship-status.warn { background: #fff4e0; color: #b76e00; }
    .ship-status.err  { background: #fdecea; color: #c0392b; }
</style>
""", unsafe_allow_html=True)

# ---------- Başlık ----------
st.markdown("""
<div class="main-header">
    <h1>⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Filo Yönetim Paneli</h1>
    <p>MarineTraffic entegrasyonu · Sertifika/Survey takibi · Satınalma · Teknik doküman kütüphanesi ·
    ETO eğitim/PSC simülasyonu · Megger kayıtları · PDF/Excel raporlama</p>
</div>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "megger_records" not in st.session_state:
    st.session_state.megger_records = []

# ---------- Filo Verileri (ETO + Kontrat bilgileri dahil) ----------
tts_fleet_data = [
    {"Gemi": "M/V MED STAR",      "IMO": "9337028", "Tip": "Container",     "DWT": "27254",    "GRT": "23633", "Bayrak": "Panama",          "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun",
     "ETO": "Ahmet YILMAZ",     "Giris": "2025-06-15", "KontratBitis": "2026-06-15"},
    {"Gemi": "M/T MOON STAR",     "IMO": "9667928", "Tip": "Tanker",        "DWT": "49997",    "GRT": "29940", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "183 m",    "Durum": "🟢 Uygun",
     "ETO": "Mehmet DEMİR",     "Giris": "2025-11-02", "KontratBitis": "2026-08-02"},
    {"Gemi": "M/T KUZEY STAR II", "IMO": "9499175", "Tip": "Tanker",        "DWT": "6107",     "GRT": "4081",  "Bayrak": "Malta",           "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟢 Uygun",
     "ETO": "Ali KAYA",         "Giris": "2026-01-20", "KontratBitis": "2027-01-20"},
    {"Gemi": "M/V A380",          "IMO": "9310915", "Tip": "Ro-Ro Cargo",   "DWT": "1300",     "GRT": "1285",  "Bayrak": "Liberia",         "Yıl": "2003", "LOA": "75 m",     "Durum": "🟢 Uygun",
     "ETO": "Hasan ÇELİK",      "Giris": "2025-09-05", "KontratBitis": "2026-03-05"},
    {"Gemi": "M/V AKBABA",        "IMO": "9319478", "Tip": "Ro-Ro Cargo",   "DWT": "1300",     "GRT": "1281",  "Bayrak": "Liberia",         "Yıl": "2004", "LOA": "75 m",     "Durum": "🟢 Uygun",
     "ETO": "Emre ŞAHİN",       "Giris": "2025-12-01", "KontratBitis": "2026-09-01"},
    {"Gemi": "M/V ALEXANDRA I",   "IMO": "8876340", "Tip": "Bulk Carrier",  "DWT": "6005",     "GRT": "4949",  "Bayrak": "Panama",          "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun",
     "ETO": "Serkan AYDIN",     "Giris": "2025-07-12", "KontratBitis": "2026-07-12"},
    {"Gemi": "M/V ALENA",         "IMO": "8857772", "Tip": "Bulk Carrier",  "DWT": "6059",     "GRT": "4949",  "Bayrak": "Panama",          "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun",
     "ETO": "Burak ÖZTÜRK",     "Giris": "2025-08-20", "KontratBitis": "2026-05-20"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Bulk Carrier",  "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberia",         "Yıl": "2011", "LOA": "225 m",    "Durum": "🟢 Uygun",
     "ETO": "Kemal ARSLAN",     "Giris": "2026-02-10", "KontratBitis": "2027-02-10"},
    {"Gemi": "M/V PACIFIC STAR",  "IMO": "9470387", "Tip": "Bulk Carrier",  "DWT": "78128",    "GRT": "41718", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun",
     "ETO": "Onur YILDIZ",      "Giris": "2025-10-01", "KontratBitis": "2026-04-01"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Bulk Carrier",  "DWT": "52428",    "GRT": "30174", "Bayrak": "Panama",          "Yıl": "2001", "LOA": "189,89 m", "Durum": "🟢 Uygun",
     "ETO": "Volkan KOÇ",       "Giris": "2025-05-18", "KontratBitis": "2026-05-18"},
    {"Gemi": "M/V VENUS STAR",    "IMO": "9609134", "Tip": "Bulk Carrier",  "DWT": "80888",    "GRT": "44025", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "229 m",    "Durum": "🟢 Uygun",
     "ETO": "Cem POLAT",        "Giris": "2026-03-01", "KontratBitis": "2027-03-01"},
    {"Gemi": "M/V MERCUR STAR",   "IMO": "9609287", "Tip": "Bulk Carrier",  "DWT": "79520",    "GRT": "43501", "Bayrak": "Malta",           "Yıl": "2015", "LOA": "229 m",    "Durum": "🟢 Uygun",
     "ETO": "Barış TAŞ",        "Giris": "2025-12-15", "KontratBitis": "2026-06-15"},
    {"Gemi": "M/V DENIZ STAR",    "IMO": "1071472", "Tip": "General Cargo", "DWT": "8300",     "GRT": "6641",  "Bayrak": "Liberia",         "Yıl": "2025", "LOA": "142 m",    "Durum": "🟢 Uygun",
     "ETO": "Tolga ERDOĞAN",    "Giris": "2026-01-05", "KontratBitis": "2026-10-05"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "General Cargo", "DWT": "8330",     "GRT": "6732",  "Bayrak": "Liberia",         "Yıl": "2025", "LOA": "142 m",    "Durum": "🟢 Uygun",
     "ETO": "Yusuf KURT",       "Giris": "2026-02-20", "KontratBitis": "2026-11-20"},
    {"Gemi": "M/V SAPHIRA",       "IMO": "7924425", "Tip": "Live Stock",    "DWT": "12900",    "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟢 Uygun",
     "ETO": "Murat AVCİ",       "Giris": "2025-04-10", "KontratBitis": "2026-04-10"},
]
fleet_df = pd.DataFrame(tts_fleet_data)

# ---------- Yardımcı Fonksiyonlar ----------
def durum_class(durum: str) -> str:
    if "Arıza" in durum or "Süresi" in durum:
        return "err"
    if "Bakım" in durum or "Yakında" in durum:
        return "warn"
    return ""

def kontrat_bilgi(giris_str: str, bitis_str: str):
    """(toplam_gün, geçen_gün, kalan_gün, yüzde, durum_class) döner."""
    try:
        giris = datetime.date.fromisoformat(giris_str)
        bitis = datetime.date.fromisoformat(bitis_str)
    except Exception:
        return 0, 0, 0, 0, ""

    bugun = datetime.date.today()
    toplam = (bitis - giris).days
    gecen = (bugun - giris).days
    kalan = (bitis - bugun).days

    if toplam <= 0:
        return 0, 0, 0, 0, "err"

    yuzde = max(0, min(100, int((gecen / toplam) * 100)))

    if kalan < 0:
        cls = "err"
    elif kalan <= 30 or yuzde >= 85:
        cls = "err"
    elif kalan <= 90 or yuzde >= 65:
        cls = "warn"
    else:
        cls = ""

    return toplam, gecen, kalan, yuzde, cls

def eto_initials(isim: str) -> str:
    parts = isim.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return isim[:2].upper()

def ship_card_html(row) -> str:
    cls = durum_class(row["Durum"])
    tip_emoji = {
        "Container": "📦",
        "Tanker": "🛢️",
        "Bulk Carrier": "⛏️",
        "Ro-Ro Cargo": "🚗",
        "General Cargo": "📦",
        "Live Stock": "🐄",
    }.get(row["Tip"], "🚢")

    # ETO fotoğrafı (varsa) yoksa baş harfler
    eto_img_path = row.get("EtoFoto", "")
    if eto_img_path:
        eto_block = f'<img class="eto-photo" src="{eto_img_path}" alt="{row["ETO"]}"/>'
    else:
        eto_block = f'<div class="eto-placeholder">{eto_initials(row["ETO"])}</div>'

    toplam, gecen, kalan, yuzde, kcls = kontrat_bilgi(row["Giris"], row["KontratBitis"])

    if kalan < 0:
        kalan_text = f"⚠️ Kontrat {abs(kalan)} gün önce bitti"
    elif kalan == 0:
        kalan_text = "⏰ Kontrat bugün bitiyor"
    else:
        kalan_text = f"⏳ {kalan} gün kaldı (%{yuzde} tamamlandı)"

    giris_fmt = row["Giris"]
    bitis_fmt = row["KontratBitis"]

    return f"""
    <div class="ship-card">
        <div class="card-flex">
            <div class="eto-left">
                {eto_block}
                <div class="eto-name">👨‍✈️ {row['ETO']}</div>
                <div class="eto-role">Baş Elektrik Zabiti (ETO)</div>
                <div class="contract-box">
                    <div class="contract-dates">
                        <span>📅 {giris_fmt}</span>
                        <span>{bitis_fmt} 📅</span>
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill {kcls}" style="width:{yuzde}%;"></div>
                    </div>
                    <div class="contract-remaining {kcls}">{kalan_text}</div>
                </div>
            </div>
            <div class="ship-right">
                <div class="ship-name">{tip_emoji} {row['Gemi']}</div>
                <div class="ship-imo">IMO: {row['IMO']} · {row['Tip']}</div>
                <div class="ship-info">
                    <b>Bayrak:</b> {row['Bayrak']}<br/>
                    <b>DWT:</b> {row['DWT']} &nbsp;|&nbsp; <b>GRT:</b> {row['GRT']}<br/>
                    <b>Yıl:</b> {row['Yıl']} &nbsp;|&nbsp; <b>LOA:</b> {row['LOA']}
                </div>
                <div class="ship-status {cls}">{row['Durum']}</div>
            </div>
        </div>
    </div>
    """

# ---------- Sidebar Navigasyon ----------
menu = st.sidebar.radio(
    "📌 Navigasyon",
    ["🏠 Dashboard",
     "🚢 Filo Yönetimi",
     "📜 Sertifika & Survey",
     "🛒 Satınalma",
     "📚 Teknik Dokümanlar",
     "🎓 ETO Eğitim & PSC",
     "⚡ Megger Kayıtları",
     "📄 Raporlama"],
)
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 TTS Ships · v3.2")

# ============================================================
# 🏠 DASHBOARD
# ============================================================
if menu == "🏠 Dashboard":
    st.subheader("📊 Filo Genel Durum")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Gemi", len(fleet_df))
    c2.metric("Uygun", (fleet_df["Durum"] == "🟢 Uygun").sum())
    c3.metric("Bakım", (fleet_df["Durum"] == "🟡 Bakım").sum())
    c4.metric("Arıza", (fleet_df["Durum"] == "🔴 Arıza").sum())

    st.markdown("---")
    st.subheader("🚢 Filo Kartları · ETO & Kontrat Takibi")

    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        tip_sec = st.multiselect("Tip Filtre", sorted(fleet_df["Tip"].unique()), default=sorted(fleet_df["Tip"].unique()))
    with f2:
        bayrak_sec = st.multiselect("Bayrak Filtre", sorted(fleet_df["Bayrak"].unique()), default=sorted(fleet_df["Bayrak"].unique()))
    with f3:
        arama = st.text_input("🔍 Gemi / IMO / ETO Ara")

    filtreli = fleet_df[fleet_df["Tip"].isin(tip_sec) & fleet_df["Bayrak"].isin(bayrak_sec)]
    if arama:
        filtreli = filtreli[
            filtreli["Gemi"].str.contains(arama, case=False, na=False) |
            filtreli["IMO"].str.contains(arama, case=False, na=False) |
            filtreli["ETO"].str.contains(arama, case=False, na=False)
        ]

    st.caption(f"Toplam **{len(filtreli)}** gemi gösteriliyor.")

    COLS = 3
    rows = filtreli.to_dict("records")
    for i in range(0, len(rows), COLS):
        cols = st.columns(COLS)
        for j, col in enumerate(cols):
            if i + j < len(rows):
                with col:
                    st.markdown(ship_card_html(rows[i + j]), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Gemi Tipi Dağılımı")
    st.bar_chart(fleet_df["Tip"].value_counts())

    st.subheader("🌍 Bayrak Dağılımı")
    st.bar_chart(fleet_df["Bayrak"].value_counts())

# ============================================================
# 🚢 FİLO YÖNETİMİ
# ============================================================
elif menu == "🚢 Filo Yönetimi":
    st.subheader("🚢 Filo Yönetimi (Tablo Görünümü)")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_tip = st.multiselect("Gemi Tipi", fleet_df["Tip"].unique(), default=list(fleet_df["Tip"].unique()))
    with col2:
        filter_bayrak = st.multiselect("Bayrak", fleet_df["Bayrak"].unique(), default=list(fleet_df["Bayrak"].unique()))
    with col3:
        search = st.text_input("🔍 Gemi / IMO / ETO Ara", key="fleet_search")

    filtered = fleet_df[fleet_df["Tip"].isin(filter_tip) & fleet_df["Bayrak"].isin(filter_bayrak)]
    if search:
        filtered = filtered[
            filtered["Gemi"].str.contains(search, case=False, na=False) |
            filtered["IMO"].str.contains(search, case=False, na=False) |
            filtered["ETO"].str.contains(search, case=False, na=False)
        ]

    st.dataframe(filtered, use_container_width=True)
    st.caption(f"Toplam {len(filtered)} gemi gösteriliyor.")

    with st.expander("➕ Yeni Gemi Ekle"):
        with st.form("yeni_gemi"):
            gemi = st.text_input("Gemi Adı")
            imo = st.text_input("IMO")
            tip = st.selectbox("Tip", ["Container", "Tanker", "Bulk Carrier", "Ro-Ro Cargo", "General Cargo", "Live Stock"])
            dwt = st.text_input("DWT")
            grt = st.text_input("GRT")
            bayrak = st.text_input("Bayrak")
            yil = st.text_input("Yıl")
            loa = st.text_input("LOA")
            eto = st.text_input("ETO")
            giris = st.date_input("Giriş Tarihi", datetime.date.today())
            bitis = st.date_input("Kontrat Bitiş", datetime.date.today() + datetime.timedelta(days=365))
            submit = st.form_submit_button("Kaydet")
            if submit and gemi and imo:
                st.success(f"✅ {gemi} (IMO {imo}) kaydedildi (demo).")

# ============================================================
# 📜 SERTİFİKA & SURVEY
# ============================================================
elif menu == "📜 Sertifika & Survey":
    st.subheader("📜 Sertifika & Survey Takibi")

    today = datetime.date.today()
    cert_data = [
        {"Gemi": "M/V MED STAR",      "Sertifika": "Safety Equipment (SE)",    "Bitiş": today + datetime.timedelta(days=15),  "Durum": "🟡 Yakında"},
        {"Gemi": "M/V MED STAR",      "Sertifika": "Load Line (LL)",           "Bitiş": today + datetime.timedelta(days=180), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/T MOON STAR",     "Sertifika": "IOPP",                     "Bitiş": today + datetime.timedelta(days=5),   "Durum": "🔴 Kritik"},
        {"Gemi": "M/T MOON STAR",     "Sertifika": "Safety Construction (SC)", "Bitiş": today + datetime.timedelta(days=240), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/T KUZEY STAR II", "Sertifika": "ISSC",                     "Bitiş": today + datetime.timedelta(days=90),  "Durum": "🟢 Geçerli"},
        {"Gemi": "M/V ATLANTIC STAR", "Sertifika": "IAPP",                     "Bitiş": today - datetime.timedelta(days=3),   "Durum": "🔴 Süresi Geçti"},
        {"Gemi": "M/V PACIFIC STAR",  "Sertifika": "Class Certificate",        "Bitiş": today + datetime.timedelta(days=45),  "Durum": "🟡 Yakında"},
        {"Gemi": "M/V VENUS STAR",    "Sertifika": "Safety Equipment (SE)",    "Bitiş": today + datetime.timedelta(days=200), "Durum": "🟢 Geçerli"},
        {"Gemi": "M/V MERCUR STAR",   "Sertifika": "Load Line (LL)",           "Bitiş": today + datetime.timedelta(days=12),  "Durum": "🟡 Yakında"},
        {"Gemi": "M/V SAPHIRA",       "Sertifika": "IOPP",                     "Bitiş": today + datetime.timedelta(days=320), "Durum": "🟢 Geçerli"},
    ]
    cert_df = pd.DataFrame(cert_data)

    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Sertifika", len(cert_df))
    c2.metric("Kritik", ((cert_df["Durum"] == "🔴 Kritik") | (cert_df["Durum"] == "🔴 Süresi Geçti")).sum())
    c3.metric("Yakında", (cert_df["Durum"] == "🟡 Yakında").sum())

    st.dataframe(cert_df, use_container_width=True)

# ============================================================
# 🛒 SATINALMA
# ============================================================
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
            st.session_state.purchases.append({
                "Tarih": datetime.date.today(),
                "Gemi": gemi, "Malzeme": malzeme, "Miktar": miktar,
                "Öncelik": oncelik, "Tedarikçi": tedarikci, "Not": notlar,
                "Durum": "🕓 Bekliyor"
            })
            st.success("✅ Talep oluşturuldu.")

    if st.session_state.purchases:
        st.markdown("### 📋 Talep Listesi")
        st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)
    else:
        st.info("Henüz talep oluşturulmadı.")

# ============================================================
# 📚 TEKNİK DOKÜMANLAR
# ============================================================
elif menu == "📚 Teknik Dokümanlar":
    st.subheader("📚 Teknik Doküman Kütüphanesi")

    docs = pd.DataFrame([
        {"Kategori": "Manuel", "Doküman": "Ana Şalter Panosu (MSB) Manual",        "Gemi": "M/V MED STAR",      "Rev": "R3"},
        {"Kategori": "Şema",   "Doküman": "Tek Hat Şeması (SLD)",                   "Gemi": "M/V MED STAR",      "Rev": "R5"},
        {"Kategori": "Manuel", "Doküman": "Jeneratör Kontrol Panosu Manual",        "Gemi": "M/T MOON STAR",     "Rev": "R2"},
        {"Kategori": "Şema",   "Doküman": "Aydınlatma Şeması",                      "Gemi": "M/V ATLANTIC STAR", "Rev": "R1"},
        {"Kategori": "Test",   "Doküman": "Megger Test Prosedürü (IR)",             "Gemi": "Tüm Filo",          "Rev": "R4"},
        {"Kategori": "Class",  "Doküman": "Class Rules - Electrical Installations", "Gemi": "Tüm Filo",          "Rev": "2025"},
        {"Kategori": "Manuel", "Doküman": "Bow Thruster Elektrik Manual",           "Gemi": "M/V A380",          "Rev": "R1"},
    ])
    st.dataframe(docs, use_container_width=True)

    kat = st.selectbox("Kategori Filtre", ["Tümü"] + sorted(docs["Kategori"].unique().tolist()))
    if kat != "Tümü":
        st.dataframe(docs[docs["Kategori"] == kat], use_container_width=True)

# ============================================================
# 🎓 ETO EĞİTİM & PSC
# ============================================================
elif menu == "🎓 ETO Eğitim & PSC":
    st.subheader("🎓 ETO Eğitim & PSC Simülasyonu")

    quiz = [
        {"Soru": "AC devrede Insulation Resistance (IR) minimum kaç MΩ olmalıdır?",
         "Secenekler": ["0.1 MΩ", "0.5 MΩ", "1 MΩ", "5 MΩ"], "Cevap": "1 MΩ"},
        {"Soru": "Megaohmmetre (Megger) testinde kullanılan gerilim hangisidir?",
         "Secenekler": ["12 V DC", "110 V AC", "500 V DC", "380 V AC"], "Cevap": "500 V DC"},
        {"Soru": "PSC'de '30 saniye kuralı' hangi konuyla ilgilidir?",
         "Secenekler": ["Emergency Generator", "Steering Gear", "Fire Pump", "Bilge Pump"], "Cevap": "Steering Gear"},
        {"Soru": "Emergency Switchboard hangi besleme kaynağını kullanır?",
         "Secenekler": ["Main Switchboard", "Emergency Generator", "Shore Power", "Bus Tie"], "Cevap": "Emergency Generator"},
        {"Soru": "Motor overload koruma cihazı hangisidir?",
         "Secenekler": ["MCB", "RCD", "Thermal Overload Relay", "Fuse"], "Cevap": "Thermal Overload Relay"},
    ]

    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
        st.session_state.score = 0

    if st.session_state.quiz_idx < len(quiz):
        q = quiz[st.session_state.quiz_idx]
        st.markdown(f"**Soru {st.session_state.quiz_idx + 1}/{len(quiz)}:** {q['Soru']}")
        secim = st.radio("Cevap:", q["Secenekler"], key=f"q{st.session_state.quiz_idx}")

        if st.button("✅ Onayla"):
            if secim == q["Cevap"]:
                st.session_state.score += 1
                st.success("Doğru!")
            else:
                st.error(f"Yanlış. Doğru cevap: {q['Cevap']}")
            st.session_state.quiz_idx += 1
            st.rerun()
    else:
        st.balloons()
        st.success(f"🎉 Sınav tamamlandı!
