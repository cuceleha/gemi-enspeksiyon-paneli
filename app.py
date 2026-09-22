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

# TTS Filosu Gemi Listesi
tts_fleet = [
    "TTS BARBAROS",
    "TTS SHIPS 1",
    "TTS SHIPS 2",
    "TTS SHIPS 3",
    "TTS SHIPS 4",
    "TTS VOLKAN",
    "TTS POYRAZ"
]

# Yan Menü (Sidebar) - Filtreler ve Gemi Seçimi
st.sidebar.header("TTS Filo Denetimi")
gemi_adi = st.sidebar.selectbox("Gemi Seçiniz", tts_fleet)

enspektor_adi = st.sidebar.text_input("Enspektör Adı Soyadı", "Elektrik Enspektörü")
tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()
st.sidebar.success(f"Seçili Gemi: **{gemi_adi}**")

# Ana Sekmeler
tab1, tab2, tab3 = st.tabs(["📋 Enspeksiyon Bulguları", "⚡ Pano & Megger Testleri", "📊 TTS Filo Özet"])

with tab1:
    st.subheader(f"🛠️ {gemi_adi} - Arıza ve Eksiklik Kaydı")
    
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", [
            "Ana Dağıtım Panosu (MSB)",
            "Acil Durum Panosu (ESB)",
            "1 No'lu Jeneratör (DG1)",
            "2 No'lu Jeneratör (DG2)",
            "3 No'lu Jeneratör (DG3)",
            "Dümen Makinesi Elektrik Panosu",
            "Güverte Aydınlatma & Vinç Panoları",
            "24V Akü Grubu & Şarj Panosu"
        ])
        kategori = st.selectbox("Kategori", [
            "İzolasyon (Megger) Düşüklüğü",
            "AVR / Volt Voltaj Düzensizliği",
            "ACB / Şalter Termik Trip",
            "Sıcaklık / Termal Kamera Anormalliği",
            "Kablo Kanalları / Sızdırmazlık (Gland)"
        ])
    
    with col2:
        durum = st.radio("Bulgu Durumu / Risk Derecesi", [
            "🔴 Kritik (Class / PSC Riski)",
            "🟡 Önemli (Kısa Vadeli Bakım)",
            "🟢 Uygun / Normal"
        ])
        aciklama = st.text_area("Bulgu / Arıza Açıklaması", "Örn: MSB 440V bara izolasyon değeri düşük (0.3 M-Ohm). Neme bağlı kaçak tespit edildi.")

    if st.button("Kaydı Filo Veritabanına Ekle"):
        st.success(f"{gemi_adi} - {ekipman} için bulgu kaydı başarıyla oluşturuldu!")

with tab2:
    st.subheader(f"⚡ {gemi_adi} - Kritik İzolasyon ve Ekipman Değerleri")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="MSB İzolasyon Direnci", value="Inf MΩ", delta="Normal")
    col_b.metric(label="DG1 Çalışma Saati", value="18,450 hrs", delta="+85 hrs")
    col_c.metric(label="24V Akü Grubu", value="26.8 V", delta="Kararlı")
    
    st.divider()
    
    st.write("### Hızlı Denetim Onay Kutuları")
    c1 = st.checkbox("MSB Isıtıcıları (Space Heaters) aktif ve çalışıyor.")
    c2 = st.checkbox("ACB Şalter mekanik kurma ve trip testleri yapıldı.")
    c3 = st.checkbox("Jeneratör Reverse Power ve Undervoltage korumaları test edildi.")
    c4 = st.checkbox("Panolarda FLIR termal kamera ile anormal sıcaklık saptanmadı.")

with tab3:
    st.subheader("📊 TTS Ships - Genel Filo Durumu")
    
    # TTS Filosu Örnek Veri Seti
    data = {
        "Gemi Adı": tts_fleet,
        "Kritik Bulgu": [1, 0, 2, 0, 1, 0, 0],
        "Açık İş Emri": [3, 1, 5, 2, 4, 0, 1],
        "Son Denetim Tarihi": ["2026-09-15", "2026-09-20", "2026-08-30", "2026-09-22", "2026-09-12", "2026-09-18", "2026-09-05"],
        "Durum": ["🔴 İnceleme Bekliyor", "🟢 Sorunsuz", "🔴 Müdahale Gerekli", "🟢 Sorunsuz", "🟡 Takipte", "🟢 Sorunsuz", "🟢 Sorunsuz"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
        
