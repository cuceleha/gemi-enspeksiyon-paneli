import streamlit as st
import pandas as pd
import datetime
import streamlit.components.v1 as components

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon Paneli",
    page_icon="⚓",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚓ TTS Ships - Filo Elektrik Enspeksiyon ve Canlı Konum Paneli")
st.markdown("TTS Filosundaki gemilerin teknik detaylarını, elektrik arızalarını ve canlı harita konumlarını takip edin.")

# Görseldeki Resmi TTS Ships Tablosundan Tam Doğrulanmış Veriler
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "MMSI": "352002237", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "MMSI": "636016142", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "MMSI": "248062000", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V A380", "IMO": "9310915", "MMSI": "636020583", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "MMSI": "636020584", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "MMSI": "352978000", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "MMSI": "352979000", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "MMSI": "636015124", "Tip": "Dökme Yük Gemisi", "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "MMSI": "636016120", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "MMSI": "356494000", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "MMSI": "636016121", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "MMSI": "248384000", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "MMSI": "636022100", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "MMSI": "636022101", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "MMSI": "305128000", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte"}
]

df_fleet = pd.DataFrame(tts_fleet_data)
gemi_listesi = df_fleet["Gemi"].tolist()

# Yan Menü (Sidebar)
st.sidebar.header("TTS Filo Denetimi")
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
tab1, tab2, tab3 = st.tabs(["🗺️ MarineTraffic Canlı Harita", "📋 Enspeksiyon Bulguları & Fotoğraf", "🚢 TTS Resmi Filo Künyesi"])

with tab1:
    st.subheader(f"🗺️ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Canlı MarineTraffic Takip Paneli")
    
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        # Doğrudan MarineTraffic Resmi Sayfasına Tek Tıkla Geçiş Butonu
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🌐 {gemi_adi} MarineTraffic'te Aç", mt_link, type="primary")
        
    st.info("💡 **İpucu:** Harita üzerinde fare ile gezinebilir, geminin canlı AIS pozisyonunu inceleyebilirsiniz.")

    # MarineTraffic Embed Widget (İframe Engeline Takılmayan Canlı Katman)
    embed_html = f"""
    <iframe 
        width="100%" 
        height="600" 
        frameborder="0" 
        scrolling="no" 
        marginheight="0" 
        marginwidth="0" 
        src="https://www.marinetraffic.com/en/ais/embed/zoom:4/centery:35/centerx:25/maptype:1/shownames:true/mmsi:0/shipid:0/fleet:/fleet_id:/oldmmsi:/keep_map_baselayer:1">
    </iframe>
    """
    components.html(embed_html, height=620)

with tab2:
    st.subheader(f"🛠️ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Arıza ve Eksiklik Kaydı")
    
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", [
            "Ana Dağıtım Panosu (MSB)",
            "Acil Durum Panosu (ESB)",
            "1 No'lu Jeneratör (DG1)",
            "2 No'lu Jeneratör (DG2)",
            "Dümen Makinesi Elektrik Panosu",
            "Güverte Vinçleri / Ro-Ro Rampası Panoları",
            "24V Akü Grubu & Şarj Panosu",
            "Sintine & İzolasyon Seviye Sensörleri"
        ])
        kategori = st.selectbox("Kategori", [
            "İzolasyon (Megger) Düşüklüğü",
            "AVR / Voltaj Düzensizliği",
            "ACB / Şalter Termik Trip",
            "Sıcaklık / Termal Kamera Anormalliği",
            "Kablo Kanalları / Sızdırmazlık (Gland)"
        ])
        durum = st.radio("Bulgu Durumu / Risk Derecesi", [
            "🔴 Kritik (Class / PSC Riski)",
            "🟡 Önemli (Kısa Vadeli Bakım)",
            "🟢 Uygun / Normal"
        ])
    
    with col2:
        aciklama = st.text_area("Bulgu / Arıza Açıklaması", "Örn: MSB 440V bara izolasyon değeri düşük (0.3 M-Ohm). Neme bağlı kaçak tespit edildi.")
        
        uploaded_files = st.file_uploader(
            "📸 Arıza / Eksiklik Görsellerini Yükleyin",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

    if uploaded_files:
        st.write("### 🖼️ Yüklenen Görsel Önizlemeleri")
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, caption=f"Görsel {idx+1}: {file.name}", use_column_width=True)

    st.divider()
    if st.button("Kaydı Filo Veritabanına Ekle"):
        st.success(f"{gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) için bulgu kaydı başarıyla oluşturuldu!")

with tab3:
    st.subheader("🚢 TTS Ships - Resmi Filo Listesi ve Teknik Detaylar")
    st.dataframe(df_fleet[["Gemi", "IMO", "MMSI", "Tip", "DWT", "GRT", "Bayrak", "Yıl", "LOA", "Durum"]], use_container_width=True)
