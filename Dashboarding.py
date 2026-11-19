import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Carolina Bio Teacher Survey Dashboard")
st.header("What Teachers Need the Most Next School Year")
st.write("By Lindsay B, Lauren G, Connor L, Isaac F")

df = pd.read_csv("clustered_responses.csv")

# filter section
all_states = df["State"].unique()
target_states = st.multiselect("Choose States", options=all_states, default=list(all_states))
df = df[df["State"].isin(target_states)]

# Q1: three main messages
st.subheader("Main Messages")
st.write("1. Concerns differ by state. Virginia ranks funding #1, but New Jersey ranks learning gaps #1, "
         "so Carolina Bio should use different messages in different states.")
st.write("2. Nearly half of teachers (188 of 400) ask for low-cost, easy-to-use materials with lesson support, "
         "not a specific product. Others want advanced lab equipment (122) or environmental kits (76).")
st.write("3. Interest in Professional Development is uneven. New Jersey wants NGSS and hands-on, Connecticut wants AI and outdoor ed, so webinars should be targeted by state.")

# Q2: ranked concerns
st.subheader("Q2: Ranked Concerns (1 = most concerned, 7 = least)")

rank_cols = ["Rank_Funding", "Rank_Engagement", "Rank_LearningGaps", "Rank_PrepTime",
             "Rank_Behavior", "Rank_Standards", "Rank_PD_Training"]

col1, col2 = st.columns([5, 5])
with col1:
    avg_rank = df[rank_cols].mean().reset_index(name="Average Rank")
    avg_rank = avg_rank.rename(columns={"index": "Concern"})
    avg_rank = avg_rank.sort_values("Average Rank")
    fig1 = px.bar(avg_rank, x="Average Rank", y="Concern", orientation="h",
                  title="Average Rank (lower = bigger concern)")
    st.plotly_chart(fig1, width="stretch")

with col2:
    rank_by_state = df.groupby("State")[rank_cols].mean().round(2)
    fig2 = px.imshow(rank_by_state, text_auto=True, aspect="auto",
                     color_continuous_scale="Blues_r",
                     title="Average Rank by State (darker = bigger concern)")
    st.plotly_chart(fig2, width="stretch")

st.write("Funding (3.75) and engagement (3.76) are the top concerns overall. Virginia ranks funding #1 (3.11), "
         "while New Jersey ranks learning gaps #1 (3.49).")

# Q3: how can Carolina Bio best assist you
st.subheader("Q3: How can Carolina Bio best assist you next school year?")

col3, col4 = st.columns([5, 5])
with col3:
    theme_counts = df["Cluster_Name"].value_counts().reset_index(name="Teachers")
    fig3 = px.bar(theme_counts, x="Teachers", y="Cluster_Name", orientation="h",
                  title="Support Themes (from text clusters)")
    st.plotly_chart(fig3, width="stretch")

with col4:
    state_theme = pd.crosstab(df["State"], df["Cluster_Name"], normalize="index") * 100
    state_theme = state_theme.reset_index().melt(id_vars="State", var_name="Theme", value_name="Percent")
    fig4 = px.bar(state_theme, x="State", y="Percent", color="Theme", barmode="group",
                  text_auto=".0f", title="Support Themes by State (%)")
    st.plotly_chart(fig4, width="stretch")

# scatter plot of the clusters (made in the notebook with t-SNE)
fig5 = px.scatter(df, x="tsne_x", y="tsne_y", color="Cluster_Name",
                  hover_data=["State", "Support_Request"],
                  title="t-SNE Plot of Support Requests")
st.plotly_chart(fig5, width="stretch")

st.write("Virginia (94%) and Delaware (88%) mostly ask for low-cost, easy-to-use materials. "
         "New Jersey (68%) and Connecticut (52%) ask for advanced equipment. Connecticut has almost all career/VR requests.")

# Q4: want to learn more about teaching (check all that apply)
st.subheader("Q4: Which topics do teachers want to learn more about?")

pl_cols = ["PL_NGSS_Alignment", "PL_HandsOn_Inquiry", "PL_AI_In_Science",
           "PL_Outdoor_EnvEd", "PL_Data_Literacy"]

col5, col6 = st.columns([5, 5])
with col5:
    pl_share = df[pl_cols].mean() * 100
    pl_share = pl_share.reset_index(name="Percent of Teachers")
    pl_share = pl_share.rename(columns={"index": "Topic"})
    fig6 = px.bar(pl_share, x="Percent of Teachers", y="Topic", orientation="h",
                  title="Percent of Teachers Selecting Each Topic")
    st.plotly_chart(fig6, width="stretch")

with col6:
    pl_by_state = (df.groupby("State")[pl_cols].mean() * 100).round(0)
    fig7 = px.imshow(pl_by_state, text_auto=True, aspect="auto",
                     color_continuous_scale="Teal",
                     title="Percent Selecting Each Topic, by State")
    st.plotly_chart(fig7, width="stretch")

st.write("Hands-on inquiry (59%) and NGSS alignment (56%) are the most requested topics. "
         "New Jersey leads on both; Connecticut leads on AI in science and outdoor ed.")

# Q5: hope and joy
st.subheader("Q5: What brings you the most hope or joy about next school year?")

col7, col8 = st.columns([5, 5])
with col7:
    hope_counts = df["Hope_Theme"].value_counts().reset_index(name="Teachers")
    fig8 = px.bar(hope_counts, x="Teachers", y="Hope_Theme", orientation="h",
                  title="Hope and Joy Themes")
    st.plotly_chart(fig8, width="stretch")

with col8:
    state_hope = pd.crosstab(df["State"], df["Hope_Theme"], normalize="index") * 100
    state_hope = state_hope.reset_index().melt(id_vars="State", var_name="Theme", value_name="Percent")
    fig9 = px.bar(state_hope, x="State", y="Percent", color="Theme", barmode="group",
                  text_auto=".0f", title="Hope and Joy Themes by State (%)")
    st.plotly_chart(fig9, width="stretch")

st.write("Hope themes follow state lines: 95% of Virginia teachers hope for student curiosity, fun and teamwork, "
         "92% of Delaware teachers for scientific reasoning and student confidence, and 68% of New Jersey and "
         "50% of Connecticut teachers for hands-on engineering and technology projects. "
         "Connecticut also has the most interest in outdoor and local environment exploration (37%).")
