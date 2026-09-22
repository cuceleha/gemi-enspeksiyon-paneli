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

# Resmi TTS Ships Harita Görseline Göre Güncellenmiş Dünya Konumları
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Lat": 10.5000, "Lon": -66.9000, "Liman": "Venezuela / Karayipler", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Lat": 25.0000, "Lon": 165.0000, "Liman": "Kuzey Pasifik / Seyirde", "Durum": "🔴 Kritik"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Lat": 2.5000, "Lon": 101.5000, "Liman": "Malakka Boğazı / Güneydoğu Asya", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V KUZEY STAR", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Lat": -25.0000, "Lon": 45.0000, "Liman": "Güney Afrika / Hint Okyanusu", "Durum": "🟡 Takipte"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Lat": 27.0000, "Lon": 34.5000, "Liman": "Kızıldeniz / Seyirde", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Lat": 36.5000, "Lon": 25.0000, "Liman": "Ege Denizi / Doğu Akdeniz", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V MOON STAR", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Lat": 38.0000, "Lon": 15.0000, "Liman": "Orta Akdeniz", "Durum": "🔴 Kritik"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Lat": 41.2500, "Lon": 29.1000, "Liman": "Karadeniz / Seyir Halinde", "Durum": "🟢 Uygun"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Lat": 40.0100, "Lon": 26.2500, "Liman": "Çanakkale Boğazı Geçiş", "Durum": "🟢 Uygun"}
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
    st.subheader(f"🗺️ TTS Filosu Küresel Konum Haritası - Seçili Gemi: {gemi_adi}")
    
    # Harita Merkezini Seçili Geminin Koordinatına Ayarla
    map_center = [secili_gemi_bilgi["Lat"], secili_gemi_bilgi["Lon"]]
    
    # Dünya Haritası Görünümü İçin Zoom Seviyesi 3 Yapıldı
    m = folium.Map(location=map_center, zoom_start=3, tiles="OpenStreetMap")

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
