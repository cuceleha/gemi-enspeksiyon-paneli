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
st.title("⚡ TTS Ships - Filo Elektrik Enspeksiyon ve Canlı Takip Paneli")
st.markdown("MarineTraffic entegrasyonu ile gemi takibi, elektrik arıza kayıtları, megger testleri ve raporlama paneli.")

# Görseldeki Resmi TTS Ships Tablosundan Tam Doğrulanmış Veriler
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte"}
]

df_fleet = pd.DataFrame(tts_fleet_data)
gemi_listesi = df_fleet["Gemi"].tolist()

# Hafızada Bulgu Verilerini Tutma (Session State)
if "bulgular" not in st.session_state:
    st.session_state.bulgular = []

# Yan Menü (Sidebar)
st.sidebar.header("⚡ TTS Enspektör Paneli")
gemi_adi = st.sidebar.selectbox("Gemi Seçiniz", gemi_listesi)

secili_gemi_bilgi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

st.sidebar.markdown(f"""
* **IMO No:** {secili_gemi_bilgi['IMO']}
* **Gemi Tipi:** {secili_gemi_bilgi['Tip']}
* **Bayrak:** {secili_gemi_bilgi['Bayrak']}
* **DWT / GRT:** {secili_gemi_bilgi['DWT']} / {secili_gemi_bilgi['GRT']}
* **Boy (LOA):** {secili_gemi_bilgi['LOA']}
* **İnşa Yılı:** {secili_gemi_bilgi['Yıl']}
* **Elektrik Durumu:** {secili_gemi_bilgi['Durum']}
""")

enspektor_adi = st.sidebar.text_input("Enspektör Adı Soyadı", "Elektrik Enspektörü")
tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()

# Ana Sekmeler
tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 MarineTraffic Canlı Takip", 
    "📋 Enspeksiyon Bulguları & Fotoğraf", 
    "⚡ Megger (İzolasyon) Ölçüm Kaydı",
    "📊 Filo Raporu & Excel İndir"
])

# TAB 1: MARINETRAFFIC CANLI TAKİP
with tab1:
    st.subheader(f"⚓ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - MarineTraffic Canlı Konum Kartı")
    
    col_mt1, col_mt2 = st.columns([2, 1])
    
    with col_mt1:
        st.info(f"📍 **{gemi_adi}** gemisinin canlı AIS konumunu, rota, sürat ve liman varış bilgilerini MarineTraffic üzerinde canlı görüntülemek için aşağıdaki butona tıklayın.")
        
        # MarineTraffic Doğrudan Canlı Bağlantı Linki
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🔴 {gemi_adi} Canlı MarineTraffic Haritasını Aç", mt_link, type="primary", use_container_width=True)
        
    with col_mt2:
        st.metric("Seçili Gemi IMO", secili_gemi_bilgi['IMO'])
        st.metric("Gemi Tipi", secili_gemi_bilgi['Tip'])
        st.metric("Elektrik Durumu", secili_gemi_bilgi['Durum'])

# TAB 2: AR IZA VE BULGU KAYDI
with tab2:
    st.subheader(f"🛠️ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Elektrik Arıza Kaydı Formu")
    
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", [
            "Ana Dağıtım Panosu (MSB)",
            "Acil Durum Panosu (ESB)",
            "1 No'lu Jeneratör (DG1)",
            "2 No'lu Jeneratör (DG2)",
            "3 No'lu Jeneratör (DG3)",
            "Dümen Makinesi Elektrik Panosu",
            "Güverte Vinçleri / Ro-Ro Rampası Panoları",
            "24V Akü Grubu & Şarj Panosu",
            "Sintine & İzolasyon Seviye Sensörleri",
            "Sintine / Sintine Pompası Panoları"
        ])
        kategori = st.selectbox("Kategori", [
            "İzolasyon (Megger) Düşüklüğü",
            "AVR / Voltaj Düzensizliği",
            "ACB / Şalter Termik Trip",
            "Sıcaklık / Termal Kamera Anormalliği",
            "Kablo Kanalları / Sızdırmazlık (Gland)",
            "Topraklama Hatası (Earth Fault)"
        ])
        durum = st.radio("Bulgu Durumu / Risk Derecesi", [
            "🔴 Kritik (Class / PSC Riski)",
            "🟡 Önemli (Kısa Vadeli Bakım)",
            "🟢 Uygun / Normal"
        ])
    
    with col2:
        aciklama = st.text_area("Bulgu / Arıza Açıklaması", "Örn: MSB 440V bara izolasyon değeri düşük (0.3 M-Ohm). Neme bağlı kaçak tespit edildi.")
        uploaded_files = st.file_uploader("📸 Arıza / Eksiklik Görselleri Yükleyin", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        st.write("### 🖼️ Yüklenen Görsel Önizlemeleri")
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, caption=f"Görsel {idx+1}: {file.name}", use_column_width=True)

    st.divider()
    if st.button("Kaydı Filo Veritabanına Ekle"):
        st.session_state.bulgular.append({
            "Tarih": str(tarih),
            "Gemi": gemi_adi,
            "IMO": secili_gemi_bilgi['IMO'],
            "Enspektör": enspektor_adi,
            "Ekipman": ekipman,
            "Kategori": kategori,
            "Risk Durumu": durum,
            "Açıklama": aciklama
        })
        st.success(f"{gemi_adi} için bulgu kaydı veritabanına eklendi!")

# TAB 3: MEGGER TESTİ KAYDI
with tab3:
    st.subheader(f"⚡ {gemi_adi} - İzolasyon Direnci (Megger) Ölçüm Paneli")
    st.info("💡 **Standart:** 440V AC sistemler için minimum kabul edilebilir izolasyon değeri **1.0 MΩ**'dur.")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        megger_ekipman = st.selectbox("Ölçüm Yapılan Ekipman", [
            "DG1 Alternatör Sargıları",
            "DG2 Alternatör Sargıları",
            "MSB 440V Busbar (Bara)",
            "Dümen Motoru 1",
            "Dümen Motoru 2",
            "Bow Thruster Motoru"
        ])
    with m_col2:
        megger_deger = st.number_input("Ölçülen İzolasyon Değeri (MΩ)", min_value=0.0, max_value=1000.0, value=5.0, step=0.1)
    with m_col3:
        if megger_deger < 1.0:
            st.error("🔴 İZOLASYON KRİTİK DÜŞÜK! (Arıza Riski)")
        elif megger_deger < 5.0:
            st.warning("🟡 İZOLASYON ORTA DÜŞÜK (Takip Edilmeli)")
        else:
            st.success("🟢 İZOLASYON SAĞLIKLI (Normal)")

# TAB 4: EXCEL RAPORLAMA
with tab4:
    st.subheader("📊 Filo Genel Denetim Raporu ve Excel Çıktısı")
    
    if len(st.session_state.bulgular) > 0:
        df_bulgu = pd.DataFrame(st.session_state.bulgular)
        st.dataframe(df_bulgu, use_container_width=True)
        
        # Excel İndirme Butonu
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_bulgu.to_excel(writer, index=False, sheet_name='Enspeksiyon Bulguları')
        
        st.download_button(
            label="📥 Tüm Bulguları Excel (.xlsx) Olarak İndir",
            data=buffer.getvalue(),
            file_name=f"TTS_Elektrik_Enspeksiyon_Raporu_{tarih}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Henüz yeni bir bulgu eklenmedi. 'Enspeksiyon Bulguları' sekmesinden yeni kayıtlar oluşturabilirsiniz.")
    
    st.divider()
    st.write("### 🚢 TTS Resmi Filo Künyesi")
    st.dataframe(df_fleet[["Gemi", "IMO", "Tip", "DWT", "GRT", "Bayrak", "Yıl", "LOA", "Durum"]], use_container_width=True)
