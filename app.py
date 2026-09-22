import streamlit as st
import pandas as pd
import datetime
import io
from fpdf import FPDF

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Filo Yönetim Paneli")
st.markdown("MarineTraffic entegrasyonu, sertifika/sürvey takibi, satınalma, teknik doküman kütüphanesi, ETO eğitim/PSC simülasyonu, megger kayıtları ve PDF/Excel raporlama paneli.")

# TTS Ships Filo Verileri
tts_fleet_data = [
    {"Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Konteyner", "DWT": "27254", "GRT": "23633", "Bayrak": "Panama", "Yıl": "2004", "LOA": "191,10 m", "Durum": "🟢 Uygun", "ETO": "Ahmet YILMAZ", "Giris": "2026-06-15", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet"},
    {"Gemi": "M/T AY YILDIZI", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Kritik", "ETO": "Mehmet KAYA", "Giris": "2026-04-01", "KontratAy": 6, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet"},
    {"Gemi": "M/T KUZEY YILDIZ II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", "Bayrak": "Malta", "Yıl": "2020", "LOA": "108,10 m", "Durum": "🟡 Takipte", "ETO": "Caner DEMİR", "Giris": "2026-08-10", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner"},
    {"Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1285", "Bayrak": "Liberya", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Emre ŞAHİN", "Giris": "2026-07-20", "KontratAy": 5, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre"},
    {"Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Kargo", "DWT": "1300", "GRT": "1281", "Bayrak": "Liberya", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Uygun", "ETO": "Burak ÇELİK", "Giris": "2026-05-12", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak"},
    {"Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Dökme Yük Gemisi", "DWT": "60054", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟢 Uygun", "ETO": "Oğuz ÖZTÜRK", "Giris": "2026-06-01", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz"},
    {"Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Dökme Yük Gemisi", "DWT": "60594", "GRT": "4848", "Bayrak": "Panama", "Yıl": "1991", "LOA": "138,40 m", "Durum": "🟡 Takipte", "ETO": "Serkan AYDIN", "Giris": "2026-04-15", "KontratAy": 6, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan"},
    {"Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Dökme Yük Gemisi", "DWT": "75002,58", "GRT": "41074", "Bayrak": "Liberya", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Kritik", "ETO": "Murat ASLAN", "Giris": "2026-03-10", "KontratAy": 6, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat"},
    {"Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Dökme Yük Gemisi", "DWT": "78128", "GRT": "41718", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "224,90 m", "Durum": "🟢 Uygun", "ETO": "Volkan YILDIZ", "Giris": "2026-07-01", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan"},
    {"Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Dökme Yük Gemisi", "DWT": "52428", "GRT": "30174", "Bayrak": "Panama", "Yıl": "2001", "LOA": "189,99 m", "Durum": "🟢 Uygun", "ETO": "Hasan ERDOĞAN", "Giris": "2026-08-01", "KontratAy": 5, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan"},
    {"Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Dökme Yük Gemisi", "DWT": "80888", "GRT": "44025", "Bayrak": "Liberya", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Ali ÖZKAN", "Giris": "2026-06-20", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali"},
    {"Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Dökme Yük Gemisi", "DWT": "79520", "GRT": "43501", "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Uygun", "ETO": "Tolga TEKİN", "Giris": "2026-07-10", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga"},
    {"Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "Genel Kargo", "DWT": "8300", "GRT": "6641", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Onur KOÇ", "Giris": "2026-08-15", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur"},
    {"Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "Genel Kargo", "DWT": "8330", "GRT": "6732", "Bayrak": "Liberya", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Uygun", "ETO": "Kaan YILMAZ", "Giris": "2026-07-25", "KontratAy": 4, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan"},
    {"Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Canlı Hayvanlar", "DWT": "12900", "GRT": "38988", "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185,82 m", "Durum": "🟡 Takipte", "ETO": "Zafer GÜNEŞ", "Giris": "2026-05-01", "KontratAy": 5, "Foto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer"}
]

df_fleet = pd.DataFrame(tts_fleet_data)
gemi_listesi = df_fleet["Gemi"].tolist()

if "bulgular" not in st.session_state:
    st.session_state.bulgular = []

# YAN MENÜ (SIDEBAR)
st.sidebar.header("⚡ TTS Enspektör Paneli")

# 1. ENSPEKTÖR BİLGİSİ
st.sidebar.subheader("👨‍💼 Elektrik Enspektörü")
st.sidebar.info("Ceyhun ÜCELEHAN")

# 2. GEMİ SEÇİMİ
gemi_adi = st.sidebar.selectbox("Gemi Seçiniz", gemi_listesi)
secili_gemi_bilgi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

# GEMİ BİLGİLERİ KÜNYESİ
st.sidebar.markdown(f"""
* **IMO No:** {secili_gemi_bilgi['IMO']}
* **Gemi Tipi:** {secili_gemi_bilgi['Tip']}
* **Bayrak:** {secili_gemi_bilgi['Bayrak']}
* **DWT / GRT:** {secili_gemi_bilgi['DWT']} / {secili_gemi_bilgi['GRT']}
* **Boy (LOA):** {secili_gemi_bilgi['LOA']}
* **İnşa Yılı:** {secili_gemi_bilgi['Yıl']}
* **Elektrik Durumu:** {secili_gemi_bilgi['Durum']}
""")

st.sidebar.divider()

# 3. GEMİDEKİ ELEKTRİK ZABİTİ (ETO) VE KONTRAT BİLGİLERİ
st.sidebar.subheader("👨‍✈️ Gemideki Elektrik Zabiti (ETO)")
st.sidebar.image(secili_gemi_bilgi['Foto'], caption=f"ETO: {secili_gemi_bilgi['ETO']}", width=150)

# TARİH DÖNÜŞÜMÜ VE HESAPLAMA
katilis_tarihi = datetime.datetime.strptime(str(secili_gemi_bilgi['Giris']), "%Y-%m-%d").date()
kontrat_ay = int(secili_gemi_bilgi['KontratAy'])
bitis_tarihi = katilis_tarihi + datetime.timedelta(days=kontrat_ay * 30)
bugun = datetime.date.today()

toplam_gun = (bitis_tarihi - katilis_tarihi).days
gecen_gun = (bugun - katilis_tarihi).days
kalan_gun = (bitis_tarihi - bugun).days

if kalan_gun <= 0:
    kalan_gun = 0
    durum_renk = "🔴 Kontrat Doldu"
    oran = 1.0
elif kalan_gun <= 30:
    durum_renk = "🟡 Değişim Zamanı Yakın"
    oran = min(1.0, max(0.0, gecen_gun / toplam_gun))
else:
    durum_renk = "🟢 Kontrat Devam Ediyor"
    oran = min(1.0, max(0.0, gecen_gun / toplam_gun))

st.sidebar.markdown("### ⏳ Kontrat Durumu")
st.sidebar.progress(oran)

st.sidebar.markdown(f"""
* **Katılış Tarihi:** `{katilis_tarihi.strftime('%d.%m.%Y')}`
* **Kontrat Sonu:** `{bitis_tarihi.strftime('%d.%m.%Y')}`
* **Süre / Kalan:** `{kontrat_ay} Ay` / **{kalan_gun} Gün**
* **Durum:** {durum_renk}
""")

tarih = st.sidebar.date_input("Denetim Tarihi", datetime.date.today())

st.sidebar.divider()

# ANA SEKMELER
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
    st.subheader(f"⚓ {gemi_adi} (IMO: {secili_gemi_bilgi['IMO']}) - Canlı Takip")
    col_mt1, col_mt2 = st.columns([2, 1])
    with col_mt1:
        st.info(f"📍 **{gemi_adi}** gemisinin canlı AIS konumunu MarineTraffic üzerinde görüntüleyin.")
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi_bilgi['IMO']}"
        st.link_button(f"🔴 {gemi_adi} Canlı MarineTraffic Haritasını Aç", mt_link, type="primary", use_container_width=True)
    with col_mt2:
        st.metric("Seçili Gemi IMO", secili_gemi_bilgi['IMO'])
        st.metric("Gemi Tipi", secili_gemi_bilgi['Tip'])
        st.metric("Elektrik Durumu", secili_gemi_bilgi['Durum'])

# TAB 2: SERTİFİKA & CLASS SÜRVEY TAKİP
with tab2:
    st.subheader(f"📜 {gemi_adi} - Sertifika & Yasal Belge / Sürvey Takip Paneli")
    
    sertifika_listesi = [
        {"Belge Adı": "Annual Electrical Class Survey", "Kategori": "Class Sürvey", "Duzenleyen": "Class / RINA", "SonTarih": "2026-10-15"},
        {"Belge Adı": "Seyir Fenerleri Tip Onay Sertifikası", "Kategori": "Ekipman Sertifikası", "Duzenleyen": "Glamox / DNV", "SonTarih": "2026-11-20"},
        {"Belge Adı": "Megger & Ölçüm Cihazları Kalibrasyonu", "Kategori": "Kalibrasyon", "Duzenleyen": "Akredite Laboratuvar", "SonTarih": "2026-10-02"},
        {"Belge Adı": "Filika Motoru & Akü Grubu Test Raporu", "Kategori": "Güvenlik / SOLAS", "Duzenleyen": "Yetkili Servis", "SonTarih": "2027-04-10"},
        {"Belge Adı": "Ana Dağıtım Panosu (MSB) Termografik Test", "Kategori": "Kestirimci Bakım", "Duzenleyen": "Enspektör / Servis", "SonTarih": "2026-09-30"}
    ]

    islenmis_sertifikalar = []
    bugun_tarih = datetime.date.today()
    for item in sertifika_listesi:
        son_t = datetime.datetime.strptime(item["SonTarih"], "%Y-%m-%d").date()
        k_gun = (son_t - bugun_tarih).days
        durum_etiket = "🔴 KRİTİK (<30 Gün)" if k_gun <= 30 else ("🟡 TAKİPTE (30-90 Gün)" if k_gun <= 90 else "🟢 UYGUN (>90 Gün)")
        islenmis_sertifikalar.append({
            "Durum Alarmı": durum_etiket,
            "Belge / Sürvey Adı": item["Belge Adı"],
            "Kategori": item["Kategori"],
            "Düzenleyen Kurum": item["Duzenleyen"],
            "Son Geçerlilik Tarihi": son_t.strftime('%d.%m.%Y'),
            "Kalan Süre": f"{k_gun} Gün" if k_gun >= 0 else "🔴 SÜRESİ DOLDU"
        })
    st.dataframe(pd.DataFrame(islenmis_sertifikalar), use_container_width=True)

# TAB 3: SATINALMA & TEDARİK
with tab3:
    st.subheader(f"🛒 {gemi_adi} - Elektrik Satınalma & Tedarikçi Paneli")
    req_data = [
        {"Req No": "REQ-2026-081", "Malzeme": "DG1 AVR MX321", "Miktar": "1 Adet", "Acillik": "🔴 Acil (PSC Riski)", "Tedarik Durumu": "📦 Sipariş Edildi", "Liman": "Tuzla Tersanesi", "Gemi Onayı": "⏳ Teslimat Bekleniyor"},
        {"Req No": "REQ-2026-074", "Malzeme": "Seyir Feneri LED Ampul Seti", "Miktar": "10 Adet", "Acillik": "🔴 Acil (SOLAS)", "Tedarik Durumu": "✅ Teslim Edildi", "Liman": "Rotterdam", "Gemi Onayı": "✅ Gemide Onaylandı"}
    ]
    st.dataframe(pd.DataFrame(req_data), use_container_width=True)

# TAB 4: ŞEMALAR & TEKNİK DOKÜMAN KÜTÜPHANESİ (YENİ)
with tab4:
    st.subheader(f"📖 {gemi_adi} - Elektrik Şemaları & Teknik Doküman Kütüphanesi")
    st.markdown("Geminin Dijital İkizi (Digital Twin), Tek Hat Şemaları (Single Line Diagram) ve Ekipman Kılavuzları:")

    col_doc1, col_doc2 = st.columns([1, 1])
    
    with col_doc1:
        st.markdown("### 🔌 Tek Hat Şemaları (Single Line Diagrams)")
        semalar = [
            {"Doküman": "440V MSB Main Switchboard Diagram", "Format": "PDF / CAD", "Boyut": "12.4 MB", "Revizyon": "Rev.3 (2025)"},
            {"Doküman": "220V Emergency Switchboard (ESB)", "Format": "PDF", "Boyut": "8.1 MB", "Revizyon": "Rev.2 (2024)"},
            {"Doküman": "Navigasyon & Seyir Fenerleri Dağıtım Şeması", "Format": "PDF", "Boyut": "4.5 MB", "Revizyon": "Rev.1 (2024)"},
            {"Doküman": "Dümen Makinesi Besleme & Kontrol Şeması", "Format": "PDF / CAD", "Boyut": "15.2 MB", "Revizyon": "Rev.4 (2026)"}
        ]
        st.dataframe(pd.DataFrame(semalar), use_container_width=True)
        st.download_button("📥 Seçili Gemi Tüm Elektrik Projelerini (ZIP) İndir", b"Demo_ZIP_Data", "Gemi_Elektrik_Projesi.zip")

    with col_doc2:
        st.markdown("### 🛠️ Ekipman Manuel Veritabanı & Arıza Arama (Troubleshooting)")
        manuels = [
            {"Ekipman / Modül": "Stamford MX321 AVR Manual", "Konu": "Voltaj Ayarı & Diyot Testi", "Hızlı Rehber": "🔍 Voltaj Düşüklüğü Arıza Arama"},
            {"Ekipman / Modül": "Schneider Masterpact ACB Şalter", "Konu": "Açma/Kapama Bobini & Trip Testi", "Hızlı Rehber": "🔍 ACB Trip Vermesi & Kurmama Arızası"},
            {"Ekipman / Modül": "Siemens S7-300 PLC Modülleri", "Konu": "Giriş/Çıkış (I/O) Kart Şemaları", "Hızlı Rehber": "🔍 SF / BF LED Hatası Teşhisi"},
            {"Ekipman / Modül": "Deif AGC-4 Jeneratör Senkronizasyon", "Konu": "Yük Paylaşımı & Otomatik Start", "Hızlı Rehber": "🔍 Jeneratör Senkron Olmama Nedeni"}
        ]
        st.dataframe(pd.DataFrame(manuels), use_container_width=True)

    st.divider()

    # HIZLI ARIZA ARAMA (TROUBLESHOOTING REHBERİ)
    st.subheader("🔍 Hızlı Arıza Arama (Troubleshooting) Arama Motoru")
    ariza_sorgu = st.selectbox("Arıza Belirtisini Seçiniz:", [
        "Jeneratör Voltaj Üretmiyor (0V)",
        "MSB Şalteri (ACB) Kapamıyor / Geri Atıyor",
        "Pano İzolasyon Alarmı Çalıyor (Megger Düşük)",
        "Seyir Fenerleri Panosu Sesli Alarm Veriyor"
    ])

    if ariza_sorgu == "Jeneratör Voltaj Üretmiyor (0V)":
        st.warning("⚠️ **Olası Nedenler & Çözüm Adımları:**\n1. AVR Sigortasını ve artık mıknatısiyet (Residual Voltage) değerini kontrol edin.\n2. Döner diyot tablosunu (Rotating Diodes) multimetre ile diyot kademesinde ölçün.\n3. İkaz sargıları (Exciter Winding) direnç değerini ölçün.")
    elif ariza_sorgu == "MSB Şalteri (ACB) Kapamıyor / Geri Atıyor":
        st.warning("⚠️ **Olası Nedenler & Çözüm Adımları:**\n1. Kurma motorunu (Undervoltage Release) kontrol edin.\n2. Şalter üzerindeki Trip göstergesini resetleyin.\n3. Ters güç (Reverse Power) veya aşırı akım rölesinin devre dışı kaldığından emin olun.")

# TAB 5: ETO EĞİTİM & PSC MÜLAKAT HAZIRLIK PANENLİ (YENİ)
with tab5:
    st.subheader("🎓 ETO Eğitim & PSC Mülakat Hazırlık Paneli")
    st.markdown("Paris MOU / Tokyo MOU Liman Devleti Kontrolleri (PSC) Öncesi ETO Yetkinlik ve Mülakat Testleri:")

    col_t1, col_t2 = st.columns([1, 1])

    with col_t1:
        st.markdown("### 📝 PSC Sık Sorulan Sorular & Hazırlık Testi")
        st.info("🎯 **Test Senaryosu:** Paris MOU Enspektörü Geminize Geldiğinde Sorulacak Elektrik Soruları")

        q1 = st.radio("1. PSC Müfettişi Acil Durum Jeneratörünün manuel olarak çalıştırılmasını istedi. İlk olarak ne kontrol edilmelidir?", [
            "A) Akü voltajı ve yakıt valfi konumu",
            "B) Filika motoru start butonu",
            "C) Sintine pompası şalteri"
        ])

        q2 = st.radio("2. 440V Ana Dağıtım Panosunda topraklama hatası (Earth Fault) tespit edildi. Sınırlı sürede arıza nasıl izole edilir?", [
            "A) Tüm gemi elektriğini hemen keserim.",
            "B) Feeder şalterlerini sırayla tek tek açıp kapatarak hangi devreden geldiğini bulurum.",
            "C) İzolasyon alarmının sesini kapatırım."
        ])

        if st.button("Test Cevaplarını Kontrol Et"):
            if q1.startswith("A") and q2.startswith("B"):
                st.success("🎉 Tebrikler! 100/100. PSC Denetimine Hazırsınız.")
            else:
                st.error("❌ Eksik cevaplar var. Lütfen PSC Hazırlık Dokümanlarını inceleyiniz.")

    with col_t2:
        st.markdown("### 🎮 İnteraktif Arıza Çözme Simülasyonu")
        st.subheader("🚨 Senaryo: Seyir Halinde Ana Pano İzolasyonu 0.1 MΩ Düşmesi")
        st.write("**Olay:** Gemi gece seyir halindeyken MSB 440V panosu 'Low Insulation' alarmı verdi.")

        adim1 = st.selectbox("1. Adım: İlk Müdahaleniz Ne Olmalıdır?", [
            "Kaptan ve Başmühendise haber verip, makine dairesindeki kritik olmayan tüketicileri (Galley/Mutfak, Havalandırma) ayırmak.",
            "Jeneratörü durdurmak.",
            "Hiçbir şey yapmadan beklemek."
        ])

        adim2 = st.selectbox("2. Adım: Nem kaynaklı kaçak şüphesi varsa ne kontrol edilir?", [
            "Güverte aydınlatma armatürleri ve ambar havalandırma fanları.",
            "Gemi telsiz cihazı.",
            "Kamaraların klimaları."
        ])

        if st.button("Simülasyon Sonucunu Göster"):
            st.success("✅ **Simülasyon Başarılı:** Doğru teşhis adımları uygulandı. Arıza emniyetli şekilde izole edildi.")

# TAB 6: ELEKTRİK ZABİTLERİ (ETO)
with tab6:
    st.subheader("👨‍✈️ Şirket Elektrik Zabitleri (ETO) & Performans Değerlendirme Tablosu")
    eto_gemide_listesi = []
    for item in tts_fleet_data:
        k_tarih = datetime.datetime.strptime(item['Giris'], "%Y-%m-%d").date()
        b_tarih = k_tarih + datetime.timedelta(days=int(item['KontratAy']) * 30)
        k_gun = (b_tarih - datetime.date.today()).days
        if k_gun < 0: k_gun = 0
        eto_gemide_listesi.append({
            "Durum": "🚢 Gemide", "Adı Soyadı": item['ETO'], "Görevli Olduğu Gemi": item['Gemi'],
            "Katılış Tarihi": k_tarih.strftime('%d.%m.%Y'), "Kontrat Sonu": b_tarih.strftime('%d.%m.%Y'),
            "Kalan Gün": f"{k_gun} Gün", "Performans Skoru": "⭐ 4.8 / 5.0"
        })
    st.dataframe(pd.DataFrame(eto_gemide_listesi), use_container_width=True)

# TAB 7: ARIZA KAYDI
with tab7:
    st.subheader(f"🛠️ {gemi_adi} - Elektrik Arıza Kaydı Formu")
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", ["Ana Dağıtım Panosu (MSB)", "Acil Durum Panosu (ESB)", "1 No'lu Jeneratör (DG1)"])
        kategori = st.selectbox("Kategori", ["İzolasyon (Megger) Düşüklüğü", "AVR / Voltaj Düzensizliği", "ACB / Şalter Trip"])
        durum = st.radio("Risk Derecesi", ["🔴 Kritik (Class / PSC Riski)", "🟡 Önemli", "🟢 Uygun"])
    with col2:
        aciklama = st.text_area("Arıza Açıklaması", "MSB 440V bara izolasyon değeri düşük.")
    if st.button("Kaydı Veritabanına Ekle"):
        st.session_state.bulgular.append({"Tarih": str(tarih), "Gemi": gemi_adi, "Ekipman": ekipman, "Risk Durumu": durum, "Açıklama": aciklama})
        st.success("Bulgu eklendi!")

# TAB 8: MEGGER TESTİ
with tab8:
    st.subheader(f"⚡ {gemi_adi} - İzolasyon Direnci (Megger) Ölçümü")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        megger_ekipman = st.selectbox("Ölçüm Yapılan Ekipman", ["DG1 Alternatör Sargıları", "MSB 440V Busbar"])
    with m_col2:
        megger_deger = st.number_input("Ölçülen İzolasyon Değeri (MΩ)", value=5.0)
    with m_col3:
        st.success("🟢 İZOLASYON SAĞLIKLI") if megger_deger >= 5.0 else st.error("🔴 KRİTİK DÜŞÜK!")

# TAB 9: PSC CHECKLIST
with tab9:
    st.subheader(f"📝 {gemi_adi} - PSC Kontrol Listesi")
    chk1 = st.checkbox("1. Acil Durum Jeneratörü otomatik start alıyor.")
    chk2 = st.checkbox("2. Navigasyon fenerleri panosu alarm veriyor.")

# TAB 10: YEDEK PARÇA TAKİBİ
with tab10:
    st.subheader("📦 Kritik Elektrik Yedek Parça Stok Durumu")
    yedek_data = [{"Parça Adı": "AVR MX321", "Stok Adedi": 2, "Durum": "🟢 Yeterli"}]
    st.dataframe(pd.DataFrame(yedek_data), use_container_width=True)

# TAB 11: RAPORLAMA & PDF/EXCEL
with tab11:
    st.subheader("📊 Filo Denetim Raporlama ve Dışa Aktarma")
    if len(st.session_state.bulgular) > 0:
        df_bulgu = pd.DataFrame(st.session_state.bulgular)
        st.dataframe(df_bulgu, use_container_width=True)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_bulgu.to_excel(writer, index=False, sheet_name='Bulgular')
        st.download_button("📥 Excel Raporu İndir", buffer.getvalue(), f"Rapor_{tarih}.xlsx")
    else:
        st.warning("Henüz kayıt bulunmamaktadır.")
