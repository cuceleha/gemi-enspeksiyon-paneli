import streamlit as st
import pandas as pd
import datetime
import os

# ---------------------------------------------------------
# SAYFA YAPILANDIRMASI
# ---------------------------------------------------------
st.set_page_config(
    page_title="TTS Ships - Elektrik Enspeksiyon & Filo Yönetim Paneli",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# YEREL VEYA YEDEK GÖRSEL YÖNETİMİ
# ---------------------------------------------------------
def get_image_path(image_filename):
    local_path = os.path.join("assets", image_filename)
    if os.path.exists(local_path):
        return local_path
    return "https://raw.githubusercontent.com/streamlit/streamlit/main/e2e/scripts/components_app/static/cat.jpg"

# ---------------------------------------------------------
# GÜNCELLENMİŞ VE İNGİLİZCE STANDARTLARINA UYGUN FİLO VERİ SETİ (15 GEMİ)
# ---------------------------------------------------------
tts_fleet_data = [
    {
        "Gemi": "M/V MED STAR", "IMO": "9337028", "Tip": "Container", "DWT": "27254", "GRT": "23633", 
        "Bayrak": "Panama", "Yıl": "2004", "LOA": "191.10 m", "Durum": "🟢 Operational", "ETO": "Ahmet YILMAZ", 
        "Giris": "2026-06-15", "KontratAy": 4, "Foto": "med_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-02-15"
    },
    {
        "Gemi": "M/T MOON STAR", "IMO": "9667928", "Tip": "Tanker", "DWT": "49997", "GRT": "29940", 
        "Bayrak": "Liberia", "Yıl": "2013", "LOA": "183 m", "Durum": "🔴 Critical", "ETO": "Mehmet KAYA", 
        "Giris": "2026-04-01", "KontratAy": 6, "Foto": "moon_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet", 
        "Arıza": "DG1 AVR Failure", "Malzeme": "AVR MX321 Pending", "Denetim": "2026-10-15"
    },
    {
        "Gemi": "M/T KUZEY STAR II", "IMO": "9499175", "Tip": "Tanker", "DWT": "6107", "GRT": "4081", 
        "Bayrak": "Malta", "Yıl": "2020", "LOA": "108.10 m", "Durum": "🟡 Monitoring", "ETO": "Caner DEMİR", 
        "Giris": "2026-08-10", "KontratAy": 4, "Foto": "kuzey_star_2.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Caner", 
        "Arıza": "Bilge Sensor Monitoring", "Malzeme": "Requisition Sent", "Denetim": "2026-11-01"
    },
    {
        "Gemi": "M/V A380", "IMO": "9310915", "Tip": "Ro-Ro Cargo", "DWT": "1300", "GRT": "1285", 
        "Bayrak": "Liberia", "Yıl": "2003", "LOA": "75 m", "Durum": "🟢 Operational", "ETO": "Emre ŞAHİN", 
        "Giris": "2026-07-20", "KontratAy": 5, "Foto": "a380.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emre", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-01-10"
    },
    {
        "Gemi": "M/V AKBABA", "IMO": "9319478", "Tip": "Ro-Ro Cargo", "DWT": "1300", "GRT": "1281", 
        "Bayrak": "Liberia", "Yıl": "2004", "LOA": "75 m", "Durum": "🟢 Operational", "ETO": "Burak ÇELİK", 
        "Giris": "2026-05-12", "KontratAy": 4, "Foto": "akbaba.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Burak", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2026-12-20"
    },
    {
        "Gemi": "M/V ALEXANDRA I", "IMO": "8876340", "Tip": "Bulk Carrier", "DWT": "60054", "GRT": "4048", 
        "Bayrak": "Panama", "Yıl": "1991", "LOA": "138.40 m", "Durum": "🟢 Operational", "ETO": "Oğuz ÖZTÜRK", 
        "Giris": "2026-06-01", "KontratAy": 4, "Foto": "alexandra_1.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Oguz", 
        "Arıza": "None", "Malzeme": "Navigation Light Bulbs", "Denetim": "2027-03-05"
    },
    {
        "Gemi": "M/V ALENA", "IMO": "8857772", "Tip": "Bulk Carrier", "DWT": "60594", "GRT": "4848", 
        "Bayrak": "Panama", "Yıl": "1991", "LOA": "138.40 m", "Durum": "🟡 Monitoring", "ETO": "Serkan AYDIN", 
        "Giris": "2026-04-15", "KontratAy": 6, "Foto": "alena.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Serkan", 
        "Arıza": "Low Panel Insulation", "Malzeme": "Insulation Spray", "Denetim": "2026-10-28"
    },
    {
        "Gemi": "M/V ATLANTIC STAR", "IMO": "9473327", "Tip": "Bulk Carrier", "DWT": "75002", "GRT": "41074", 
        "Bayrak": "Liberia", "Yıl": "2011", "LOA": "225 m", "Durum": "🔴 Critical", "ETO": "Murat ASLAN", 
        "Giris": "2026-03-10", "KontratAy": 6, "Foto": "atlantic_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Murat", 
        "Arıza": "MSB Breaker (ACB) Trip", "Malzeme": "ACB Coil Set", "Denetim": "2026-10-02"
    },
    {
        "Gemi": "M/V PACIFIC STAR", "IMO": "9470387", "Tip": "Bulk Carrier", "DWT": "78128", "GRT": "41718", 
        "Bayrak": "Liberia", "Yıl": "2013", "LOA": "224.90 m", "Durum": "🟢 Operational", "ETO": "Volkan YILDIZ", 
        "Giris": "2026-07-01", "KontratAy": 4, "Foto": "pacific_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Volkan", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-04-12"
    },
    {
        "Gemi": "M/V CHIEF SEATTLE", "IMO": "9230751", "Tip": "Bulk Carrier", "DWT": "52428", "GRT": "30174", 
        "Bayrak": "Panama", "Yıl": "2001", "LOA": "189.99 m", "Durum": "🟢 Operational", "ETO": "Hasan ERDOĞAN", 
        "Giris": "2026-08-01", "KontratAy": 5, "Foto": "chief_seattle.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Hasan", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-05-18"
    },
    {
        "Gemi": "M/V VENUS STAR", "IMO": "9609134", "Tip": "Bulk Carrier", "DWT": "80888", "GRT": "44025", 
        "Bayrak": "Liberia", "Yıl": "2013", "LOA": "229 m", "Durum": "🟢 Operational", "ETO": "Ali ÖZKAN", 
        "Giris": "2026-06-20", "KontratAy": 4, "Foto": "venus_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ali", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-02-22"
    },
    {
        "Gemi": "M/V MERCUR STAR", "IMO": "9609287", "Tip": "Bulk Carrier", "DWT": "79520", "GRT": "43501", 
        "Bayrak": "Malta", "Yıl": "2015", "LOA": "229 m", "Durum": "🟢 Operational", "ETO": "Tolga TEKİN", 
        "Giris": "2026-07-10", "KontratAy": 4, "Foto": "mercur_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tolga", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-01-30"
    },
    {
        "Gemi": "M/V DENİZ STAR", "IMO": "1071472", "Tip": "General Cargo", "DWT": "8300", "GRT": "6641", 
        "Bayrak": "Liberia", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Operational", "ETO": "Onur KOÇ", 
        "Giris": "2026-08-15", "KontratAy": 4, "Foto": "deniz_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Onur", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-06-10"
    },
    {
        "Gemi": "M/V BLACKSEA STAR", "IMO": "1114901", "Tip": "General Cargo", "DWT": "8330", "GRT": "6732", 
        "Bayrak": "Liberia", "Yıl": "2025", "LOA": "142 m", "Durum": "🟢 Operational", "ETO": "Kaan YILMAZ", 
        "Giris": "2026-07-25", "KontratAy": 4, "Foto": "blacksea_star.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kaan", 
        "Arıza": "None", "Malzeme": "OK", "Denetim": "2027-07-01"
    },
    {
        "Gemi": "M/V SAPHIRA", "IMO": "7924425", "Tip": "Live Stock", "DWT": "12900", "GRT": "38988", 
        "Bayrak": "Antigua-Barbuda", "Yıl": "1995", "LOA": "185.82 m", "Durum": "🟡 Monitoring", "ETO": "Zafer GÜNEŞ", 
        "Giris": "2026-05-01", "KontratAy": 5, "Foto": "saphira.jpg", 
        "EtoFoto": "https://api.dicebear.com/7.x/avataaars/svg?seed=Zafer", 
        "Arıza": "Ventilation Fan Monitoring", "Malzeme": "Contactor Set", "Denetim": "2026-11-15"
    }
]

df_fleet = pd.DataFrame(tts_fleet_data)

# ---------------------------------------------------------
# SESSION STATE (OTURUM DURUMU TAKİBİ)
# ---------------------------------------------------------
if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

if "arizalar_db" not in st.session_state:
    st.session_state.arizalar_db = []

if "megger_db" not in st.session_state:
    st.session_state.megger_db = [
        {"Gemi": "M/T MOON STAR", "Ekipman": "DG-1 Alternatör", "Megohm": "0.2 MΩ", "Tarih": "2026-09-01", "Durum": "🔴 Critical Low"},
        {"Gemi": "M/V ATLANTIC STAR", "Ekipman": "MSB Şalter Motoru", "Megohm": "0.8 MΩ", "Tarih": "2026-09-10", "Durum": "🔴 Critical Low"},
        {"Gemi": "M/T KUZEY STAR II", "Ekipman": "Sintine Pompası Motoru", "Megohm": "2.5 MΩ", "Tarih": "2026-09-12", "Durum": "🟡 Monitoring"}
    ]

# ---------------------------------------------------------
# YAN MENÜ (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.title("⚡ TTS Inspector Panel")
st.sidebar.subheader("👨‍💼 Electrical Inspector")
st.sidebar.info("Ceyhun ÜCELEHAN")

st.sidebar.divider()

gemi_secenekleri = ["-- Fleet Overview --"] + df_fleet["Gemi"].tolist()

def on_select_change():
    secilen = st.session_state.sidebar_select
    if secilen == "-- Fleet Overview --":
        st.session_state.selected_ship = None
    else:
        st.session_state.selected_ship = secilen

current_idx = 0
if st.session_state.selected_ship in df_fleet["Gemi"].tolist():
    current_idx = gemi_secenekleri.index(st.session_state.selected_ship)

st.sidebar.selectbox(
    "Select Vessel / View Details",
    gemi_secenekleri,
    index=current_idx,
    key="sidebar_select",
    on_change=on_select_change
)

st.sidebar.divider()
st.sidebar.markdown("### 📊 Fleet Summary")
st.sidebar.write(f"• **Total Vessels:** {len(df_fleet)}")
st.sidebar.write(f"• **Critical Issues:** {len(df_fleet[df_fleet['Durum'] == '🔴 Critical'])}")
st.sidebar.write(f"• **Under Monitoring:** {len(df_fleet[df_fleet['Durum'] == '🟡 Monitoring'])}")

# =========================================================
# 🏠 PAGE 1: FLEET OVERVIEW
# =========================================================
if st.session_state.selected_ship is None:
    st.title("⚡ TTS Ships - Fleet Management & Inspection Panel")
    st.markdown("Overview of all fleet vessels, assigned ETOs, and operational status.")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    toplam_gemi = len(df_fleet)
    kritik_sayisi = len(df_fleet[df_fleet["Durum"] == "🔴 Critical"])
    malzeme_sayisi = len(df_fleet[df_fleet["Malzeme"] != "OK"])

    kpi1.metric("🚢 Total Fleet Vessels", f"{toplam_gemi} Ships")
    kpi2.metric("🔴 Critical Electrical Defect", f"{kritik_sayisi} Ships", delta="-2 Action Required", delta_color="inverse")
    kpi3.metric("🛒 Material / Spare Requisition", f"{malzeme_sayisi} Ships", delta="In Procurement")
    kpi4.metric("📅 Inspection Due (30 Days)", "3 Ships", delta="Upcoming", delta_color="off")

    st.divider()

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("🚨 Critical & Monitored Defects")
        ariza_df = df_fleet[df_fleet["Durum"].isin(["🔴 Critical", "🟡 Monitoring"])][["Gemi", "Durum", "Arıza", "ETO"]]
        st.dataframe(ariza_df, use_container_width=True, hide_index=True)

    with col_t2:
        st.subheader("🛒 Pending Spare Parts")
        malz_df = df_fleet[df_fleet["Malzeme"] != "OK"][["Gemi", "Malzeme", "Durum", "ETO"]]
        st.dataframe(malz_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("📷 TTS Fleet Vessel Cards (Select Vessel for Details)")
    
    cols_per_row = 3
    for i in range(0, len(tts_fleet_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(tts_fleet_data):
                g = tts_fleet_data[i + j]
                with cols[j]:
                    img_src = get_image_path(g["Foto"])
                    st.image(img_src, caption=f"{g['Gemi']} ({g['Tip']})", use_container_width=True)
                    
                    st.markdown(f"### {g['Gemi']}")
                    st.caption(f"**IMO:** {g['IMO']} | **Type:** {g['Tip']} | **Flag:** {g['Bayrak']}")
                    st.markdown(f"* **Electrical Status:** {g['Durum']}")
                    st.markdown(f"* **Assigned ETO:** 👨‍✈️ {g['ETO']}")
                    st.markdown(f"* **Current Defect:** `{g['Arıza']}`")
                    
                    if st.button(f"🔍 Go to {g['Gemi']} Panel", key=f"btn_gemi_{g['IMO']}", use_container_width=True):
                        st.session_state.selected_ship = g['Gemi']
                        st.rerun()
                    st.divider()

# =========================================================
# 🚢 PAGE 2: VESSEL DETAILS PANEL
# =========================================================
else:
    gemi_adi = st.session_state.selected_ship
    secili_gemi = df_fleet[df_fleet["Gemi"] == gemi_adi].iloc[0]

    if st.button("⬅️ Back to Fleet Overview", type="secondary"):
        st.session_state.selected_ship = None
        st.rerun()

    st.title(f"🚢 {gemi_adi} - Inspection & Electrical Panel")

    st.sidebar.divider()
    st.sidebar.markdown(f"### 📋 {gemi_adi} Particulars")
    st.sidebar.markdown(f"""
    * **IMO No:** {secili_gemi['IMO']}
    * **Vessel Type:** {secili_gemi['Tip']}
    * **Flag:** {secili_gemi['Bayrak']}
    * **DWT / GRT:** {secili_gemi['DWT']} / {secili_gemi['GRT']}
    * **LOA:** {secili_gemi['LOA']}
    * **Built:** {secili_gemi['Yıl']}
    * **Status:** {secili_gemi['Durum']}
    """)

    st.sidebar.subheader("👨‍✈️ Onboard ETO")
    st.sidebar.image(secili_gemi['EtoFoto'], caption=f"ETO: {secili_gemi['ETO']}", width=100)
    st.sidebar.write(f"**Sign-on Date:** {secili_gemi['Giris']}")
    st.sidebar.write(f"**Contract Duration:** {secili_gemi['KontratAy']} Months")

    tab_canli, tab_ariza, tab_megger, tab_malzeme, tab_rapor = st.tabs([
        "🌐 Live Tracking & AIS",
        "📋 Defect Report & Photos",
        "⚡ Megger (Insulation) Test Table",
        "🛒 Spare Part Requisition",
        "📄 Inspection Report Output"
    ])

    with tab_canli:
        st.subheader(f"⚓ {gemi_adi} Live AIS Tracking")
        st.info("Live AIS data and vessel tracking.")
        
        mt_link = f"https://www.marinetraffic.com/en/ais/details/ships/imo:{secili_gemi['IMO']}"
        st.link_button(f"🌐 Open {gemi_adi} on MarineTraffic", mt_link, type="primary")
        
        c_col1, c_col2 = st.columns([2, 1])
        with c_col1:
            st.image(get_image_path(secili_gemi["Foto"]), caption=f"{gemi_adi} Image", use_container_width=True)
        with c_col2:
            st.markdown("#### 📍 Last Reported Status")
            st.write(f"**Last Inspection:** {secili_gemi['Denetim']}")
            st.write(f"**Current Defect Status:** {secili_gemi['Arıza']}")
            st.write(f"**Spare Requisition:** {secili_gemi['Malzeme']}")

    with tab_ariza:
        st.subheader("📋 Defect Reporting Panel")
        
        col_a1, col_a2 = st.columns([1, 1])
        with col_a1:
            ekipman = st.selectbox(
                "Defective System / Equipment",
                ["Diesel Generator (DG1 / DG2 / DG3)", "Main Switchboard (MSB)", "Steering Gear Panel", "Bilge Separator", "Navigation Lights", "Deck Cranes / Winch", "Other"]
            )
            ariza_detay = st.text_area("Defect Description & Inspector Note", value=secili_gemi['Arıza'])
            oncelik = st.select_slider("Priority", options=["Low", "Medium", "High", "🔴 CRITICAL / URGENT"])
            
        with col_a2:
            st.markdown("#### 📷 Upload Defect Photo")
            uploaded_file = st.file_uploader("Upload Image (JPG, PNG)", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image", width=300)
            
            if st.button("💾 Save Defect Record", type="primary"):
                st.session_state.arizalar_db.append({
                    "Gemi": gemi_adi,
                    "Ekipman": ekipman,
                    "Detay": ariza_detay,
                    "Öncelik": oncelik,
                    "Tarih": datetime.date.today().strftime("%Y-%m-%d")
                })
                st.success("Defect record saved successfully!")

        st.divider()
        st.markdown("#### 📜 Defect History")
        gemi_arizalari = [a for a in st.session_state.arizalar_db if a["Gemi"] == gemi_adi]
        if gemi_arizalari:
            st.dataframe(pd.DataFrame(gemi_arizalari), use_container_width=True)
        else:
            st.info("No active defect records logged for this vessel.")

    with tab_megger:
        st.subheader("⚡ Megger (Insulation Resistance) Test Log")
        st.caption("Periodic insulation resistance measurements in Megohms (MΩ).")
        
        gemi_megger = [m for m in st.session_state.megger_db if m["Gemi"] == gemi_adi]
        if gemi_megger:
            st.table(pd.DataFrame(gemi_megger)[["Ekipman", "Megohm", "Tarih", "Durum"]])
        else:
            st.warning("No Megger record found for this vessel.")

        st.divider()
        st.markdown("#### ➕ Add New Measurement")
        m1, m2, m3, m4 = st.columns(4)
        m_ekipman = m1.text_input("Equipment (e.g. DG-1 Stator)")
        m_val = m2.number_input("Measured (MΩ)", min_value=0.0, max_value=1000.0, value=5.0, step=0.1)
        m_durum = m3.selectbox("Status", ["🟢 Excellent (>100 MΩ)", "🟢 Good (>5 MΩ)", "🟡 Monitor (1-5 MΩ)", "🔴 Critical (<1 MΩ)"])
        
        if m4.button("⚡ Save Log"):
            st.session_state.megger_db.append({
                "Gemi": gemi_adi,
                "Ekipman": m_ekipman,
                "Megohm": f"{m_val} MΩ",
                "Tarih": datetime.date.today().strftime("%Y-%m-%d"),
                "Durum": m_durum
            })
            st.success("Megger log updated!")
            st.rerun()

    with tab_malzeme:
        st.subheader("🛒 Electrical Spare Part Requisition")
        st.write(f"**Current Requisition Status:** `{secili_gemi['Malzeme']}`")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            parca_adi = st.text_input("Requested Equipment / Part", value="" if secili_gemi['Malzeme'] == "OK" else secili_gemi['Malzeme'])
            parca_adet = st.number_input("Quantity", min_value=1, value=1)
            parca_kod = st.text_input("IMPA Code (Optional)", placeholder="e.g. 33 01 22")
        with col_m2:
            liman = st.selectbox("Supply Port", ["Istanbul / Turkey", "Singapore", "Rotterdam / Netherlands", "Suez / Egypt", "Tuzla Shipyard"])
            aciklama = st.text_area("Purchase Notes", placeholder="Urgency, voltage/current specifications, etc.")
            
        if st.button("🚀 Send Requisition to Technical Purchasing", type="primary"):
            st.success(f"Requisition for {parca_adi} ({parca_adet} Pcs) sent successfully!")

    with tab_rapor:
        st.subheader("📄 Electrical Inspection Report Output")
        
        rapor_taslak = f"""
====================================================================
               TTS SHIPS ELECTRICAL INSPECTION REPORT
====================================================================
DATE        : {datetime.date.today().strftime('%d.%m.%Y')}
INSPECTOR   : Ceyhun ÜCELEHAN
VESSEL NAME : {gemi_adi}
IMO NO      : {secili_gemi['IMO']} | FLAG: {secili_gemi['Bayrak']}
TYPE        : {secili_gemi['Tip']} | LOA: {secili_gemi['LOA']}
ONBOARD ETO : {secili_gemi['ETO']}

1. ELECTRICAL SYSTEM OVERVIEW
--------------------------------------------------------------------
• Status               : {secili_gemi['Durum']}
• Active Defect        : {secili_gemi['Arıza']}
• Spare Part Status    : {secili_gemi['Malzeme']}

2. INSPECTOR ASSESSMENT & REMARKS
--------------------------------------------------------------------
• Main Switchboard (MSB) and Generators inspected.
• Megger test logs recorded.
• Maintenance plan reviewed with Onboard ETO ({secili_gemi['ETO']}).

====================================================================
Generated by: TTS Inspector Panel v2.0
====================================================================
        """
        
        st.text_area("📄 Report Preview", rapor_taslak, height=280)
        st.download_button(
            label="📥 Download Report (.TXT)",
            data=rapor_taslak,
            file_name=f"{gemi_adi.replace('/', '_')}_Inspection_Report.txt",
            mime="text/plain"
        )
