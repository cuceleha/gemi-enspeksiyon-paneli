import streamlit as st
import pandas as pd
import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Gemi Elektrik Enspeksiyon Paneli",
    page_icon="⚓",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚓ Gemi Elektrik Enspeksiyon ve Takip Paneli")
st.markdown("Filodaki gemilerin elektrik arızaları, denetim bulguları ve periyodik bakımlarını takip edin.")

# Yan Menü (Sidebar) - Filtreler ve Gemi Seçimi
st.sidebar.header("Denetim Parametreleri")
gemi_adi = st.sidebar.selectbox(
    "Gemi Seçiniz",
    ["M/V ATLANTIS", "M/V OCEAN KING", "M/V PACIFIC STAR", "M/V BLACK SEA"]
)

enspektor_adi = st.sidebar.text_input("Enspektör Adı Soyadı", "Elektrik Enspektörü")
tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()
st.sidebar.info("Verileri girdikten sonra alt kısımdaki panellerden durum takibi yapabilirsiniz.")

# Ana Sekmeler
tab1, tab2, tab3 = st.tabs(["📋 Enspeksiyon Bulguları", "⚡ Pano & Jeneratör Durumu", "📊 Raporlama"])

with tab1:
    st.subheader(f"{gemi_adi} - Elektrik Arıza ve Eksiklik Kaydı")
    
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", [
            "Ana Dağıtım Panosu (MSB)",
            "Acil Durum Panosu (ESB)",
            "1 No'lu Jeneratör (DG1)",
            "2 No'lu Jeneratör (DG2)",
            "Akü Grubu & Şarj Panosu",
            "Sintine & İzolasyon Seviyesi"
        ])
        kategori = st.selectbox("Kategori", ["İzolasyon (Megger)", "AVR / Senkronizasyon", "ACB / Koruma Rölesi", "Sıcaklık / Termal", "Aydınlatma / Kablo"])
    
    with col2:
        durum = st.radio("Bulgu Durumu", ["Kritik (Class/PSC Riski)", "Önemli (Kısa Vadeli Bakım)", "Uygun / Normal"])
        aciklama = st.text_area("Bulgu / Arıza Açıklaması", "Örn: MSB 440V bara izolasyon değeri düşük (0.2 M-Ohm). Neme bağlı kaçak tespit edildi.")

    if st.button("Kaydı Onayla ve Ekle"):
        st.success(f"{ekipman} için bulgu kaydı başarıyla oluşturuldu!")

with tab2:
    st.subheader("⚡ Kritik Ekipman Kontrol Listesi")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="MSB İzolasyon Direnci", value="Inf MΩ", delta="Normal")
    col_b.metric(label="DG1 Çalışma Saati", value="14,250 hrs", delta="+120 hrs")
    col_c.metric(label="24V Akü Grubu", value="26.4 V", delta="-0.2 V", delta_color="inverse")
    
    st.divider()
    
    st.write("### Hızlı Denetim Onay Kutuları")
    c1 = st.checkbox("MSB Isıtıcıları (Space Heaters) aktif ve çalışıyor.")
    c2 = st.checkbox("ACB Şalter mekanik kurma ve trip testleri yapıldı.")
    c3 = st.checkbox("Jeneratör Reverse Power ve Undervoltage korumaları test edildi.")
    c4 = st.checkbox("Panolarda FLIR termal kamera ile anormal sıcaklık saptanmadı.")

with tab3:
    st.subheader("📊 Filo Genel Özet")
    
    # Örnek Veri Seti
    data = {
        "Gemi": ["M/V ATLANTIS", "M/V OCEAN KING", "M/V PACIFIC STAR", "M/V BLACK SEA"],
        "Kritik Bulgu": [1, 0, 3, 0],
        "Açık İş Emri": [4, 2, 7, 1],
        "Son Denetim": ["2026-09-10", "2026-09-18", "2026-08-25", "2026-09-20"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
