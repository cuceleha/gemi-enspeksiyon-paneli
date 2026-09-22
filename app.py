import streamlit as st
import pandas as pd
import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide"
)

# KESİN YÜKLENEN GÜVENLİ SHIP CDN GÖRSELLERİ
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

# SIDEBAR
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

    # GENEL ÖZET TABLOLARI
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

    # GEMİ KARTLARI
    st.markdown("### 📷 TTS Filosu Gemi Kartları (Detay İçin Gemiyi Seçiniz)")
    
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    st.image(g["Foto"], use_container_width=True)
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
# 🚢 SAYFA 2: SEÇİLİ GEMİYE ÖZEL TÜM ALT PANELLER
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
    st.sidebar.write(f"**Katılış:** {secili_gemi_bilgi['Giris']}")
    st.sidebar.write(f"**Kontrat Süresi:** {secili_gemi_bilgi['KontratAy']} Ay")

    # TÜM ALT PANELLER (SEKMELER)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Canlı Takip & Harita", 
        "📋 Arıza Kaydı & Foto Yükleme", 
        "⚡ Megger İzolasyon Ölçümleri", 
        "🛒 Malzeme & Yedek Parça Talebi",
        "📄 Enspeksiyon Raporu Oluştur"
    ])

    # SEKMELER 1: CANLI TAKİP
    with tab1:
        st.subheader(f"⚓ {gemi_adi} Canlı Konum ve Bilgileri")
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🔴 {gemi_adi} MarineTraffic Canlı Haritasını Aç", mt_link, type="primary", use_container_width=True)
        st.image(secili_gemi_bilgi['Foto'], caption=f"{gemi_adi} Görseli", use_container_width=True)

    # SEKMELER 2: ARIZA KAYDI VE FOTOĞRAF YÜKLEME
    with tab2:
        st.subheader("📋 Arıza Bildirimi ve Görsel Ekleme")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            ekipman = st.selectbox("Arızalı Ekipman / Sistem", ["Jeneratör (DG1/DG2/DG3)", "Ana Pano (MSB)", "Dümen Makinesi", "Sintine Separatörü", "Seyir Fenerleri", "Vinç / Güverte Ekipmanı"])
            ariza_tanimi = st.text_area("Arıza Detayı ve Enspektör Notu", value=secili_gemi_bilgi['Arıza'])
            oncelik = st.select_slider("Öncelik Derecesi", options=["Düşük", "Orta", "Yüksek", "🔴 KRİTİK"])
        with col_b:
            uploaded_file = st.file_uploader("Arıza Fotoğrafı Yükle", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Yüklenen Arıza Görseli", width=300)
            if st.button("💾 Arıza Kaydını Güncelle"):
                st.success("Arıza kaydı sistem hafızasına güncellendi!")

    # SEKMELER 3: MEGGER İZOLASYON ÖLÇÜMLERİ
    with tab3:
        st.subheader("⚡ Megger / İzolasyon Direnci Ölçüm Tablosu")
        st.info("Pano ve motorların periyodik MΩ (Megohm) değerlerini giriniz.")
        
        megger_data = {
            "Ekipman": ["DG-1 Alternatör", "DG-2 Alternatör", "Baş Pervane (Bow Thruster)", "Yangın Pompası Motoru", "Dümen Hidrolik Motor 1"],
            "Ölçülen Değer (MΩ)": [50.0, 45.0, 1.2, 100.0, 85.0],
            "Durum": ["🟢 İyi", "🟢 İyi", "🔴 Düşük (Kritik)", "🟢 Mükemmel", "🟢 İyi"]
        }
        st.table(pd.DataFrame(megger_data))
        
        st.markdown("#### Yeni Ölçüm Ekle")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.text_input("Ekipman Adı")
        m_col2.number_input("Değer (MΩ)", min_value=0.0, max_value=1000.0, value=10.0)
        m_col3.selectbox("Durum Değerlendirmesi", ["🟢 İyi", "🟡 Takip Edilmeli", "🔴 Kritik"])

    # SEKMELER 4: MALZEME TALEBİ
    with tab4:
        st.subheader("🛒 Yedek Parça ve Malzeme Talep Formu")
        st.write(f"**Mevcut Talep Durumu:** `{secili_gemi_bilgi['Malzeme']}`")
        
        st.text_input("Parça / Malzeme Adı (Örn: AVR MX321, 63A Şalter)", value="" if secili_gemi_bilgi['Malzeme'] == "Tamam" else secili_gemi_bilgi['Malzeme'])
        st.number_input("Adet / Miktar", min_value=1, value=1)
        st.selectbox("Tedarik Limanı", ["İstanbul / Türkiye", "Singapur", "Rotterdam / Hollanda", "Süveyş / Mısır"])
        if st.button("🚀 Talep Formunu Satınalmaya Gönder"):
            st.success("Talep satınalma departmanına iletildi!")

    # SEKMELER 5: RAPOR OLUŞTURMA
    with tab5:
        st.subheader("📄 Enspeksiyon Raporu Çıktısı")
        st.write("Gemiye ait yapılan tüm incelemeleri ve test sonuçlarını tek tıkla raporlayabilirsiniz.")
        
        rapor_metni = f"""
        TTS SHIPS ELEKTRİK ENSPEKSİYON RAPORU
        ------------------------------------
        Gemi Adı: {gemi_adi}
        IMO No: {secili_gemi_bilgi['IMO']}
        Tarih: {datetime.date.today()}
        Enspektör: Ceyhun ÜCELEHAN
        ETO: {secili_gemi_bilgi['ETO']}
        
        DURUM ÖZETİ:
        - Genel Durum: {secili_gemi_bilgi['Durum']}
        - Arıza Durumu: {secili_gemi_bilgi['Arıza']}
        - Malzeme Durumu: {secili_gemi_bilgi['Malzeme']}
        """
        st.text_area("Rapor Önizleme", rapor_metni, height=200)
        st.download_button("📥 Raporu İndir (.TXT)", data=rapor_metni, file_name=f"{gemi_adi}_Enspeksiyon_Raporu.txt")
