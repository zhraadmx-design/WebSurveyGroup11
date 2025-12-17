import streamlit as st
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Survey Analysis - Kelompok 11",
    layout="wide"
)

# =====================================================
# SIDEBAR LANGUAGE SELECTION
# =====================================================
language = st.sidebar.selectbox(
    "Pilih Bahasa / Select Language",
    ["Indonesia", "English"]
)

# =====================================================
# TEXT DI BASED ON LANGUAGE
# =====================================================
if language == "Indonesia":
    texts = {
        "home_title": "Aplikasi Analisis Survei",
        "home_subtitle": "Kelompok 11 — President University",
        "pendahuluan_title": "Pendahuluan",
        "pendahuluan_text": "Aplikasi ini dirancang untuk membantu pengolahan dan analisis data survei menggunakan pendekatan statistik secara sistematis dan informatif.",
        "deskriptif_title": "Analisis Deskriptif",
        "deskriptif_text": "Analisis deskriptif digunakan untuk menggambarkan karakteristik data survei, seperti mean, median, standar deviasi, nilai minimum, dan maksimum.",
        "asosiasi_title": "Analisis Asosiasi",
        "asosiasi_text": "Analisis asosiasi bertujuan untuk mengetahui hubungan antar variabel numerik. Aplikasi ini menggunakan korelasi Pearson atau Spearman secara otomatis.",
        "tujuan_title": "Tujuan",
        "tujuan_text": "Membantu mahasiswa dalam memahami data survei serta menyajikan hasil analisis statistik yang mudah dipahami.",
        "upload_file": "Upload File Excel",
        "desc_stats": "Statistik Deskriptif",
        "scatter_plot": "Visualisasi Scatter Plot",
        "variable_x": "Variabel X",
        "variable_y": "Variabel Y",
        "method": "Metode",
        "corr_coef": "Koefisien Korelasi",
        "p_value": "P-value",
        "significant": "Hubungan signifikan ditemukan.",
        "not_significant": "Tidak ditemukan hubungan signifikan.",
        "about_title": "President University",
        "about_subtitle": "Kelompok 11"
    }
else:
    texts = {
        "home_title": "Survey Analysis Application",
        "home_subtitle": "Group 11 — President University",
        "pendahuluan_title": "Introduction",
        "pendahuluan_text": "This application is designed to help process and analyze survey data using a systematic and informative statistical approach.",
        "deskriptif_title": "Descriptive Analysis",
        "deskriptif_text": "Descriptive analysis is used to describe survey data characteristics, such as mean, median, standard deviation, minimum, and maximum values.",
        "asosiasi_title": "Association Analysis",
        "asosiasi_text": "Association analysis aims to identify relationships between numeric variables. The app automatically uses Pearson or Spearman correlation.",
        "tujuan_title": "Purpose",
        "tujuan_text": "Helps students understand survey data and present statistical analysis results in an easy-to-understand way.",
        "upload_file": "Upload Excel File",
        "desc_stats": "Descriptive Statistics",
        "scatter_plot": "Scatter Plot Visualization",
        "variable_x": "Variable X",
        "variable_y": "Variable Y",
        "method": "Method",
        "corr_coef": "Correlation Coefficient",
        "p_value": "P-value",
        "significant": "Significant relationship found.",
        "not_significant": "No significant relationship found.",
        "about_title": "President University",
        "about_subtitle": "Group 11"
    }

# =====================================================
# CSS — FULL COLOR THEME (tetap cantik!)
# =====================================================
st.markdown("""
<style>
/* BACKGROUND */
.stApp {
    background: linear-gradient(180deg, #fdeaff 0%, #e8f0ff 100%);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ff7eb3, #8ec5fc);
    padding-top: 30px;
}
section[data-testid="stSidebar"] * {color: white !important; font-weight: 500;}

/* HEADER */
.header-box {
    background: linear-gradient(135deg, #ff7eb3, #8ec5fc);
    padding: 55px; border-radius: 0 0 45px 45px; text-align: center;
    color: white; margin-bottom: 60px; box-shadow: 0 15px 30px rgba(0,0,0,0.12);
}

/* CARDS */
.section-card, .profile-card {
    background: white; padding: 30px; border-radius: 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1); margin-bottom: 35px;
}
.section-title {font-size: 26px; font-weight: bold; color: #ff6fae; margin-bottom: 12px;}
.section-text {font-size: 18px; color: #444; line-height: 1.7;}
.profile-name {font-size: 28px; font-weight: bold; color: #ff6fae;}
.profile-text {font-size: 18px; color: #444;}
.profile-quote {margin-top: 10px; font-style: italic; color: #7aa2ff;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
page = st.sidebar.radio("Navigasi", ["Home", "Analisis Survei", "About Us"])

# =====================================================
# HOME
# =====================================================
if page == "Home":
    st.markdown(f'<div class="header-box"><h1>{texts["home_title"]}</h1><h3>{texts["home_subtitle"]}</h3></div>', unsafe_allow_html=True)
    for title_key in ["pendahuluan", "deskriptif", "asosiasi", "tujuan"]:
        st.markdown(f'''
        <div class="section-card">
            <div class="section-title">{texts[f"{title_key}_title"]}</div>
            <div class="section-text">{texts[f"{title_key}_text"]}</div>
        </div>
        ''', unsafe_allow_html=True)

# =====================================================
# ANALISIS SURVEI
# =====================================================
elif page == "Analisis Survei":
    st.title("Analisis Data Survei")
    file = st.file_uploader(texts["upload_file"], type=["xlsx"])

    if file:
        df = pd.read_excel(file)
        st.dataframe(df)
        st.subheader(texts["desc_stats"])
        st.write(df.describe())

        numeric = df.select_dtypes(include="number").columns
        if len(numeric) >= 2:
            x = st.selectbox(texts["variable_x"], numeric)
            y = st.selectbox(texts["variable_y"], numeric)

            if df[x].nunique() > 10 and df[y].nunique() > 10:
                corr, p = pearsonr(df[x], df[y])
                method = "Pearson"
            else:
                corr, p = spearmanr(df[x], df[y])
                method = "Spearman"

            st.write(f"**{texts['method']}:** {method}")
            st.write(f"**{texts['corr_coef']}:** {corr:.3f}")
            st.write(f"**{texts['p_value']}:** {p:.4f}")
            st.write("**Hubungan signifikan ditemukan.**" if p < 0.05 else "**Tidak ditemukan hubungan signifikan.**")

            st.subheader(texts["scatter_plot"])
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(data=df, x=x, y=y, ax=ax, s=100, color="#FF6FAE", alpha=0.7)
            sns.regplot(data=df, x=x, y=y, scatter=False, ax=ax, color="#7AA2FF")
            ax.set_title(f"{x} vs {y}", fontsize=16)
            st.pyplot(fig)

# =====================================================
# ABOUT US — DI-FIX biar jalan di Streamlit versi lama juga!
# =====================================================
elif page == "About Us":
    st.markdown(f'<div class="header-box"><h1>{texts["about_title"]}</h1><h3>{texts["about_subtitle"]}</h3></div>', unsafe_allow_html=True)

    members = [
        ("Alya Mukhbita", "004202400003", "Project Leader & Documentation", "assets/alya.jpg", "Leading with grace"),
        ("Nabila Maharani Yudhistiro", "004202400116", "UI/UX Designer", "assets/Nabila.jpg", "Beauty in every pixel"),
        ("Talytha Belva Clarisa", "004202400020", "Data Analyst", "assets/talytha.jpg", "Data tells the story"),
        ("Zahra Aulia Al Madani", "004202400087", "Programmer", "assets/Zahra.jpg", "Code with purpose")
    ]

    for i in range(0, len(members), 2):
        col1, col2 = st.columns(2)
        # Anggota kiri
        with col1:
            m = members[i]
            st.image(m[3], use_column_width=True)  # ← diubah jadi use_column_width (kompatibel semua versi)
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-name">{m[0]}</div>
                <div class="profile-text"><b>NIM:</b> {m[1]}</div>
                <div class="profile-text"><b>Role:</b> {m[2]}</div>
                <div class="profile-quote">"{m[4]}"</div>
            </div>
            """, unsafe_allow_html=True)
        # Anggota kanan (kalau ada)
        if i+1 < len(members):
            with col2:
                m = members[i+1]
                st.image(m[3], use_column_width=True)
                st.markdown(f"""
                <div class="profile-card">
                    <div class="profile-name">{m[0]}</div>
                    <div class="profile-text"><b>NIM:</b> {m[1]}</div>
                    <div class="profile-text"><b>Role:</b> {m[2]}</div>
                    <div class="profile-quote">"{m[4]}"</div>
                </div>
                """, unsafe_allow_html=True)
