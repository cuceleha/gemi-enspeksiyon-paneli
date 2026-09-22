import streamlit as st
import pandas as pd
import datetime
import io
from fpdf import FPDF

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Satınalma Paneli",
    page_icon="⚡",
    layout="wide"
)

# Başlık ve Açıklama
st.title("⚡ TTS Ships - Gemi Elektrik Enspeksiyon & Satınalma Paneli")
st.markdown("MarineTraffic entegrasyonu, sertifika/sürvey takibi, elektrik satınalma & tedarik yönetimi, megger kayıtları, PSC kontrol listesi ve PDF/Excel raporlama paneli.")

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

# KONTRAT BİLGİLERİ TABLOSU
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🌐 Canlı Takip", 
    "📜 Sertifika & Class Sürvey",
    "🛒 Satınalma & Tedarikçi",
    "👨‍✈️ Elektrik Zabitleri (ETO)",
    "📋 Arıza Kaydı & Fotoğraf", 
    "⚡ Megger (İzolasyon)",
    "📝 PSC Kontrol Listesi",
    "📦 Elektrik Yedek Parça",
    "📊 Raporlama & PDF/Excel"
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
    st.markdown("Class (RINA/NKK/BV/ABS), Bayrak Devleti ve Yasal Elektrik Ekipmanı Sertifikalarının Son Kullanma Tarihleri:")

    sertifika_listesi = [
        {"Belge Adı": "Annual Electrical Class Survey", "Kategori": "Class Sürvey", "Duzenleyen": "Class / RINA", "SonTarih": "2026-10-15"},
        {"Belge Adı": "Seyir Fenerleri Tip Onay Sertifikası", "Kategori": "Ekipman Sertifikası", "Duzenleyen": "Glamox / DNV", "SonTarih": "2026-11-20"},
        {"Belge Adı": "Megger & Ölçüm Cihazları Kalibrasyonu", "Kategori": "Kalibrasyon", "Duzenleyen": "Akredite Laboratuvar", "SonTarih": "2026-10-02"},
        {"Belge Adı": "Filika Motoru & Akü Grubu Test Raporu", "Kategori": "Güvenlik / SOLAS", "Duzenleyen": "Yetkili Servis", "SonTarih": "2027-04-10"},
        {"Belge Adı": "Ana Dağıtım Panosu (MSB) Termografik Test", "Kategori": "Kestirimci Bakım", "Duzenleyen": "Enspektör / Servis", "SonTarih": "2026-09-30"},
        {"Belge Adı": "Gemi İçi Telsiz & GMDSS Akü Sertifikası", "Kategori": "Bayrak / Class", "Duzenleyen": "Radio Surveyor", "SonTarih": "2027-01-15"},
        {"Belge Adı": "Körleme / İzolasyon Test Onay Belgesi", "Kategori": "Güvenlik", "Duzenleyen": "Tersane / Class", "SonTarih": "2028-06-01"},
    ]

    islenmis_sertifikalar = []
    bugun_tarih = datetime.date.today()

    kritik_sayisi = 0
    takip_sayisi = 0
    uygun_sayisi = 0

    for item in sertifika_listesi:
        son_t = datetime.datetime.strptime(item["SonTarih"], "%Y-%m-%d").date()
        k_gun = (son_t - bugun_tarih).days

        if k_gun <= 30:
            durum_etiket = "🔴 KRİTİK (<30 Gün)"
            kritik_sayisi += 1
        elif k_gun <= 90:
            durum_etiket = "🟡 TAKİPTE (30-90 Gün)"
            takip_sayisi += 1
        else:
            durum_etiket = "🟢 UYGUN (>90 Gün)"
            uygun_sayisi += 1

        islenmis_sertifikalar.append({
            "Durum Alarmı": durum_etiket,
            "Belge / Sürvey Adı": item["Belge Adı"],
            "Kategori": item["Kategori"],
            "Düzenleyen Kurum": item["Duzenleyen"],
            "Son Geçerlilik Tarihi": son_t.strftime('%d.%m.%Y'),
            "Kalan Süre": f"{k_gun} Gün" if k_gun >= 0 else "🔴 SÜRESİ DOLDU"
        })

    df_cert = pd.DataFrame(islenmis_sertifikalar)

    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Toplam Sertifika / Sürvey", len(df_cert))
    c_m2.metric("🔴 Kritik (Son 30 Gün)", kritik_sayisi)
    c_m3.metric("🟡 Yaklaşan (30-90 Gün)", takip_sayisi)
    c_m4.metric("🟢 Geçerli (>90 Gün)", uygun_sayisi)

    st.divider()

    with st.expander("➕ Yeni Sertifika / Sürvey Kaydı Ekle"):
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            y_belge = st.text_input("Belge / Sürvey Adı")
            y_kat = st.selectbox("Kategori", ["Class Sürvey", "Ekipman Sertifikası", "Kalibrasyon", "Güvenlik / SOLAS", "Bayrak / Class"])
        with col_c2:
            y_kurum = st.text_input("Düzenleyen Kurum / Servis")
            y_tarih = st.date_input("Son Geçerlilik Tarihi", datetime.date.today() + datetime.timedelta(days=365))
        with col_c3:
            st.write(" ")
            st.write(" ")
            if st.button("Sertifikayı Kaydet", use_container_width=True):
                st.success(f"'{y_belge}' sertifikası veritabanına eklendi!")

    st.dataframe(df_cert, use_container_width=True)

# TAB 3: SATINALMA & TEDARİKÇİ PANENLİ (YENİ SEKMELER)
with tab3:
    st.subheader(f"🛒 {gemi_adi} - Elektrik Satınalma, Talep & Tedarik Takip Paneli")
    st.markdown("Gemideki ETO tarafından talep edilen elektrik malzemeleri, acillik seviyeleri, tedarik yeri ve teslimat durumları:")

    # ÖRNEK SATINALMA TALEP VERİLERİ
    req_data = [
        {
            "Req No": "REQ-2026-081",
            "Gemi": gemi_adi,
            "Talep Eden": f"ETO ({secili_gemi_bilgi['ETO']})",
            "Malzeme / Parça Adı": "DG1 Alternatör Otomatik Voltaj Regülatörü (AVR MX321)",
            "Miktar": "1 Adet",
            "Acillik / Risk": "🔴 Acil (Seyir Emniyeti / PSC)",
            "Tedarik Durumu": "📦 Sipariş Edildi",
            "Tedarik Edilecek Liman": "Tuzla Tersanesi / Türkiye",
            "Tedarikçi Firma": "MarPower Electrical B.V.",
            "Gemi Onayı / Teslimat": "⏳ Teslimat Bekleniyor"
        },
        {
            "Req No": "REQ-2026-074",
            "Gemi": gemi_adi,
            "Talep Eden": f"ETO ({secili_gemi_bilgi['ETO']})",
            "Malzeme / Parça Adı": "Seyir Fenerleri LED Ampul Seti (24V DC - Glamox)",
            "Miktar": "10 Adet",
            "Acillik / Risk": "🔴 Acil (SOLAS / PSC Riski)",
            "Tedarik Durumu": "✅ Teslim Edildi",
            "Tedarik Edilecek Liman": "Rotterdam / Hollanda",
            "Tedarikçi Firma": "Glamox Marine Europe",
            "Gemi Onayı / Teslimat": "✅ Gemide Onaylandı (ETO)"
        },
        {
            "Req No": "REQ-2026-068",
            "Gemi": gemi_adi,
            "Talep Eden": f"ETO ({secili_gemi_bilgi['ETO']})",
            "Malzeme / Parça Adı": "Fluke 1587 FC İzolasyon Multimetresi (Megger)",
            "Miktar": "1 Set",
            "Acillik / Risk": "🟡 Orta (Bakım & Kalibrasyon)",
            "Tedarik Durumu": "📋 Teklif Aşamasında",
            "Tedarik Edilecek Liman": "Singapur Limanı",
            "Tedarikçi Firma": "Teklifler Değerlendiriliyor",
            "Gemi Onayı / Teslimat": "⏳ Tedarik Aşamasında"
        },
        {
            "Req No": "REQ-2026-052",
            "Gemi": gemi_adi,
            "Talep Eden": f"ETO ({secili_gemi_bilgi['ETO']})",
            "Malzeme / Parça Adı": "24V 200Ah Jel Akü Grubu (GMDSS Telsiz İçin)",
            "Miktar": "4 Adet",
            "Acillik / Risk": "🟡 Orta (Süresi Yaklaşıyor)",
            "Tedarik Durumu": "📦 Sipariş Edildi",
            "Tedarik Edilecek Liman": "Pire Limanı / Yunanistan",
            "Tedarikçi Firma": "Hellas Marine Batteries",
            "Gemi Onayı / Teslimat": "⏳ Yolda / Acente İle Sevk"
        },
        {
            "Req No": "REQ-2026-041",
            "Gemi": gemi_adi,
            "Talep Eden": f"ETO ({secili_gemi_bilgi['ETO']})",
            "Malzeme / Parça Adı": "Kablo Rakorları (Gland) Seti & Isı Büzüşmeli Makaron",
            "Miktar": "1 Kutu",
            "Acillik / Risk": "🟢 Düşük (Stok Tamamlama)",
            "Tedarik Durumu": "✅ Teslim Edildi",
            "Tedarik Edilecek Liman": "İzmir Limanı",
            "Tedarikçi Firma": "Ege Elektrik Denizcilik",
            "Gemi Onayı / Teslimat": "✅ Gemide Onaylandı (ETO)"
        }
    ]

    df_req = pd.DataFrame(req_data)

    # ÖZET METRİKLER
    p_m1, p_m2, p_m3, p_m4 = st.columns(4)
    p_m1.metric("Toplam Malzeme Talebi", len(df_req))
    p_m2.metric("🔴 Acil / PSC Riski", len(df_req[df_req["Acillik / Risk"].str.contains("🔴")]))
    p_m3.metric("⏳ Tedarik Edilecek / Yolda", len(df_req[df_req["Tedarik Durumu"].str.contains("Sipariş|Teklif")]))
    p_m4.metric("✅ Gemi Onaylı (Teslim)", len(df_req[df_req["Gemi Onayı / Teslimat"].str.contains("✅")]))

    st.divider()

    # YENİ MALZEME TALEBİ OLUŞTURMA FORMU
    with st.expander("➕ Gemiden / Enspektörden Yeni Malzeme Talebi (Requisition) Ekle"):
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            r_parca = st.text_input("Malzeme / Parça Adı & Kodu")
            r_miktar = st.text_input("Miktar (Adet/Set)", value="1 Adet")
            r_acil = st.selectbox("Acillik & Risk Seviyesi", [
                "🔴 Acil (Seyir Emniyeti / PSC / Class Riski)",
                "🟡 Orta (Periyodik Bakım / Süresi Yaklaşan)",
                "🟢 Düşük (Genel Stok Tamamlama)"
            ])
        with col_r2:
            r_liman = st.text_input("Tedarik Edilmesi İstenen Liman", value="Tuzla Tersanesi")
            r_tedarikci = st.text_input("Önerilen Tedarikçi / Marka (Opsiyonel)")
            r_durum = st.selectbox("Tedarik Durumu", ["📋 Onay Bekliyor", "📋 Teklif Aşamasında", "📦 Sipariş Edildi", "✅ Teslim Edildi"])
        with col_r3:
            r_onay = st.selectbox("Gemi Teslim Onayı", ["⏳ Tedarik / Teslimat Bekleniyor", "✅ Gemide Onaylandı (ETO Teslim Aldı)"])
            st.write(" ")
            if st.button("Talebi Sisteme Kaydet", use_container_width=True):
                st.success(f"'{r_parca}' talebi oluşturuldu ve satınalma listesine eklendi!")

    # TALEP LİSTESİ TABLOSU
    st.dataframe(df_req, use_container_width=True)

    st.divider()

    # LİMAN & TEDARİKÇİ TEKLİF KARŞILAŞTIRMA SEKMESİ
    st.subheader("💡 Liman Bazlı Tedarikçi Teklif Karşılaştırma (PO Evaluation)")
    st.markdown("Seçili acil parçalar için tedarikçilerden alınan tekliflerin enspektör karşılaştırması:")

    teklif_data = [
        {"Tedarikçi Firma": "MarPower Electrical B.V.", "Liman / Konum": "Rotterdam", "Parça / Ürün": "AVR MX321 (Original)", "Birim Fiyat ($)": "1,250 $", "Teslim Süresi": "2 Gün", "Enspektör Onayı": "✅ Tercih Edilen"},
        {"Tedarikçi Firma": "Singapore Marine Spares Ltd.", "Liman / Konum": "Singapur", "Parça / Ürün": "AVR MX321 (OEM)", "Birim Fiyat ($)": "890 $", "Teslim Süresi": "5 Gün", "Enspektör Onayı": "⚪ İkinci Seçenek"},
        {"Tedarikçi Firma": "Tuzla Deniz Elektrik A.Ş.", "Liman / Konum": "Tuzla / TR", "Parça / Ürün": "AVR MX321 (Muadil)", "Birim Fiyat ($)": "650 $", "Teslim Süresi": "Aynı Gün", "Enspektör Onayı": "🟡 Stok/Stil Beklemede"}
    ]
    st.dataframe(pd.DataFrame(teklif_data), use_container_width=True)

# TAB 4: ELEKTRİK ZABİTLERİ (ETO)
with tab4:
    st.subheader("👨‍✈️ Şirket Elektrik Zabitleri (ETO) & Performans Değerlendirme Tablosu")
    st.write("Şirket bünyesinde gemilerde görev yapan ve yedekte (izinde) bekleyen tüm Elektrik Zabitlerinin özet durumu:")

    eto_gemide_listesi = []
    for item in tts_fleet_data:
        k_tarih = datetime.datetime.strptime(item['Giris'], "%Y-%m-%d").date()
        b_tarih = k_tarih + datetime.timedelta(days=int(item['KontratAy']) * 30)
        k_gun = (b_tarih - datetime.date.today()).days
        if k_gun < 0: k_gun = 0

        eto_gemide_listesi.append({
            "Durum": "🚢 Gemide",
            "Adı Soyadı": item['ETO'],
            "Görevli Olduğu Gemi": item['Gemi'],
            "Katılış Tarihi": k_tarih.strftime('%d.%m.%Y'),
            "Kontrat Sonu": b_tarih.strftime('%d.%m.%Y'),
            "Kalan Gün": f"{k_gun} Gün",
            "Performans Skoru": "⭐ 4.8 / 5.0",
            "Başarılı Olduğu Konular": "PLC Otomasyon, Alternatör Bakımı, Jeneratör AVR",
            "Geliştirilmesi Gereken Alanlar": "Gemi İçi Telsiz/VHF Sistemleri",
            "Sertifika / Eğitim": "High Voltage (HV) Geçerli"
        })

    eto_yedek_listesi = [
        {
            "Durum": "🏖️ Yedekte (İzinde)",
            "Adı Soyadı": "Cemal TOPAL",
            "Görevli Olduğu Gemi": "— (Katılış Bekliyor)",
            "Katılış Tarihi": "—",
            "Kontrat Sonu": "—",
            "Kalan Gün": "Hazır (Müsait)",
            "Performans Skoru": "⭐ 4.6 / 5.0",
            "Başarılı Olduğu Konular": "Vinç Panoları, İzolasyon Arıza Bulma",
            "Geliştirilmesi Gereken Alanlar": "Sertifikasyon Yenileme",
            "Sertifika / Eğitim": "HV Sertifikası Var (Yenilenmeli)"
        },
        {
            "Durum": "🏖️ Yedekte (İzinde)",
            "Adı Soyadı": "Metin YILDIZ",
            "Görevli Olduğu Gemi": "— (Katılış Bekliyor)",
            "Katılış Tarihi": "—",
            "Kontrat Sonu": "—",
            "Kalan Gün": "Hazır (Müsait)",
            "Performans Skoru": "⭐ 4.9 / 5.0",
            "Başarılı Olduğu Konular": "Dümen Sistemleri, MSB Şalter Bakımı",
            "Geliştirilmesi Gereken Alanlar": "İngilizce Raporlama",
            "Sertifika / Eğitim": "HV + DP Maintenance"
        },
        {
            "Durum": "🏖️ Yedekte (Eğitimde)",
            "Adı Soyadı": "Selim ERDEN",
            "Görevli Olduğu Gemi": "— (Kurs Aşamasında)",
            "Katılış Tarihi": "—",
            "Kontrat Sonu": "—",
            "Kalan Gün": "15 Gün Sonra Müsait",
            "Performans Skoru": "⭐ 4.3 / 5.0",
            "Başarılı Olduğu Konular": "Akü Sistemleri, Aydınlatma & Fenerler",
            "Geliştirilmesi Gereken Alanlar": "PLC Yazılımı",
            "Sertifika / Eğitim": "HV Eğitimi Devam Ediyor"
        }
    ]

    df_tum_eto = pd.DataFrame(eto_gemide_listesi + eto_yedek_listesi)

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Toplam Elektrik Zabiti", len(df_tum_eto))
    col_m2.metric("Gemide Aktif Çalışan", len(eto_gemide_listesi))
    col_m3.metric("Yedekte / Göreve Hazır", len(eto_yedek_listesi))

    st.divider()

    filtre = st.radio("Listeleme Filtresi:", ["Hepsini Göster", "Sadece Gemidekiler", "Sadece Yedektekiler"], horizontal=True)

    if filtre == "Sadece Gemidekiler":
        df_goster = df_tum_eto[df_tum_eto["Durum"] == "🚢 Gemide"]
    elif filtre == "Sadece Yedektekiler":
        df_goster = df_tum_eto[df_tum_eto["Durum"].str.contains("Yedekte")]
    else:
        df_goster = df_tum_eto

    st.dataframe(df_goster, use_container_width=True)

# TAB 5: ARIZA KAYDI
with tab5:
    st.subheader(f"🛠️ {gemi_adi} - Elektrik Arıza Kaydı Formu")
    col1, col2 = st.columns(2)
    with col1:
        ekipman = st.selectbox("Aksam / Ekipman", [
            "Ana Dağıtım Panosu (MSB)", "Acil Durum Panosu (ESB)", "1 No'lu Jeneratör (DG1)",
            "2 No'lu Jeneratör (DG2)", "3 No'lu Jeneratör (DG3)", "Dümen Makinesi Panosu",
            "Güverte Vinçleri / Ro-Ro Rampası", "24V Akü Grubu & Şarj Panosu", "Sintine Sensörleri"
        ])
        kategori = st.selectbox("Kategori", [
            "İzolasyon (Megger) Düşüklüğü", "AVR / Voltaj Düzensizliği", "ACB / Şalter Trip",
            "Sıcaklık / Termal Kamera Anormalliği", "Kablo Kanalları / Gland", "Topraklama Hatası"
        ])
        durum = st.radio("Risk Derecesi", ["🔴 Kritik (Class / PSC Riski)", "🟡 Önemli (Kısa Vadeli Bakım)", "🟢 Uygun / Normal"])
    with col2:
        aciklama = st.text_area("Arıza Açıklaması", "Örn: MSB 440V bara izolasyon değeri düşük (0.3 M-Ohm). Neme bağlı kaçak tespit edildi.")
        uploaded_files = st.file_uploader("📸 Arıza Görselleri Yükleyin", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        st.write("### 🖼️ Yüklenen Görsel Önizlemeleri")
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, caption=f"Görsel {idx+1}: {file.name}", use_column_width=True)

    st.divider()
    if st.button("Kaydı Veritabanına Ekle"):
        st.session_state.bulgular.append({
            "Tarih": str(tarih), "Gemi": gemi_adi, "IMO": secili_gemi_bilgi['IMO'],
            "Enspektör": "Ceyhun ÜCELEHAN", "Ekipman": ekipman, "Kategori": kategori,
            "Risk Durumu": durum, "Açıklama": aciklama
        })
        st.success(f"{gemi_adi} için bulgu kaydı veritabanına eklendi!")

# TAB 6: MEGGER TESTİ
with tab6:
    st.subheader(f"⚡ {gemi_adi} - İzolasyon Direnci (Megger) Ölçümü")
    st.info("💡 Standart: 440V AC sistemler için minimum kabul edilebilir izolasyon değeri **1.0 MΩ**'dur.")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        megger_ekipman = st.selectbox("Ölçüm Yapılan Ekipman", ["DG1 Alternatör Sargıları", "DG2 Alternatör Sargıları", "MSB 440V Busbar", "Dümen Motoru 1", "Dümen Motoru 2", "Bow Thruster Motoru"])
    with m_col2:
        megger_deger = st.number_input("Ölçülen İzolasyon Değeri (MΩ)", min_value=0.0, max_value=1000.0, value=5.0, step=0.1)
    with m_col3:
        if megger_deger < 1.0:
            st.error("🔴 İZOLASYON KRİTİK DÜŞÜK! (Arıza Riski)")
        elif megger_deger < 5.0:
            st.warning("🟡 İZOLASYON ORTA DÜŞÜK (Takip Edilmeli)")
        else:
            st.success("🟢 İZOLASYON SAĞLIKLI (Normal)")

# TAB 7: PSC CHECKLIST
with tab7:
    st.subheader(f"📝 {gemi_adi} - PSC & Class Elektrik Denetim Kontrol Listesi")
    st.write("Liman Devleti Kontrolü (PSC) öncesi onaylanması gereken kritik elektrik maddeleri:")
    
    chk1 = st.checkbox("1. Acil Durum Jeneratörü (Emergency Generator) otomatik start alıyor ve ESB şalteri kapıyor.")
    chk2 = st.checkbox("2. Acil durum 24V akü grubu şarj voltajı ve yoğunluk değerleri normal.")
    chk3 = st.checkbox("3. Navigasyon fenerleri panosu alarm ve yedek ampul geçişleri sorunsuz çalışıyor.")
    chk4 = st.checkbox("4. Dümen makinesi ana ve yedek besleme motorları ile alarm testleri yapıldı.")
    chk5 = st.checkbox("5. Sintine yüksek seviye alarmları ve otomatik pompa start kontaktörleri çalışıyor.")
    chk6 = st.checkbox("6. Ana Dağıtım Panosu (MSB) önündeki yalıtkan kauçuk paspaslar eksiksiz.")

    onay_sayisi = sum([chk1, chk2, chk3, chk4, chk5, chk6])
    st.progress(onay_sayisi / 6)
    st.write(f"**Tamamlanan Kontrol:** {onay_sayisi} / 6")

# TAB 8: YEDEK PARÇA TAKİBİ
with tab8:
    st.subheader("📦 Kritik Elektrik Yedek Parça Stok Durumu")
    yedek_data = [
        {"Parça Adı": "Otomatik Voltaj Regülatörü (AVR)", "Ekipman": "DG1 / DG2 Alternatör", "Stok Adedi": 2, "Kritik Stok": 1, "Durum": "🟢 Yeterli"},
        {"Parça Adı": "ACB Koruma Rölesi", "Ekipman": "MSB Şalter", "Stok Adedi": 1, "Kritik Stok": 1, "Durum": "🟡 Sınırda"},
        {"Parça Adı": "Seyir Feneri LED Ampul Seti", "Ekipman": "Seyir Fenerleri", "Stok Adedi": 0, "Kritik Stok": 2, "Durum": "🔴 Sipariş Edilmeli"},
        {"Parça Adı": "24V 200Ah Jel Akü", "Ekipman": "Telsiz & Emergency", "Stok Adedi": 4, "Kritik Stok": 2, "Durum": "🟢 Yeterli"}
    ]
    st.dataframe(pd.DataFrame(yedek_data), use_container_width=True)

# TAB 9: RAPORLAMA & PDF/EXCEL
with tab9:
    st.subheader("📊 Filo Denetim Raporlama ve Dışa Aktarma")
    
    if len(st.session_state.bulgular) > 0:
        df_bulgu = pd.DataFrame(st.session_state.bulgular)
        st.dataframe(df_bulgu, use_container_width=True)
        
        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_bulgu.to_excel(writer, index=False, sheet_name='Enspeksiyon Bulguları')
            st.download_button("📥 Excel (.xlsx) Raporu İndir", buffer.getvalue(), f"TTS_Elektrik_Raporu_{tarih}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

        with c_exp2:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "TTS SHIPS - ELEKTRIK ENSPEKSIYON RAPORU", ln=True, align='C')
            pdf.set_font("Arial", size=10)
            pdf.cell(190, 10, f"Tarih: {tarih} | Enspektor: Ceyhun ÜCELEHAN", ln=True, align='C')
            pdf.ln(10)
            for idx, b in enumerate(st.session_state.bulgular):
                pdf.cell(190, 8, f"{idx+1}. Gemi: {b['Gemi']} | Ekipman: {b['Ekipman']} | Durum: {b['Risk Durumu']}", ln=True)
                pdf.cell(190, 8, f"   Aciklama: {b['Açıklama']}", ln=True)
                pdf.ln(2)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("📄 PDF Enspeksiyon Raporu İndir", pdf_bytes, f"TTS_Elektrik_Raporu_{tarih}.pdf", "application/pdf", use_container_width=True)
    else:
        st.warning("Henüz yeni bir bulgu eklenmedi. 'Arıza Kaydı' sekmesinden yeni kayıtlar oluşturabilirsiniz.")
