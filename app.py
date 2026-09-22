import streamlit as st
import pandas as pd
import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon Paneli",
    page_icon="⚓",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚓ TTS Ships - Filo Elektrik Enspeksiyon ve Takip Paneli")
st.markdown("TTS Filosundaki gemilerin elektrik arızaları, megger testleri ve denetim bulgularını canlı takip edin.")

# Güncellenmiş TTS Filosu Veritabanı
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "949", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m"}
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
* **İnşa Yılı:** {secili_gemi_bilgi['Yıl']}
""")

enspektor_adi = st.sidebar.text_input("Enspektör Adı Soyadı", "Elektrik Enspektörü")
tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()

# Ana Sekmeler
tab1, tab2, tab3 = st.tabs(["📋 Enspeksiyon Bulguları & Fotoğraf", "⚡ Pano & Megger Testleri", "🚢 TTS Filo Künyesi ve Durumu"])

with tab1:
    st.subheader(f"🛠️ {gemi_adi} ({secili_gemi_bilgi['Tip']}) - Arıza ve Eksiklik Kaydı")
    
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
        
        # Fotoğraf Yükleme Paneli
        uploaded_files = st.file_uploader(
            "📸 Arıza / Eksiklik Görsellerini Yükleyin (Çoklu Yükleme Desteklenir)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

    # Yüklenen Görsellerin Önizlemesi
    if uploaded_files:
        st.write("### 🖼️ Yüklenen Görsel Önizlemeleri")
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, caption=f"Görsel {idx+1}: {file.name}", use_column_width=True)

    st.divider()
    if st.button("Kaydı Görsellerle Birlikte Filo Veritabanına Ekle"):
        st.success(f"{gemi_adi} - {ekipman} için bulgu kaydı ve ekli {len(uploaded_files) if uploaded_files else 0} adet görsel başarıyla yüklendi!")

with tab2:
    st.subheader(f"⚡ {gemi_adi} - Elektrik Parametreleri & Kontrol Listesi")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="MSB İzolasyon Direnci", value="Inf MΩ", delta="Normal")
    col_b.metric(label="24V Akü Grubu", value="26.8 V", delta="Kararlı")
    col_c.metric(label="İnşa Yılı / Yaş", value=f"{secili_gemi_bilgi['Yıl']}", delta=f"{2026 - int(secili_gemi_bilgi['Yıl'])} Yaşında")
    
    st.divider()
    
    st.write("### Hızlı Denetim Onay Kutuları")
    c1 = st.checkbox("MSB Isıtıcıları (Space Heaters) aktif ve çalışıyor.")
    c2 = st.checkbox("ACB Şalter mekanik kurma ve trip testleri yapıldı.")
    c3 = st.checkbox("Jeneratör Reverse Power ve Undervoltage korumaları test edildi.")
    c4 = st.checkbox("Panolarda FLIR termal kamera ile anormal sıcaklık saptanmadı.")

with tab3:
    st.subheader("🚢 TTS Ships - Resmi Filo Listesi ve Teknik Detaylar")
    st.dataframe(df_fleet, use_container_width=True)
