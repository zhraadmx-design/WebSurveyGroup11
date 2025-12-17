import streamlit as st
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from googletrans import Translator

# =====================================================
# TRANSLATION (3 LANGUAGES) - Untuk UI
# =====================================================
LANG = {
    "Indonesia": { ... },  # Sama seperti sebelumnya
    "English": { ... },
    "China": { ... }
}

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Survey Analysis - Kelompok 11", layout="wide")

# =====================================================
# SESSION STATE & SIDEBAR
# =====================================================
if 'language' not in st.session_state:
    st.session_state.language = "English"

if 'page' not in st.session_state:
    st.session_state.page = None

# Pilih bahasa
selected_lang = st.sidebar.selectbox(
    "Language / Bahasa / 语言",
    ["Indonesia", "English", "China"],
    index=["Indonesia", "English", "China"].index(st.session_state.language)
)

if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    st.rerun()

language = st.session_state.language
t = LANG[language]

# Navigasi halaman
pages = [t["home"], t["analysis"], t["about"]]
if st.session_state.page not in pages:
    st.session_state.page = t["home"]

page = st.sidebar.radio(
    t["nav"],
    pages,
    index=pages.index(st.session_state.page)
)

if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

# =====================================================
# PAGE 1 — HOME
# =====================================================
if page == t["home"]:
    st.title(t["home_title"])
    st.write(t["home_desc"])
    st.markdown("---")
    st.subheader(t["home_intro"])
    st.markdown(f"### {t['home_desc_title']}")
    st.write(t["home_desc_text"])
    st.markdown(f"### {t['home_assoc_title']}")
    st.write(t["home_assoc_text"])

# =====================================================
# PAGE 2 — ANALYSIS
# =====================================================
elif page == t["analysis"]:
    st.title(t["analysis"])
    file = st.file_uploader(t["upload"], type=["xlsx"])
    
    if file:
        df = pd.read_excel(file)
        
        # =================================================
        # TERJEMAHKAN KOLOM / DATA KE BAHASA PILIHAN
        # =================================================
        translator = Translator()
        df_translated = df.copy()
        
        # Tentukan kode bahasa untuk googletrans
        lang_code = {"Indonesia": "id", "English": "en", "China": "zh-cn"}[language]

        # Terjemahkan semua kolom yang bertipe object (string)
        for col in df_translated.select_dtypes(include='object').columns:
            df_translated[col] = df_translated[col].astype(str).apply(
                lambda x: translator.translate(x, dest=lang_code).text if x.strip() != "" else x
            )

        st.subheader("Data (Translated)")
        st.dataframe(df_translated)

        st.subheader(t["desc_stat"])
        st.write(df_translated.describe(include='all'))

        numeric = df_translated.select_dtypes(include="number").columns
        if len(numeric) >= 2:
            x = st.selectbox(t["x_var"], numeric)
            y = st.selectbox(t["y_var"], numeric)

            if df_translated[x].nunique() > 10 and df_translated[y].nunique() > 10:
                corr, p = pearsonr(df_translated[x], df_translated[y])
                method = "Pearson"
            else:
                corr, p = spearmanr(df_translated[x], df_translated[y])
                method = "Spearman"

            st.write(f"{t['method']}: {method}")
            st.write(f"{t['coef']}: {corr:.3f}")
            st.write(f"{t['pvalue']}: {p:.4f}")
            if p < 0.05:
                st.success(t["sig"])
            else:
                st.warning(t["nosig"])

# =====================================================
# PAGE 3 — ABOUT US
# =====================================================
elif page == t["about"]:
    st.title(t["about_title"])
    st.subheader(t["about_group"])
    st.write(t["about_members"])
