import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

dfrain=pd.read_csv('p1indiarainfe.csv')
dfrain.drop(columns='Unnamed: 0',inplace=True)

st.set_page_config(layout="wide")
st.title("All India Rainfall Dashboard")

# ---------------------------------------------
# SIDEBAR
# ---------------------------------------------
st.sidebar.header("Menu")

theme = st.sidebar.radio("Theme", ["Light", "Dark"])
st.sidebar.divider()

min_y = int(dfrain["year"].min())
max_y = int(dfrain["year"].max())

year_range = st.sidebar.slider("Select Year Range", min_y, max_y, (min_y, max_y))
st.sidebar.divider()
view = st.sidebar.radio("View", ["Visual", "Data"])
chartview=st.sidebar.selectbox("Chart Style",['Line','Bar','Bar with Deviation'])

# ---------------------------------------------
# THEME
# ---------------------------------------------
if theme == "Dark":
    plt.style.use("dark_background")
else:
    plt.style.use("default")

# ---------------------------------------------
# FILTER DATA
# ---------------------------------------------
filtered = dfrain[(dfrain["year"] >= year_range[0]) & (dfrain["year"] <= year_range[1])]


# ===========================================================
# VIEW: VISUAL
# ===========================================================
if view == "Visual":

    col1, col2 = st.columns([2, 1])

    # Chart
    with col1:
        st.subheader("Rainfall Chart (Seaborn)")

        if chartview=='Bar':
            fig = plt.figure(figsize=(10,4))
            sns.barplot(
                data=filtered,
                x="year",
                y="cms",
                color="orange",
                errorbar=None
            )
        elif chartview=='Line':
            fig = plt.figure(figsize=(10,4))
            sns.lineplot(
                data=filtered,
                x="year",
                y="cms",
                color="orange"
            )
        elif chartview=='Bar with Deviation':
            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12,8))
            # First subplot
            ax0=ax[0].bar(dfrain.year, dfrain.cms, color='green') # assigning bars to variable
            ax[0].set_xlabel('Year', fontsize=12, fontweight='bold')
            ax[0].set_ylabel('in cms', fontsize=12, fontweight='bold')
            ax[0].set_title('Rainfall in India',fontsize=15, fontweight='bold')
            ax[0].bar_label(ax0, fmt='%.1f', label_type='edge') # setting data labels
            ax[0].grid(True)

            # Second subplot with conditional colors
            barcolor = ['red' if x < 0 else 'green' for x in dfrain.deviation]
            ax1 = ax[1].bar(dfrain.year, dfrain.deviation, color=barcolor)
            ax[1].set_xlabel('Year', fontsize=12, fontweight='bold')
            ax[1].set_ylabel('Deviation in Cms', fontsize=12, fontweight='bold')
            ax[1].set_title('Deviation of Rainfall',fontsize=15, fontweight='bold')

            # Add bar labels
            ax[1].bar_label(ax1, fmt='%.1f', label_type='edge')
            plt.tight_layout()

        

        #plt.xlabel("Year of Rainfall")
        #plt.ylabel("Rainfall in Cms")
        #plt.title("All India Rainfall", fontsize=20)
        
        st.pyplot(fig)

    # Insights
    with col2:
        st.subheader("Insights")

        st.metric(f"Wettest Year",f"{dfrain.cms.max():.2f} cms",f"{dfrain.year[dfrain.jsmm.idxmax()]}")
        st.metric(f"Driest Year ", f"{dfrain.cms.min():.2f} cms",f"{dfrain.year[dfrain.jsmm.idxmin()]}")

        st.metric("Avg Rainfall", f"{dfrain.cms.mean():.2f} cm")

elif view == "Data":
    st.subheader("Filtered Rainfall Data")
    st.dataframe(filtered.reset_index(drop=True))


