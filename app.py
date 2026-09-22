import streamlit as st
import pandas as pd
import datetime
import io

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide"
)

# KESİN ÇALIŞAN SABİT CDN GÖRSEL ADRESLERİ (HTTPS JPEG)
IMG_CONTAINER = "https://images.unsplash.com/photo-1559136555-9303baea8ebd?auto=format&fit=crop&w=800&q=80"
IMG_TANKER = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80"
IMG_BULK = "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80"
IMG_RORO = "https://images.unsplash.com/photo-1516214104703-d870798883c5?auto=format&fit=crop&w=800&q=80"

# TTS Ships Filo Verileri
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", "Giris": "2026-06-15", "KontratAy": 4, "Foto": IMG_CONTAINER, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-15"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik", "ETO": "Mehmet KAYA", "Giris": "2026-04-01", "KontratAy": 6, "Foto": IMG_TANKER, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet", "Arıza": "DG1 AVR Arızası (Kritik)", "Malzeme": "AVR MX321 Bekleniyor", "Denetim": "2026-10-15"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte", "ETO": "Caner DEMİR", "Giris": "2026-08-10", "KontratAy": 4, "Foto": IMG_TANKER, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner", "Arıza": "Sintine Sensörü Takipte", "Malzeme": "Talep Açıldı", "Denetim": "2026-11-01"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", "Giris": "2026-07-20", "KontratAy": 5, "Foto": IMG_RORO, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-10"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Burak ÇELİK", "Giris": "2026-05-12", "KontratAy": 4, "Foto": IMG_RORO, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2026-12-20"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Oğuz ÖZTÜRK", "Giris": "2026-06-01", "KontratAy": 4, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz", "Arıza": "Yok", "Malzeme": "Seyir Feneri LED Ampul", "Denetim": "2027-03-05"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte", "ETO": "Serkan AYDIN", "Giris": "2026-04-15", "KontratAy": 6, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan", "Arıza": "Pano İzolasyonu Düşük", "Malzeme": "İzolasyon Spreyi", "Denetim": "2026-10-28"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik", "ETO": "Murat ASLAN", "Giris": "2026-03-10", "KontratAy": 6, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat", "Arıza": "MSB Şalteri (ACB) Trip", "Malzeme": "ACB Bobin Seti", "Denetim": "2026-10-02"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Volkan YILDIZ", "Giris": "2026-07-01", "KontratAy": 4, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-04-12"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun", "ETO": "Hasan ERDOĞAN", "Giris": "2026-08-01", "KontratAy": 5, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-05-18"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Ali ÖZKAN", "Giris": "2026-06-20", "KontratAy": 4, "Foto": IMG_CONTAINER, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-22"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Tolga TEKİN", "Giris": "2026-07-10", "KontratAy": 4, "Foto": IMG_CONTAINER, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-30"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Onur KOÇ", "Giris": "2026-08-15", "KontratAy": 4, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-06-10"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Kaan YILMAZ", "Giris": "2026-07-25", "KontratAy": 4, "Foto": IMG_BULK, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-07-01"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte", "ETO": "Zafer GÜNEŞ", "Giris": "2026-05-01", "KontratAy": 5, "Foto": IMG_RORO, "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer", "Arıza": "Havalandırma Fanı Takipte", "Malzeme": "Kontaktör Seti", "Denetim": "2026-11-15"}
]

df_fleet = pd.DataFrame(tts_fleet_data)

if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

if "bulgular" not in st.session_state:
    st.session_state.bulgular = []

# YAN MENÜ (SIDEBAR)
st.sidebar.header("⚡ TTS Enspektör Paneli")
st.sidebar.subheader("👨‍💼 Elektrik Enspektörü")
st.sidebar.info("Ceyhun ÜCELEHAN")

gemi_secenekleri = ["-- Filo Genel Görünümü --"] + df_fleet["Gemi"].tolist()
secilen_sidebar = st.sidebar.selectbox("Gemi Seçiniz / Detaya Git", gemi_secenekleri, index=0 if st.session_state.selected_ship is None else gemi_secenekleri.index(st.session_state.selected_ship))

if secilen_sidebar != "-- Filo Genel Görünümü --":
    st.session_state.selected_ship = secilen_sidebar
elif secilen_sidebar == "-- Filo Genel Görünümü --" and st.session_state.selected_ship is not None:
    st.session_state.selected_ship = None

# ==========================================
# 🏠 SAYFA 1: FİLO GENEL BAKIŞ
# ==========================================
if st.session_state.selected_ship is None:
    st.title("⚡ TTS Ships - Filo Genel Bakış Paneli")
    st.markdown("Filodaki tüm gemilerin durumları, görevdeki ETO'lar ve görsel filo kartları.")

    # ÜST METRİKLER
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    toplam_gemi = len(df_fleet)
    kritik_gemi_sayisi = len(df_fleet[df_fleet["Durum"] == "🔴 Kritik"])
    malzeme_bekleyen = len(df_fleet[df_fleet["Malzeme"] != "Tamam"])

    kpi_col1.metric("🚢 Toplam Filo Gemisi", f"{toplam_gemi} Gemi")
    kpi_col2.metric("🔴 Kritik Elektrik Arızası", f"{kritik_gemi_sayisi} Gemi", delta="-2 Acil", delta_color="inverse")
    kpi_col3.metric("🛒 Malzeme / Parça Talebi", f"{malzeme_bekleyen} Gemi", delta="Tedarikte")
    kpi_col4.metric("📅 Denetimi Yaklaşan (30 Gün)", "3 Gemi", delta="Yaklaşıyor", delta_color="off")

    st.divider()

    # GENEL TABLOLAR
    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        st.markdown("### 🚨 Kritik Arızalı Gemiler")
        kritik_df = df_fleet[df_fleet["Durum"].isin(["🔴 Kritik", "🟡 Takipte"])][["Gemi", "Durum", "Arıza", "ETO"]]
        st.dataframe(kritik_df, use_container_width=True)

    with p_col2:
        st.markdown("### 🛒 Malzeme İhtiyacı Olan Gemiler")
        malzeme_df = df_fleet[df_fleet["Malzeme"] != "Tamam"][["Gemi", "Malzeme", "Durum"]]
        st.dataframe(malzeme_df, use_container_width=True)

    st.divider()

    # GEMİ KARTLARI (KESİN YÜKLENEN HTML HTML IMG YÖNTEMİ)
    st.markdown("### 📷 TTS Filosu Gemi Kartları (Detay İçin Gemiyi Seçiniz)")
    
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    # HTML img kullanarak engelleyicileri tamamen atlıyoruz
                    st.markdown(f'<img src="{g["Foto"]}" style="width:100%; height:200px; object-fit:cover; border-radius:8px;">', unsafe_allow_html=True)
                    st.markdown(f"#### {g['Gemi']}")
                    st.caption(f"**IMO:** {g['IMO']} | **Tip:** {g['Tip']} | **Bayrak:** {g['Bayrak']}")
                    st.markdown(f"* **Elektrik Durumu:** {g['Durum']}")
                    st.markdown(f"* **Görevli ETO:** 👨‍✈️ {g['ETO']}")
                    st.markdown(f"* **Mevcut Arıza:** `{g['Arıza']}`")
                    
                    if st.button(f"🔍 {g['Gemi']} Detaylı Paneline Git", key=f"btn_gemi_{g['IMO']}", use_container_width=True):
                        st.session_state.selected_ship = g['Gemi']
                        st.rerun()
                    st.divider()

# ==========================================
# 🚢 SAYFA 2: SEÇİLİ GEMİYE ÖZEL DETAYLI PANEL
# ==========================================
else:
    gemi_adi = st.session_state.selected_ship
    secili_gemi_bilgi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

    if st.button("⬅️ Filo Genel Görünümüne Geri Dön", type="secondary"):
        st.session_state.selected_ship = None
        st.rerun()

    st.title(f"🚢 {gemi_adi} - Detaylı Enspeksiyon & Elektrik Yönetim Paneli")

    # SIDEBAR KÜNYE
    st.sidebar.divider()
    st.sidebar.markdown(f"### 📋 {gemi_adi} Künye")
    st.sidebar.markdown(f"""
    * **IMO No:** {secili_gemi_bilgi['IMO']}
    * **Gemi Tipi:** {secili_gemi_bilgi['Tip']}
    * **Bayrak:** {secili_gemi_bilgi['Bayrak']}
    * **DWT / GRT:** {secili_gemi_bilgi['DWT']} / {secili_gemi_bilgi['GRT']}
    * **Boy (LOA):** {secili_gemi_bilgi['LOA']}
    * **İnşa Yılı:** {secili_gemi_bilgi['Yıl']}
    * **Elektrik Durumu:** {secili_gemi_bilgi['Durum']}
    """)

    st.sidebar.subheader("👨‍✈️ Gemideki ETO & Kontrat")
    st.sidebar.image(secili_gemi_bilgi['EtoFoto'], caption=f"ETO: {secili_gemi_bilgi['ETO']}", width=120)

    # DETAYLI SEKMELER
    tab1, tab2, tab3 = st.tabs(["🌐 Canlı Takip", "📋 Arıza Kaydı & Foto", "⚡ Megger Ölçümü"])

    with tab1:
        st.subheader(f"⚓ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Canlı Takip")
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🔴 {gemi_adi} MarineTraffic Canlı Haritasını Aç", mt_link, type="primary", use_container_width=True)
        st.markdown(f'<img src="{secili_gemi_bilgi["Foto"]}" style="width:100%; max-height:400px; object-fit:cover; border-radius:8px;">', unsafe_allow_html=True)

    with tab2:
        st.subheader("📋 Arıza Kaydı")
        st.write(f"**Mevcut Durum:** {secili_gemi_bilgi['Arıza']}")

    with tab3:
        st.subheader("⚡ Megger Ölçümü")
        st.number_input("Ölçülen İzolasyon Değeri (MΩ)", value=5.0)
