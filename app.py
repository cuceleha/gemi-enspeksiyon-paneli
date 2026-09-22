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

# Başlık ve Açıklama
st.title("⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Filo Yönetim Paneli")
st.markdown("MarineTraffic entegrasyonu, sertifika/sürvey takibi, satınalma, teknik doküman kütüphanesi, ETO eğitim/PSC simülasyonu, megger kayıtları ve PDF/Excel raporlama paneli.")

# TTS Ships Filo Verileri (ttsships.com Orijinal Resim URL'leri ile)
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", "Giris": "2026-06-15", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/MED-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-15"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik", "ETO": "Mehmet KAYA", "Giris": "2026-04-01", "KontratAy": 6, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/AY-YILDIZI.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet", "Arıza": "DG1 AVR Arızası (Kritik)", "Malzeme": "AVR MX321 Bekleniyor", "Denetim": "2026-10-15"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte", "ETO": "Caner DEMİR", "Giris": "2026-08-10", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/KUZEY-YILDIZ-II.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner", "Arıza": "Sintine Sensörü Takipte", "Malzeme": "Talep Açıldı", "Denetim": "2026-11-01"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", "Giris": "2026-07-20", "KontratAy": 5, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/A380.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-10"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Burak ÇELİK", "Giris": "2026-05-12", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/AKBABA.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2026-12-20"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Oğuz ÖZTÜRK", "Giris": "2026-06-01", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/ALEXANDRA-I.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz", "Arıza": "Yok", "Malzeme": "Seyir Feneri LED Ampul", "Denetim": "2027-03-05"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte", "ETO": "Serkan AYDIN", "Giris": "2026-04-15", "KontratAy": 6, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/ALENA.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan", "Arıza": "Pano İzolasyonu Düşük", "Malzeme": "İzolasyon Spreyi", "Denetim": "2026-10-28"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik", "ETO": "Murat ASLAN", "Giris": "2026-03-10", "KontratAy": 6, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/ATLANTIC-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat", "Arıza": "MSB Şalteri (ACB) Trip", "Malzeme": "ACB Bobin Seti", "Denetim": "2026-10-02"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Volkan YILDIZ", "Giris": "2026-07-01", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/PACIFIC-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-04-12"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun", "ETO": "Hasan ERDOĞAN", "Giris": "2026-08-01", "KontratAy": 5, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/CHIEF-SEATTLE.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-05-18"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Ali ÖZKAN", "Giris": "2026-06-20", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/VENUS-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-22"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Tolga TEKİN", "Giris": "2026-07-10", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/MERCUR-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-30"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Onur KOÇ", "Giris": "2026-08-15", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/DENIZ-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-06-10"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Kaan YILMAZ", "Giris": "2026-07-25", "KontratAy": 4, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/BLACKSEA-STAR.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-07-01"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte", "ETO": "Zafer GÜNEŞ", "Giris": "2026-05-01", "KontratAy": 5, "Foto": "https://ttsships.com/wp-content/uploads/2023/11/SAPHIRA.jpg", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer", "Arıza": "Havalandırma Fanı Takipte", "Malzeme": "Kontaktör Seti", "Denetim": "2026-11-15"}
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

# GEMİ SEÇİM KUTUSU
selected_from_sidebar = st.sidebar.selectbox(
    "Gemi Seçiniz / Detay Detayı Görün",
    ["-- Filo Genel Görünümü --"] + df_fleet["Gemi"].tolist()
)

if selected_from_sidebar != "-- Filo Genel Görünümü --":
    st.session_state.selected_ship = selected_from_sidebar

# ==========================================
# ANA SAYFA: FİLO GENEL GÖRÜNÜMÜ (SEKMELER GİZLİ)
# ==========================================
if st.session_state.selected_ship is None or selected_from_sidebar == "-- Filo Genel Görünümü --":
    st.session_state.selected_ship = None
    
    st.subheader("🚢 TTS Ships Filo Listesi")
    
    # KPI METRİKLERİ
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Toplam Gemi", f"{len(df_fleet)} Gemi")
    kpi2.metric("Kritik Arızalı", f"{len(df_fleet[df_fleet['Durum'] == '🔴 Kritik'])} Gemi")
    kpi3.metric("Malzeme Bekleyen", f"{len(df_fleet[df_fleet['Malzeme'] != 'Tamam'])} Gemi")
    
    st.divider()

    # KART YAPISI VE BUTON İLE DETAYA GEÇİŞ
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    st.image(g["Foto"], use_container_width=True)
                    st.markdown(f"### {g['Gemi']}")
                    st.caption(f"**IMO:** {g['IMO']} | **Tip:** {g['Tip']}")
                    st.markdown(f"**Durum:** {g['Durum']}")
                    st.markdown(f"**ETO:** {g['ETO']}")
                    
                    if st.button(f"🔎 {g['Gemi']} Detaylı Paneli Aç", key=f"btn_{g['IMO']}"):
                        st.session_state.selected_ship = g['Gemi']
                        st.rerun()
                    st.divider()

# ==========================================
# DETAY SAYFASI: GEMİYE ÖZEL PANELLER (SEKMELER BURADA AÇILIR)
# ==========================================
else:
    gemi_adi = st.session_state.selected_ship
    secili_gemi_bilgi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

    if st.button("⬅️ Filo Genel Görünümüne Dön"):
        st.session_state.selected_ship = None
        st.rerun()

    st.markdown(f"# 🚢 {gemi_adi} Detaylı Enspeksiyon Paneli")
    
    # DETAYLI SEKMELER
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🌐 Canlı Takip", 
        "📜 Sertifika & Class",
        "🛒 Satınalma & Tedarik",
        "📖 Şemalar & Dokümanlar",
        "🎓 ETO Eğitim & PSC",
        "📋 Arıza Kaydı", 
        "⚡ Megger Ölçümü",
        "📊 Raporlama"
    ])

    with tab1:
        st.subheader(f"⚓ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Canlı Takip")
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🔴 MarineTraffic Canlı Konumu Aç", mt_link, type="primary", use_container_width=True)

    with tab2:
        st.subheader("📜 Sertifika & Yasal Belge Takibi")
        st.info("Class ve Sürvey geçerlilik durumları aktif olarak takip edilmektedir.")

    with tab3:
        st.subheader("🛒 Satınalma & Malzeme Talepleri")
        st.write(f"**Mevcut Malzeme Durumu:** {secili_gemi_bilgi['Malzeme']}")

    with tab4:
        st.subheader("📖 Şemalar & Teknik Doküman Kütüphanesi")
        st.download_button("📥 Elektrik Projesini İndir (ZIP)", b"Demo_Data", "Proje.zip")

    with tab5:
        st.subheader("🎓 ETO Eğitim & PSC Mülakat Simülasyonu")
        st.write("PSC denetimleri öncesi teknik kontrol adımları.")

    with tab6:
        st.subheader("📋 Arıza Kaydı Formu")
        ekipman = st.selectbox("Aksam / Ekipman", ["Ana Pano (MSB)", "Acil Pano (ESB)", "Jeneratör"])
        aciklama = st.text_area("Arıza Açıklaması", secili_gemi_bilgi['Arıza'])
        if st.button("Arızayı Kaydet"):
            st.success("Kayıt güncellendi.")

    with tab7:
        st.subheader("⚡ İzolasyon (Megger) Ölçümleri")
        st.number_input("Ölçülen Değer (MΩ)", value=5.0)

    with tab8:
        st.subheader("📊 Raporlama ve Dışa Aktar")
        st.write("Gemiye özel enspeksiyon rapor çıktısı.")
