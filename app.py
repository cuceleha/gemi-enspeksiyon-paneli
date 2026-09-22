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

# TTS Ships Filo Verileri (MarineTraffic & Denizcilik CDN Görselleri İle)
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", "Giris": "2026-06-15", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-15"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik", "ETO": "Mehmet KAYA", "Giris": "2026-04-01", "KontratAy": 6, "Foto": "https://images.unsplash.com/photo-1516214104703-d870798883c5?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet", "Arıza": "DG1 AVR Arızası (Kritik)", "Malzeme": "AVR MX321 Bekleniyor", "Denetim": "2026-10-15"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte", "ETO": "Caner DEMİR", "Giris": "2026-08-10", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner", "Arıza": "Sintine Sensörü Takipte", "Malzeme": "Talep Açıldı", "Denetim": "2026-11-01"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", "Giris": "2026-07-20", "KontratAy": 5, "Foto": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-10"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Burak ÇELİK", "Giris": "2026-05-12", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1524522173746-f628baad3644?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2026-12-20"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Oğuz ÖZTÜRK", "Giris": "2026-06-01", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz", "Arıza": "Yok", "Malzeme": "Seyir Feneri LED Ampul", "Denetim": "2027-03-05"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte", "ETO": "Serkan AYDIN", "Giris": "2026-04-15", "KontratAy": 6, "Foto": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan", "Arıza": "Pano İzolasyonu Düşük", "Malzeme": "İzolasyon Spreyi", "Denetim": "2026-10-28"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik", "ETO": "Murat ASLAN", "Giris": "2026-03-10", "KontratAy": 6, "Foto": "https://images.unsplash.com/photo-1505705694340-019e1e335916?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat", "Arıza": "MSB Şalteri (ACB) Trip", "Malzeme": "ACB Bobin Seti", "Denetim": "2026-10-02"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Volkan YILDIZ", "Giris": "2026-07-01", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-04-12"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun", "ETO": "Hasan ERDOĞAN", "Giris": "2026-08-01", "KontratAy": 5, "Foto": "https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-05-18"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Ali ÖZKAN", "Giris": "2026-06-20", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1516214104703-d870798883c5?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-02-22"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Tolga TEKİN", "Giris": "2026-07-10", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-01-30"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Onur KOÇ", "Giris": "2026-08-15", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-06-10"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Kaan YILMAZ", "Giris": "2026-07-25", "KontratAy": 4, "Foto": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan", "Arıza": "Yok", "Malzeme": "Tamam", "Denetim": "2027-07-01"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte", "ETO": "Zafer GÜNEŞ", "Giris": "2026-05-01", "KontratAy": 5, "Foto": "https://images.unsplash.com/photo-1524522173746-f628baad3644?w=500&q=80", "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer", "Arıza": "Havalandırma Fanı Takipte", "Malzeme": "Kontaktör Seti", "Denetim": "2026-11-15"}
]

df_fleet = pd.DataFrame(tts_fleet_data)

# Session State Yönetimi
if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

if "bulgular" not in st.session_state:
    st.session_state.bulgular = []

# YAN MENÜ (SIDEBAR)
st.sidebar.header("⚡ TTS Enspektör Paneli")
st.sidebar.subheader("👨‍💼 Elektrik Enspektörü")
st.sidebar.info("Ceyhun ÜCELEHAN")

# HIZLI GEMİ SEÇİM DROPDOWN'U
gemi_secenekleri = ["-- Filo Genel Görünümü --"] + df_fleet["Gemi"].tolist()
secilen_sidebar = st.sidebar.selectbox("Gemi Seçiniz / Detaya Git", gemi_secenekleri, index=0 if st.session_state.selected_ship is None else gemi_secenekleri.index(st.session_state.selected_ship))

if secilen_sidebar != "-- Filo Genel Görünümü --":
    st.session_state.selected_ship = secilen_sidebar
elif secilen_sidebar == "-- Filo Genel Görünümü --" and st.session_state.selected_ship is not None:
    st.session_state.selected_ship = None

# ==========================================
# 🏠 SAYFA 1: FİLO GENEL BAKIŞ (GEMİ SEÇİLMEDİĞİNDE)
# ==========================================
if st.session_state.selected_ship is None:
    st.title("⚡ TTS Ships - Filo Genel Bakış Paneli")
    st.markdown("Filodaki tüm gemilerin durumları, görevdeki ETO'lar, kritik arızalar ve görsel filo kartları.")

    # ÜST METRİKLER (KPI CARDS)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    toplam_gemi = len(df_fleet)
    kritik_gemi_sayisi = len(df_fleet[df_fleet["Durum"] == "🔴 Kritik"])
    malzeme_bekleyen = len(df_fleet[df_fleet["Malzeme"] != "Tamam"])

    kpi_col1.metric("🚢 Toplam Filo Gemisi", f"{toplam_gemi} Gemi")
    kpi_col2.metric("🔴 Kritik Elektrik Arızası", f"{kritik_gemi_sayisi} Gemi", delta="-2 Acil", delta_color="inverse")
    kpi_col3.metric("🛒 Malzeme / Parça Talebi", f"{malzeme_bekleyen} Gemi", delta="Tedarikte")
    kpi_col4.metric("📅 Denetimi Yaklaşan (30 Gün)", "3 Gemi", delta="Yaklaşıyor", delta_color="off")

    st.divider()

    # GENEL TABLOLAR
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

    # KART YAPISI (GEMİLERE TIKLAYINCA DETAY AÇILIR)
    st.markdown("### 📷 TTS Filosu Gemi Kartları (Detayları Görmek İçin Gemiyi Seçiniz)")
    
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    st.image(g["Foto"], use_container_width=True, caption=f"MarineTraffic Görseli: {g['Gemi']}")
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
# 🚢 SAYFA 2: SEÇİLİ GEMİYE ÖZEL DETAYLI PANEL VE TÜM SEKMELER
# ==========================================
else:
    gemi_adi = st.session_state.selected_ship
    secili_gemi_bilgi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

    # GERİ DÖN BUTONU
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

    katilis_tarihi = datetime.datetime.strptime(str(secili_gemi_bilgi['Giris']), "%Y-%m-%d").date()
    kontrat_ay = int(secili_gemi_bilgi['KontratAy'])
    bitis_tarihi = katilis_tarihi + datetime.timedelta(days=kontrat_ay * 30)
    bugun = datetime.date.today()
    kalan_gun = max(0, (bitis_tarihi - bugun).days)

    st.sidebar.markdown(f"""
    * **Katılış:** `{katilis_tarihi.strftime('%d.%m.%Y')}`
    * **Bitiş:** `{bitis_tarihi.strftime('%d.%m.%Y')}`
    * **Kalan Süre:** **{kalan_gun} Gün**
    """)

    tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

    # DETAYLI 11 PANEL
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "🌐 Canlı Takip", 
        "📜 Sertifika & Class",
        "🛒 Satınalma & Tedarik",
        "📖 Şemalar & Dokümanlar",
        "🎓 ETO Eğitim & PSC",
        "👨‍✈️ Elektrik Zabitleri",
        "📋 Arıza Kaydı & Foto", 
        "⚡ Megger Ölçümü",
        "📝 PSC Checklist",
        "📦 Yedek Parça Takip",
        "📊 Raporlama & Export"
    ])

    # TAB 1: MARINETRAFFIC
    with tab1:
        st.subheader(f"⚓ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - MarineTraffic Canlı Takip")
        col_mt1, col_mt2 = st.columns([2, 1])
        with col_mt1:
            st.info(f"📍 **{gemi_adi}** gemisinin canlı AIS konumunu MarineTraffic haritası üzerinde açabilirsiniz.")
            mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
            st.link_button(f"🔴 {gemi_adi} MarineTraffic Canlı Haritasını Aç", mt_link, type="primary", use_container_width=True)
            st.image(secili_gemi_bilgi['Foto'], caption=f"{gemi_adi} - MarineTraffic Görseli", use_container_width=True)
        with col_mt2:
            st.metric("Gemi IMO", secili_gemi_bilgi['IMO'])
            st.metric("Gemi Tipi", secili_gemi_bilgi['Tip'])
            st.metric("Elektrik Durumu", secili_gemi_bilgi['Durum'])

    # TAB 2: SERTİFİKALAR
    with tab2:
        st.subheader(f"📜 {gemi_adi} - Sertifika & Sürvey Takip Paneli")
        sertifika_listesi = [
            {"Belge Adı": "Annual Electrical Class Survey", "Kategori": "Class Sürvey", "Duzenleyen": "Class / RINA", "SonTarih": "2026-10-15"},
            {"Belge Adı": "Seyir Fenerleri Tip Onay Sertifikası", "Kategori": "Ekipman Sertifikası", "Duzenleyen": "Glamox / DNV", "SonTarih": "2026-11-20"},
            {"Belge Adı": "Megger & Ölçüm Cihazları Kalibrasyonu", "Kategori": "Kalibrasyon", "Duzenleyen": "Akredite Lab", "SonTarih": "2026-10-02"},
            {"Belge Adı": "MSB Pano Termografik Test Raporu", "Kategori": "Kestirimci Bakım", "Duzenleyen": "Enspektör Servis", "SonTarih": "2026-09-30"}
        ]
        st.dataframe(pd.DataFrame(sertifika_listesi), use_container_width=True)

    # TAB 3: SATINALMA
    with tab3:
        st.subheader(f"🛒 {gemi_adi} - Elektrik Satınalma Paneli")
        req_data = [
            {"Req No": "REQ-2026-081", "Malzeme": secili_gemi_bilgi['Malzeme'], "Miktar": "1 Adet", "Acillik": "🔴 Acil", "Tedarik Durumu": "📦 Sipariş Edildi", "Liman": "Tuzla Tersanesi"}
        ]
        st.dataframe(pd.DataFrame(req_data), use_container_width=True)

    # TAB 4: ŞEMALAR
    with tab4:
        st.subheader(f"📖 {gemi_adi} - Elektrik Projeleri ve Kılavuzlar")
        st.markdown("### 🔌 Tek Hat Şemaları (Single Line Diagrams)")
        semalar = [
            {"Doküman": "440V MSB Main Switchboard Diagram", "Format": "PDF", "Boyut": "12.4 MB"},
            {"Doküman": "220V Emergency Switchboard (ESB)", "Format": "PDF", "Boyut": "8.1 MB"},
            {"Doküman": "Dümen Makinesi Besleme Şeması", "Format": "PDF", "Boyut": "15.2 MB"}
        ]
        st.dataframe(pd.DataFrame(semalar), use_container_width=True)
        st.download_button("📥 Tüm Elektrik Şemalarını İndir (ZIP)", b"Demo_ZIP_Data", f"{gemi_adi}_Elektrik_Projesi.zip")

    # TAB 5: ETO EĞİTİM & PSC
    with tab5:
        st.subheader("🎓 ETO Eğitim & PSC Mülakat Hazırlık Paneli")
        st.info(" Paris MOU / Tokyo MOU Denetimi Öncesi Elektrik Soru Bankası")
        q1 = st.radio("1. Acil Durum Jeneratörünün manuel olarak çalıştırılmasında ilk adım nedir?", [
            "A) Akü voltajı ve yakıt vanasının kontrolü",
            "B) Ana tablo şalterini açmak",
            "C) Sintine pompasını çalıştırmak"
        ])
        if st.button("Cevabı Doğrula"):
            if q1.startswith("A"):
                st.success("✅ Doğru Cevap!")
            else:
                st.error("❌ Yanlış cevap.")

    # TAB 6: ELEKTRİK ZABİTLERİ
    with tab6:
        st.subheader("👨‍✈️ Gemideki Görevli Elektrik Zabiti")
        st.markdown(f"**Görevli ETO:** {secili_gemi_bilgi['ETO']}")
        st.markdown(f"**Katılış Tarihi:** {secili_gemi_bilgi['Giris']}")

    # TAB 7: ARIZA KAYDI
    with tab7:
        st.subheader(f"📋 {gemi_adi} - Arıza Kaydı ve Giriş Formu")
        col1, col2 = st.columns(2)
        with col1:
            ekipman = st.selectbox("Aksam / Ekipman", ["Ana Dağıtım Panosu (MSB)", "Acil Durum Panosu (ESB)", "1 No'lu Jeneratör (DG1)"])
            durum = st.radio("Risk Derecesi", ["🔴 Kritik", "🟡 Önemli", "🟢 Uygun"])
        with col2:
            aciklama = st.text_area("Arıza Açıklaması", value=secili_gemi_bilgi['Arıza'])
        if st.button("Arıza Kaydını Güncelle / Ekle"):
            st.session_state.bulgular.append({"Tarih": str(tarih), "Gemi": gemi_adi, "Ekipman": ekipman, "Risk Durumu": durum, "Açıklama": aciklama})
            st.success("Arıza veritabanına kaydedildi.")

    # TAB 8: MEGGER TESTİ
    with tab8:
        st.subheader(f"⚡ {gemi_adi} - İzolasyon Direnci (Megger) Ölçümü")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            megger_ekipman = st.selectbox("Ölçüm Yapılan Ekipman", ["DG1 Alternatör Sargıları", "MSB 440V Busbar", "Güverte Aydınlatma Panosu"])
        with m_col2:
            megger_deger = st.number_input("Ölçülen İzolasyon Değeri (MΩ)", value=5.0)
        if megger_deger >= 5.0:
            st.success("🟢 İZOLASYON SAĞLIKLI")
        else:
            st.error("🔴 KRİTİK DÜŞÜK İZOLASYON (Düzeltici Faaliyet Gerekli)")

    # TAB 9: PSC CHECKLIST
    with tab9:
        st.subheader(f"📝 {gemi_adi} - PSC Kontrol Listesi")
        chk1 = st.checkbox("1. Acil Durum Jeneratörü otomatik ve manuel start alıyor.")
        chk2 = st.checkbox("2. Seyir fenerleri panosu sesli ve görsel alarm veriyor.")
        chk3 = st.checkbox("3. Acil aydınlatmalar ve akü grubu sağlam.")

    # TAB 10: YEDEK PARÇA
    with tab10:
        st.subheader("📦 Kritik Elektrik Yedek Parça Stok Durumu")
        yedek_data = [
            {"Parça Adı": "AVR MX321", "Stok": "1 Adet", "Durum": "🟢 Yeterli"},
            {"Parça Adı": "ACB Açma Bobini 220V", "Stok": "2 Adet", "Durum": "🟢 Yeterli"},
            {"Parça Adı": "Seyir Feneri LED Ampul", "Stok": "5 Adet", "Durum": "🟡 Takipte"}
        ]
        st.dataframe(pd.DataFrame(yedek_data), use_container_width=True)

    # TAB 11: RAPORLAMA
    with tab11:
        st.subheader("📊 Enspeksiyon Raporunu İndir")
        if len(st.session_state.bulgular) > 0:
            df_b = pd.DataFrame(st.session_state.bulgular)
            st.dataframe(df_b, use_container_width=True)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_b.to_excel(writer, index=False, sheet_name='Bulgular')
            st.download_button("📥 Excel Formatında Raporu İndir", buffer.getvalue(), f"{gemi_adi}_Rapor.xlsx")
        else:
            st.info("Henüz yeni eklenmiş bir arıza/bulgu kaydı yok. Yukarıdaki formları kullanarak veri ekleyebilirsiniz.")
