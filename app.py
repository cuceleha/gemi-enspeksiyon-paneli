import streamlit as st
import pandas as pd
import datetime
import os

# ---------------------------------------------------------
# SAYFA YAPILANDIRMASI
# ---------------------------------------------------------
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# YEREL VEYA YEDEK GÖRSEL YÖNETİMİ
# Resimleri GitHub / Streamlit projenizde 'assets' klasörüne koyabilirsiniz.
# ---------------------------------------------------------
def get_image_path(image_filename):
    local_path = os.path.join("assets", image_filename)
    if os.path.exists(local_path):
        return local_path
    # Yerel resim henüz yüklenmediyse gösterilecek varsayılan denizcilik simgesi/görseli
    return "https://raw.githubusercontent.com/streamlit/streamlit/main/e2e/scripts/components_app/static/cat.jpg"

# ---------------------------------------------------------
# FİLO VERİ SETİ (15 GEMİ TAM LİSTE)
# ---------------------------------------------------------
tts_fleet_data = [
    {
        "Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner Gemisi", "DWT": "27254", "GRT": "23633", 
        "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", 
        "Giris": "2026-06-15", "KontratAy": 4, "Foto": "med_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-15"
    },
    {
        "Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Kimyasal Tanker", "DWT": "49997", "GRT": "29940", 
        "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183,00 m", "Durum": "🔴 Kritik", "ETO": "Mehmet KAYA", 
        "Giris": "2026-04-01", "KontratAy": 6, "Foto": "ay_yildizi.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet", 
        "Arıza": "DG1 AVR Arızası (Kritik)", "Malzeme": "AVR MX321 Bekleniyor", "Denetim": "2026-10-15"
    },
    {
        "Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Petrol Tankeri", "DWT": "6107", "GRT": "4081", 
        "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte", "ETO": "Caner DEMİR", 
        "Giris": "2026-08-10", "KontratAy": 4, "Foto": "kuzey_yildiz.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner", 
        "Arıza": "Sintine Sensörü Takipte", "Malzeme": "Talep Açıldı", "Denetim": "2026-11-01"
    },
    {
        "Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", 
        "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75,00 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", 
        "Giris": "2026-07-20", "KontratAy": 5, "Foto": "a380.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-10"
    },
    {
        "Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", 
        "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75,00 m", "Durum": "🟢 Uygun", "ETO": "Burak ÇELİK", 
        "Giris": "2026-05-12", "KontratAy": 4, "Foto": "akbaba.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2026-12-20"
    },
    {
        "Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", 
        "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Oğuz ÖZTÜRK", 
        "Giris": "2026-06-01", "KontratAy": 4, "Foto": "alexandra_1.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz", 
        "Arıza": "Yok", "Malzeme": "Seyir Feneri LED Ampul", "Denetim": "2027-03-05"
    },
    {
        "Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", 
        "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte", "ETO": "Serkan AYDIN", 
        "Giris": "2026-04-15", "KontratAy": 6, "Foto": "alena.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan", 
        "Arıza": "Pano İzolasyonu Düşük", "Malzeme": "İzolasyon Spreyi", "Denetim": "2026-10-28"
    },
    {
        "Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", 
        "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225,00 m", "Durum": "🔴 Kritik", "ETO": "Murat ASLAN", 
        "Giris": "2026-03-10", "KontratAy": 6, "Foto": "atlantic_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat", 
        "Arıza": "MSB Şalteri (ACB) Trip", "Malzeme": "ACB Bobin Seti", "Denetim": "2026-10-02"
    },
    {
        "Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", 
        "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Volkan YILDIZ", 
        "Giris": "2026-07-01", "KontratAy": 4, "Foto": "pacific_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-04-12"
    },
    {
        "Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", 
        "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun", "ETO": "Hasan ERDOĞAN", 
        "Giris": "2026-08-01", "KontratAy": 5, "Foto": "chief_seattle.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-05-18"
    },
    {
        "Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", 
        "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229,00 m", "Durum": "🟢 Uygun", "ETO": "Ali ÖZKAN", 
        "Giris": "2026-06-20", "KontratAy": 4, "Foto": "venus_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-22"
    },
    {
        "Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", 
        "Bayrak": "Malta", "Yıl": "2015", "LOA": "229,00 m", "Durum": "🟢 Uygun", "ETO": "Tolga TEKİN", 
        "Giris": "2026-07-10", "KontratAy": 4, "Foto": "mercur_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-30"
    },
    {
        "Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", 
        "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142,00 m", "Durum": "🟢 Uygun", "ETO": "Onur KOÇ", 
        "Giris": "2026-08-15", "KontratAy": 4, "Foto": "deniz_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-06-10"
    },
    {
        "Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", 
        "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142,00 m", "Durum": "🟢 Uygun", "ETO": "Kaan YILMAZ", 
        "Giris": "2026-07-25", "KontratAy": 4, "Foto": "blacksea_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan", 
        "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-07-01"
    },
    {
        "Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvan Taşıyıcı", "DWT": "12900", "GRT": "38988", 
        "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte", "ETO": "Zafer GÜNEŞ", 
        "Giris": "2026-05-01", "KontratAy": 5, "Foto": "saphira.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer", 
        "Arıza": "Havalandırma Fanı Takipte", "Malzeme": "Kontaktör Seti", "Denetim": "2026-11-15"
    }
]

df_fleet = pd.DataFrame(tts_fleet_data)

# ---------------------------------------------------------
# SESSION STATE (OTURUM DURUMU TAKİBİ)
# ---------------------------------------------------------
if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

if "arizalar_db" not in st.session_state:
    st.session_state.arizalar_db = []

if "megger_db" not in st.session_state:
    st.session_state.megger_db = [
        {"Gemi": "M/T AY YILDIZI", "Ekipman": "DG-1 Alternatör", "Megohm": "0.2 MΩ", "Tarih": "2026-09-01", "Durum": "🔴 Kritik Düşük"},
        {"Gemi": "M/V ATLANTIC STAR", "Ekipman": "MSB Şalter Motoru", "Megohm": "0.8 MΩ", "Tarih": "2026-09-10", "Durum": "🔴 Kritik Düşük"},
        {"Gemi": "M/T KUZEY YILDIZ II", "Ekipman": "Sintine Pompası Motoru", "Megohm": "2.5 MΩ", "Tarih": "2026-09-12", "Durum": "🟡 Takip Edilmeli"}
    ]

# ---------------------------------------------------------
# YAN MENÜ (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.title("⚡ TTS Enspektör Paneli")
st.sidebar.subheader("👨‍💼 Elektrik Enspektörü")
st.sidebar.info("Ceyhun ÜCELEHAN")

st.sidebar.divider()

gemi_secenekleri = ["-- Filo Genel Görünümü --"] + df_fleet["Gemi"].tolist()

# Seçilen gemi değiştiğinde session state senkronizasyonu
def on_select_change():
    secilen = st.session_state.sidebar_select
    if secilen == "-- Filo Genel Görünümü --":
        st.session_state.selected_ship = None
    else:
        st.session_state.selected_ship = secilen

current_idx = 0
if st.session_state.selected_ship in df_fleet["Gemi"].tolist():
    current_idx = gemi_secenekleri.index(st.session_state.selected_ship)

st.sidebar.selectbox(
    "Gemi Seçiniz / Detaya Git",
    gemi_secenekleri,
    index=current_idx,
    key="sidebar_select",
    on_change=on_select_change
)

st.sidebar.divider()
st.sidebar.markdown("### 📊 Filo Özet İstatistikler")
st.sidebar.write(f"• **Toplam Gemi:** {len(df_fleet)}")
st.sidebar.write(f"• **Kritik Arıza:** {len(df_fleet[df_fleet['Durum'] == '🔴 Kritik'])}")
st.sidebar.write(f"• **Takipte:** {len(df_fleet[df_fleet['Durum'] == '🟡 Takipte'])}")

# =========================================================
# 🏠 SAYFA 1: FİLO GENEL BAKIŞ
# =========================================================
if st.session_state.selected_ship is None:
    st.title("⚡ TTS Ships - Filo Genel Bakış Paneli")
    st.markdown("Filodaki tüm gemilerin durumları, görevdeki ETO'lar ve görsel filo kartları.")

    # 1. METRİKLER / KPI KARTLARI
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    toplam_gemi = len(df_fleet)
    kritik_sayisi = len(df_fleet[df_fleet["Durum"] == "🔴 Kritik"])
    malzeme_sayisi = len(df_fleet[df_fleet["Malzeme"] != "Tamam"])

    kpi1.metric("🚢 Toplam Filo Gemisi", f"{toplam_gemi} Gemi")
    kpi2.metric("🔴 Kritik Elektrik Arızası", f"{kritik_sayisi} Gemi", delta="-2 Acil Müdahale", delta_color="inverse")
    kpi3.metric("🛒 Malzeme / Parça Talebi", f"{malzeme_sayisi} Gemi", delta="Tedarik Sürecinde")
    kpi4.metric("📅 Denetimi Yaklaşan (30 Gün)", "3 Gemi", delta="Yaklaşıyor", delta_color="off")

    st.divider()

    # 2. HIZLI DURUM TABLOLARI
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("🚨 Kritik ve Takipteki Arızalar")
        ariza_df = df_fleet[df_fleet["Durum"].isin(["🔴 Kritik", "🟡 Takipte"])][["Gemi", "Durum", "Arıza", "ETO"]]
        st.dataframe(ariza_df, use_container_width=True, hide_index=True)

    with col_t2:
        st.subheader("🛒 Parça Bekleyen Gemiler")
        malz_df = df_fleet[df_fleet["Malzeme"] != "Tamam"][["Gemi", "Malzeme", "Durum", "ETO"]]
        st.dataframe(malz_df, use_container_width=True, hide_index=True)

    st.divider()

    # 3. GEMİ KARTLARI
    st.subheader("📷 TTS Filosu Gemi Kartları (Detay İçin Gemiyi Seçiniz)")
    
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    # Görsel Gösterimi
                    img_src = get_image_path(g["Foto"])
                    st.image(img_src, caption=f"{g['Gemi']} ({g['Tip']})", use_container_width=True)
                    
                    st.markdown(f"### {g['Gemi']}")
                    st.caption(f"**IMO:** {g['IMO']} | **Tip:** {g['Tip']} | **Bayrak:** {g['Bayrak']}")
                    st.markdown(f"* **Elektrik Durumu:** {g['Durum']}")
                    st.markdown(f"* **Görevli ETO:** 👨‍✈️ {g['ETO']}")
                    st.markdown(f"* **Mevcut Arıza:** `{g['Arıza']}`")
                    
                    if st.button(f"🔍 {g['Gemi']} Detaylı Paneline Git", key=f"btn_gemi_{g['IMO']}", use_container_width=True):
                        st.session_state.selected_ship = g['Gemi']
                        st.rerun()
                    st.divider()

# =========================================================
# 🚢 SAYFA 2: SEÇİLİ GEMİYE ÖZEL FULL DETAYLI PANEL
# =========================================================
else:
    gemi_adi = st.session_state.selected_ship
    secili_gemi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

    if st.button("⬅️ Filo Genel Görünümüne Geri Dön", type="secondary"):
        st.session_state.selected_ship = None
        st.rerun()

    st.title(f"🚢 {gemi_adi} - Detaylı Enspeksiyon & Elektrik Yönetim Paneli")

    # SIDEBAR GEMİ KÜNYESİ
    st.sidebar.divider()
    st.sidebar.markdown(f"### 📋 {gemi_adi} Künye")
    st.sidebar.markdown(f"""
    * **IMO No:** {secili_gemi['IMO']}
    * **Gemi Tipi:** {secili_gemi['Tip']}
    * **Bayrak:** {secili_gemi['Bayrak']}
    * **DWT / GRT:** {secili_gemi['DWT']} / {secili_gemi['GRT']}
    * **Boy (LOA):** {secili_gemi['LOA']}
    * **İnşa Yılı:** {secili_gemi['Yıl']}
    * **Elektrik Durumu:** {secili_gemi['Durum']}
    """)

    st.sidebar.subheader("👨‍✈️ Gemideki ETO")
    st.sidebar.image(secili_gemi['EtoFoto'], caption=f"ETO: {secili_gemi['ETO']}", width=100)
    st.sidebar.write(f"**Katılış Tarihi:** {secili_gemi['Giris']}")
    st.sidebar.write(f"**Kontrat Süresi:** {secili_gemi['KontratAy']} Ay")

    # ---------------------------------------------------------
    # EKSİKSİZ TÜM ALT PANELLER (SEKMELER)
    # ---------------------------------------------------------
    tab_canli, tab_ariza, tab_megger, tab_malzeme, tab_rapor = st.tabs([
        "🌐 Canlı Takip & AIS Haritası",
        "📋 Arıza Kaydı & Fotoğraf Yükleme",
        "⚡ Megger (İzolasyon) Ölçüm Tablosu",
        "🛒 Parça & Malzeme Talepleri",
        "📄 Enspeksiyon Raporu & PDF Çıktısı"
    ])

    # SEKMELER 1: CANLI TAKİP & HARİTA
    with tab_canli:
        st.subheader(f"⚓ {gemi_adi} Canlı Konum ve MarineTraffic Takibi")
        st.info("Canlı AIS verisi ve gemi detaylı görünümü.")
        
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi['IMO']}"
        st.link_button(f"🌐 {gemi_adi} MarineTraffic Canlı Haritasını Yeni Sekmede Aç", mt_link, type="primary")
        
        c_col1, c_col2 = st.columns([2, 1])
        with c_col1:
            st.image(get_image_path(secili_gemi["Foto"]), caption=f"{gemi_adi} Güncel Görseli", use_container_width=True)
        with c_col2:
            st.markdown("#### 📍 Son Bildirilen Durum")
            st.write(f"**En Son Denetim:** {secili_gemi['Denetim']}")
            st.write(f"**Mevcut Arıza Durumu:** {secili_gemi['Arıza']}")
            st.write(f"**Malzeme Tedarik:** {secili_gemi['Malzeme']}")

    # SEKMELER 2: ARIZA KAYDI VE FOTOĞRAF YÜKLEME
    with tab_ariza:
        st.subheader("📋 Arıza Bildirimi ve Fotoğraf Yükleme Paneli")
        
        col_a1, col_a2 = st.columns([1, 1])
        with col_a1:
            ekipman = st.selectbox(
                "Arızalı Ekipman / Sistem",
                ["Jeneratör (DG1 / DG2 / DG3)", "Ana Pano (MSB)", "Dümen Makinesi Panosu", "Sintine Separatörü", "Seyir Fenerleri", "Güverte Vinçleri / Irgat", "Diğer"]
            )
            ariza_detay = st.text_area("Arıza Tanımı ve Enspektör Notu", value=secili_gemi['Arıza'])
            oncelik = st.select_slider("Öncelik Seviyesi", options=["Düşük", "Orta", "Yüksek", "🔴 KRİTİK ACİL"])
            
        with col_a2:
            st.markdown("#### 📷 Arıza Görseli Yükle")
            uploaded_file = st.file_uploader("Gemi/Pano Arıza Fotoğrafı (JPG, PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Yüklenen Arıza Görseli", width=300)
            
            if st.button("💾 Arıza Kaydını Sistem Hafızasına Kaydet", type="primary"):
                st.session_state.arizalar_db.append({
                    "Gemi": gemi_adi,
                    "Ekipman": ekipman,
                    "Detay": ariza_detay,
                    "Öncelik": oncelik,
                    "Tarih": datetime.date.today().strftime("%Y-%m-%d")
                })
                st.success("Arıza kaydı başarıyla sisteme eklendi!")

        st.divider()
        st.markdown("#### 📜 Bu Gemide Geçmişte Açılan Arıza Kayıtları")
        gemi_arizalari = [a for a in st.session_state.arizalar_db if a["Gemi"] == gemi_adi]
        if gemi_arizalari:
            st.dataframe(pd.DataFrame(gemi_arizalari), use_container_width=True)
        else:
            st.info("Bu gemi için henüz yeni eklenmiş aktif kayıt bulunmuyor.")

    # SEKMELER 3: MEGGER İZOLASYON ÖLÇÜMLERİ
    with tab_megger:
        st.subheader("⚡ Megger (İzolasyon Direnci) Test Tablosu")
        st.caption("Pano, alternatör ve elektrik motorlarının periyodik MΩ (Megohm) test sonuçları.")
        
        # Mevcut Kayıtları Göster
        gemi_megger = [m for m in st.session_state.megger_db if m["Gemi"] == gemi_adi]
        if gemi_megger:
            st.table(pd.DataFrame(gemi_megger)[["Ekipman", "Megohm", "Tarih", "Durum"]])
        else:
            st.warning("Bu gemi için girilmiş özel Megger ölçümü yok. Aşağıdan ekleyebilirsiniz.")

        st.divider()
        st.markdown("#### ➕ Yeni Ölçüm Ekle")
        m1, m2, m3, m4 = st.columns(4)
        m_ekipman = m1.text_input("Ekipman Adı (Örn: DG-1 Stator)")
        m_val = m2.number_input("Ölçülen Değer (MΩ)", min_value=0.0, max_value=1000.0, value=5.0, step=0.1)
        m_durum = m3.selectbox("Durum", ["🟢 Mükemmel (>100 MΩ)", "🟢 İyi (>5 MΩ)", "🟡 Takip Edilmeli (1-5 MΩ)", "🔴 Kritik Düşük (<1 MΩ)"])
        
        if m4.button("⚡ Ölçümü Kaydet"):
            st.session_state.megger_db.append({
                "Gemi": gemi_adi,
                "Ekipman": m_ekipman,
                "Megohm": f"{m_val} MΩ",
                "Tarih": datetime.date.today().strftime("%Y-%m-%d"),
                "Durum": m_durum
            })
            st.success("Megger ölçüm kaydı güncellendi!")
            st.rerun()

    # SEKMELER 4: MALZEME & YEDEK PARÇA TALEBİ
    with tab_malzeme:
        st.subheader("🛒 Elektrik Malzeme & Yedek Parça Talep Paneli")
        st.write(f"**Mevcut Malzeme Durumu:** `{secili_gemi['Malzeme']}`")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            parca_adi = st.text_input("Talep Edilen Parça / Ekipman", value="" if secili_gemi['Malzeme'] == "Tamam" else secili_gemi['Malzeme'])
            parca_adet = st.number_input("Miktar / Adet", min_value=1, value=1)
            parca_kod = st.text_input("IMPAC / Katalog Kodu (Opsiyonel)", placeholder="Örn: 33 01 22")
        with col_m2:
            liman = st.selectbox("Teslim Edilecek İkmal Limanı", ["İstanbul / Türkiye", "Singapur", "Rotterdam / Hollanda", "Süveyş / Mısır", "Tuzla Tersane"])
            aciklama = st.text_area("Satınalma İçin Notlar", placeholder="Aciliyet durumu, voltaj/akım değerleri vb.")
            
        if st.button("🚀 Talep Formunu Satınalmaya İlet", type="primary"):
            st.success(f"{parca_adi} ({parca_adet} Adet) talebi Satınalma Departmanı'na iletildi!")

    # SEKMELER 5: RAPOR OLUŞTURMA VE ÇIKTI
    with tab_rapor:
        st.subheader("📄 Elektrik Enspeksiyon Rapor Çıktısı")
        st.write("Yapılan tüm incelemeler, megger testleri ve arızalar otomatik rapora dönüştürülür.")
        
        rapor_taslak = f"""
====================================================================
               TTS SHIPS ELEKTRİK ENSPEKSİYON RAPORU
====================================================================
TARİH       : {datetime.date.today().strftime('%d.%m.%Y')}
ENSPEKTÖR   : Ceyhun ÜCELEHAN
GEMİ ADI    : {gemi_adi}
IMO NO      : {secili_gemi['IMO']} | BAYRAK: {secili_gemi['Bayrak']}
GEMİ TİPİ   : {secili_gemi['Tip']} | LOA: {secili_gemi['LOA']}
GÖREVLI ETO : {secili_gemi['ETO']}

1. GENEL ELEKTRİK DURUMU
--------------------------------------------------------------------
• Durum Değerlendirmesi : {secili_gemi['Durum']}
• Aktif Arıza Kaydı    : {secili_gemi['Arıza']}
• Malzeme Durumu       : {secili_gemi['Malzeme']}

2. ENSPEKTÖR DEĞERLENDİRME NOTLARI
--------------------------------------------------------------------
• Ana Pano (MSB) ve Jeneratörlerin genel durumu kontrol edildi.
• Megger testleri periyodik takibe alındı.
• Görevli ETO ({secili_gemi['ETO']}) ile bakım planlaması gözden geçirildi.

====================================================================
Rapor Oluşturuldu: TTS Enspektör Paneli v2.0
====================================================================
        """
        
        st.text_area("📄 Rapor Önizleme", rapor_taslak, height=280)
        st.download_button(
            label="📥 Raporu Metin Belgesi Olarak İndir (.TXT)",
            data=rapor_taslak,
            file_name=f"{gemi_adi.replace('/', '_')}_Enspeksiyon_Raporu.txt",
            mime="text/plain"
        )
