import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import st_folium

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon Paneli",
    page_icon="⚓",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚓ TTS Ships - Filo Elektrik Enspeksiyon ve Canlı Konum Paneli")
st.markdown("TTS Filosundaki gemilerin canlı konumları, elektrik arızaları, megger testleri ve denetim bulgularını takip edin.")

# Güncellenmiş TTS Filosu (Konum ve Koordinat Verileri Dahil)
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Lat": 40.985, "Lon": 28.780, "Liman": "Ambarlı Limanı", "Durum": "🟢 Uygun"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Lat": 40.750, "Lon": 29.500, "Liman": "TÜPRAŞ / İzmit", "Durum": "🔴 Kritik"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Lat": 40.850, "Lon": 29.280, "Liman": "Tuzla Tersaneler Bölgesi", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Lat": 41.020, "Lon": 28.950, "Liman": "Harem Ro-Ro Limanı", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Lat": 40.710, "Lon": 29.800, "Liman": "Yılport / Dilovası", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Lat": 38.420, "Lon": 27.130, "Liman": "Alsancak / İzmir", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Lat": 36.800, "Lon": 34.630, "Liman": "Mersin Limanı", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Lat": 40.800, "Lon": 29.350, "Liman": "Yalova Tersaneler", "Durum": "🔴 Kritik"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Lat": 41.250, "Lon": 29.100, "Liman": "Karadeniz / Seyir Halinde", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Lat": 40.010, "Lon": 26.250, "Liman": "Çanakkale Boğazı Geçiş", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Lat": 36.580, "Lon": 36.170, "Liman": "İskenderun Limanı", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Lat": 41.000, "Lon": 28.970, "Liman": "Zeytinburnu Demir Sahası", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Lat": 40.860, "Lon": 29.250, "Liman": "Tuzla Sedef Tersanesi", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Lat": 40.870, "Lon": 29.260, "Liman": "Tuzla Desan Tersanesi", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Lat": 36.850, "Lon": 28.250, "Liman": "Marmaris / Demirde", "Durum": "🟡 Takipte"}
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
* **Bulunduğu Konum:** {secili_gemi_bilgi['Liman']}
* **Koordinat:** {secili_gemi_bilgi['Lat']}, {secili_gemi_bilgi['Lon']}
* **Elektrik Durumu:** {secili_gemi_bilgi['Durum']}
""")

enspektor_adi = st.sidebar.text_input("Enspektör Adı Soyadı", "Elektrik Enspektörü")
tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()

# Ana Sekmeler
tab1, tab2, tab3 = st.tabs(["🗺️ Canlı Harita & Konum", "📋 Enspeksiyon Bulguları & Fotoğraf", "🚢 TTS Filo Künyesi ve Durumu"])

with tab1:
    st.subheader(f"🗺️ TTS Filosu Canlı Konum Haritası - Seçili Gemi: {gemi_adi}")
    
    # Harita Merkezini Seçili Geminin Koordinatına Ayarla
    map_center = [secili_gemi_bilgi["Lat"], secili_gemi_bilgi["Lon"]]
    
    # Ücretsiz ve API Anahtarı İstemeyen Standart Harita Katmanı
    m = folium.Map(location=map_center, zoom_start=8, tiles="OpenStreetMap")

    color_map = {"🟢 Uygun": "green", "🟡 Takipte": "orange", "🔴 Kritik": "red"}

    # Tüm Filoyu Haritaya İşle
    for _, row in df_fleet.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4>{row['Gemi']}</h4>
            <b>IMO:</b> {row['IMO']}<br>
            <b>Tip:</b> {row['Tip']}<br>
            <b>Konum:</b> {row['Liman']}<br>
            <b>Elektrik Sağlığı:</b> {row['Durum']}
        </div>
        """
        
        # Seçili gemiye özel belirgin ikon
        is_selected = row["Gemi"] == gemi_adi
        icon_color = "purple" if is_selected else color_map.get(row["Durum"], "blue")
        
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['Gemi']} - {row['Liman']}",
            icon=folium.Icon(color=icon_color, icon='ship', prefix='fa')
        ).add_to(m)

    st_folium(m, width="100%", height=500)

with tab2:
    st.subheader(f"🛠️ {gemi_adi} - Arıza ve Eksiklik Kaydı")
    
    col_k1, col_k2 = st.columns(2)
    col_k1.info(f"📍 **Otomatik Çekilen Konum:** {secili_gemi_bilgi['Liman']}")
    col_k2.info(f"🌐 **GPS Koordinatı:** Enlem {secili_gemi_bilgi['Lat']} | Boylam {secili_gemi_bilgi['Lon']}")
    
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
    if st.button("Kaydı Konum Bilgisiyle Birlikte Filo Veritabanına Ekle"):
        st.success(f"{gemi_adi} ({secili_gemi_bilgi['Liman']}) için bulgu kaydı başarıyla oluşturuldu!")

with tab3:
    st.subheader("🚢 TTS Ships - Resmi Filo Listesi, Konumları ve Teknik Detaylar")
    st.dataframe(df_fleet[["Gemi", "IMO", "Tip", "Liman", "Durum", "Bayrak", "Yıl", "Lat", "Lon"]], use_container_width=True)
