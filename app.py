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

    /* Gemi Kartı */
    .ship-card {
        background: #ffffff;
        border: 1px solid #e3e8ef;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 15px;
        height: 100%;
    }
    .ship-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(30,111,217,0.25);
    }
    .ship-card img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .ship-name {
        font-weight: 700;
        font-size: 16px;
        color: #0b3d91;
        margin-bottom: 4px;
    }
    .ship-imo {
        font-size: 12px;
        color: #7a8699;
        margin-bottom: 8px;
    }
    .ship-info {
        font-size: 12.5px;
        color: #333;
        line-height: 1.55;
    }
    .ship-info b { color: #0b3d91; }
    .ship-status {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
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

# ---------- Tip bazlı varsayılan görsel URL'leri ----------
DEFAULT_IMAGES = {
    "Container":     "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800",
    "Tanker":        "https://images.unsplash.com/photo-1605281317010-fe5ffe798166?w=800",
    "Bulk Carrier":  "https://images.unsplash.com/photo-1559297434-fae8a1916a79?w=800",
    "Ro-Ro Cargo":   "https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=800",
    "General Cargo": "https://images.unsplash.com/photo-1568054668631-68c6b0e4f7b4?w=800",
    "Live Stock":    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
}
FALLBACK_IMG = "https://images.unsplash.com/photo-1524522173746-f628baad3644?w=800"

# ---------- Filo Verileri ----------
tts_fleet_data = [
    {"Gemi": "M/V MED STAR",      "IMO": "9337028", "Tip": "Container",     "DWT": "27254",    "GRT": "23633", "Bayrak": "Panama",          "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/T MOON STAR",     "IMO": "9667928", "Tip": "Tanker",        "DWT": "49997",    "GRT": "29940", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "183 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/T KUZEY STAR II", "IMO": "9499175", "Tip": "Tanker",        "DWT": "6107",     "GRT": "4081",  "Bayrak": "Malta",           "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V A380",          "IMO": "9310915", "Tip": "Ro-Ro Cargo",   "DWT": "1300",     "GRT": "1285",  "Bayrak": "Liberia",         "Yıl": "2003", "LOA": "75 m",     "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V AKBABA",        "IMO": "9319478", "Tip": "Ro-Ro Cargo",   "DWT": "1300",     "GRT": "1281",  "Bayrak": "Liberia",         "Yıl": "2004", "LOA": "75 m",     "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V ALEXANDRA I",   "IMO": "8876340", "Tip": "Bulk Carrier",  "DWT": "6005",     "GRT": "4949",  "Bayrak": "Panama",          "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V ALENA",         "IMO": "8857772", "Tip": "Bulk Carrier",  "DWT": "6059",     "GRT": "4949",  "Bayrak": "Panama",          "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Bulk Carrier",  "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberia",         "Yıl": "2011", "LOA": "225 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V PACIFIC STAR",  "IMO": "9470387", "Tip": "Bulk Carrier",  "DWT": "78128",    "GRT": "41718", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Bulk Carrier",  "DWT": "52428",    "GRT": "30174", "Bayrak": "Panama",          "Yıl": "2001", "LOA": "189,89 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V VENUS STAR",    "IMO": "9609134", "Tip": "Bulk Carrier",  "DWT": "80888",    "GRT": "44025", "Bayrak": "Liberia",         "Yıl": "2013", "LOA": "229 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V MERCUR STAR",   "IMO": "9609287", "Tip": "Bulk Carrier",  "DWT": "79520",    "GRT": "43501", "Bayrak": "Malta",           "Yıl": "2015", "LOA": "229 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V DENIZ STAR",    "IMO": "1071472", "Tip": "General Cargo", "DWT": "8300",     "GRT": "6641",  "Bayrak": "Liberia",         "Yıl": "2025", "LOA": "142 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "General Cargo", "DWT": "8330",     "GRT": "6732",  "Bayrak": "Liberia",         "Yıl": "2025", "LOA": "142 m",    "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
    {"Gemi": "M/V SAPHIRA",       "IMO": "7924425", "Tip": "Live Stock",    "DWT": "12900",    "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟢 Uygun", "ETO": "-", "Giris": "-", "Kontrat": "-", "Gorsel": ""},
]
fleet_df = pd.DataFrame(tts_fleet_data)

# ---------- Yardımcı: Durum CSS sınıfı ----------
def durum_class(durum: str) -> str:
    if "Arıza" in durum or "Süresi" in durum:
        return "err"
    if "Bakım" in durum or "Yakında" in durum:
        return "warn"
    return ""

# ---------- Yardımcı: Kart HTML ----------
def ship_card_html(row) -> str:
    img = row["Gorsel"] if row.get("Gorsel") else DEFAULT_IMAGES.get(row["Tip"], FALLBACK_IMG)
    cls = durum_class(row["Durum"])
    return f"""
    <div class="ship-card">
        <img src="{img}" alt="{row['Gemi']}" onerror="this.src='{FALLBACK_IMG}'"/>
        <div class="ship-name">🚢 {row['Gemi']}</div>
        <div class="ship-imo">IMO: {row['IMO']} &nbsp;·&nbsp; {row['Tip']}</div>
        <div class="ship-info">
            <b>Bayrak:</b> {row['Bayrak']}<br/>
            <b>DWT:</b> {row['DWT']} &nbsp;|&nbsp; <b>GRT:</b> {row['GRT']}<br/>
            <b>Yıl:</b> {row['Yıl']} &nbsp;|&nbsp; <b>LOA:</b> {row['LOA']}
        </div>
        <div class="ship-status {cls}">{row['Durum']}</div>
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
st.sidebar.caption("© 2026 TTS Ships · v3.0")

# ============================================================
# 🏠 DASHBOARD — KART GÖRÜNÜMÜ
# ============================================================
if menu == "🏠 Dashboard":
    st.subheader("📊 Filo Genel Durum")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Gemi", len(fleet_df))
    c2.metric("Uygun", (fleet_df["Durum"] == "🟢 Uygun").sum())
    c3.metric("Bakım", (fleet_df["Durum"] == "🟡 Bakım").sum())
    c4.metric("Arıza", (fleet_df["Durum"] == "🔴 Arıza").sum())

    st.markdown("---")
    st.subheader("🚢 Filo Kartları")

    # Filtreler
    f1, f2, f3 = st.columns([1, 1, 1])
    with f1:
        tip_sec = st.multiselect("Tip Filtre", sorted(fleet_df["Tip"].unique()), default=sorted(fleet_df["Tip"].unique()))
    with f2:
        bayrak_sec = st.multiselect("Bayrak Filtre", sorted(fleet_df["Bayrak"].unique()), default=sorted(fleet_df["Bayrak"].unique()))
    with f3:
        arama = st.text_input("🔍 Gemi / IMO Ara")

    filtreli = fleet_df[fleet_df["Tip"].isin(tip_sec) & fleet_df["Bayrak"].isin(bayrak_sec)]
    if arama:
        filtreli = filtreli[
            filtreli["Gemi"].str.contains(arama, case=False, na=False) |
            filtreli["IMO"].str.contains(arama, case=False, na=False)
        ]

    st.caption(f"Toplam **{len(filtreli)}** gemi gösteriliyor.")

    # Kart grid — 3 sütun
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
# 🚢 FİLO YÖNETİMİ (tablo görünümü)
# ============================================================
elif menu == "🚢 Filo Yönetimi":
    st.subheader("🚢 Filo Yönetimi (Tablo Görünümü)")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_tip = st.multiselect("Gemi Tipi", fleet_df["Tip"].unique(), default=list(fleet_df["Tip"].unique()))
    with col2:
        filter_bayrak = st.multiselect("Bayrak", fleet_df["Bayrak"].unique(), default=list(fleet_df["Bayrak"].unique()))
    with col3:
        search = st.text_input("🔍 Gemi / IMO Ara", key="fleet_search")

    filtered = fleet_df[fleet_df["Tip"].isin(filter_tip) & fleet_df["Bayrak"].isin(filter_bayrak)]
    if search:
        filtered = filtered[
            filtered["Gemi"].str.contains(search, case=False, na=False) |
            filtered["IMO"].str.contains(search, case=False, na=False)
        ]

    st.dataframe(filtered.drop(columns=["Gorsel"]), use_container_width=True)
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
        st.success(f"🎉 Sınav tamamlandı! Skor: {st.session_state.score}/{len(quiz)}")
        if st.button("🔄 Yeniden Başla"):
            st.session_state.quiz_idx = 0
            st.session_state.score = 0
            st.rerun()

# ============================================================
# ⚡ MEGGER KAYITLARI
# ============================================================
elif menu == "⚡ Megger Kayıtları":
    st.subheader("⚡ Megger / Insulation Resistance (IR) Kayıtları")

    with st.form("megger_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            gemi = st.selectbox("Gemi", fleet_df["Gemi"].tolist(), key="megger_gemi")
            devre = st.text_input("Devre / Ekipman")
        with col2:
            test_v = st.selectbox("Test Gerilimi", ["500 V DC", "1000 V DC", "2500 V DC"])
            ir_deger = st.number_input("IR Değeri (MΩ)", min_value=0.0, value=100.0, step=0.1)
        with col3:
            test_tarih = st.date_input("Test Tarihi", datetime.date.today())
            sonuc = st.selectbox("Sonuç", ["✅ Uygun", "⚠️ İzle", "❌ Uygun Değil"])

        if st.form_submit_button("💾 Kaydet") and devre:
            st.session_state.megger_records.append({
                "Tarih": test_tarih, "Gemi": gemi, "Devre": devre,
                "Test V": test_v, "IR (MΩ)": ir_deger, "Sonuç": sonuc
            })
            st.success("✅ Kayıt eklendi.")

    if st.session_state.megger_records:
        st.dataframe(pd.DataFrame(st.session_state.megger_records), use_container_width=True)
    else:
        st.info("Henüz megger kaydı yok.")

# ============================================================
# 📄 RAPORLAMA
# ============================================================
elif menu == "📄 Raporlama":
    st.subheader("📄 PDF & Excel Raporlama")

    rapor_tipi = st.selectbox("Rapor Tipi", ["Filo Listesi", "Satınalma", "Megger Kayıtları"])

    if rapor_tipi == "Filo Listesi":
        df_rapor = fleet_df.drop(columns=["Gorsel"])
    elif rapor_tipi == "Satınalma":
        df_rapor = pd.DataFrame(st.session_state.purchases) if st.session_state.purchases else pd.DataFrame([{"Not": "Kayıt yok"}])
    else:
        df_rapor = pd.DataFrame(st.session_state.megger_records) if st.session_state.megger_records else pd.DataFrame([{"Not": "Kayıt yok"}])

    st.dataframe(df_rapor, use_container_width=True)

    col1, col2 = st.columns(2)

    # --- Excel ---
    with col1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_rapor.to_excel(writer, index=False, sheet_name="Rapor")
        st.download_button(
            "⬇️ Excel İndir",
            data=buffer.getvalue(),
            file_name=f"tts_ships_{rapor_tipi.lower().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # --- PDF ---
    with col2:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "TTS Ships - Rapor", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 8, f"Rapor Tipi: {rapor_tipi}", ln=True)
        pdf.cell(0, 8, f"Tarih: {datetime.date.today()}", ln=True)
        pdf.ln(4)

        cols = list(df_rapor.columns)
        col_w = 190 / max(len(cols), 1)
        pdf.set_font("Helvetica", "B", 9)
        for c in cols:
            pdf.cell(col_w, 8, str(c)[:20], border=1)
        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        for _, row in df_rapor.iterrows():
            for c in cols:
                pdf.cell(col_w, 8, str(row[c])[:22], border=1)
            pdf.ln()

        pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="replace")
        st.download_button(
            "⬇️ PDF İndir",
            data=pdf_bytes,
            file_name=f"tts_ships_{rapor_tipi.lower().replace(' ', '_')}.pdf",
            mime="application/pdf",
        )
