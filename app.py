# --- FILE: app.py ---
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Cấu hình trang
st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🛍️ Dashboard Phân Khúc Khách Hàng")
st.markdown("Dự án phân cụm dựa trên hành vi mua sắm (Rule-Based Clustering)")

# 2. Load dữ liệu
@st.cache_data
def load_data():
    try:
        # Đọc file csv bạn vừa xuất ở Cell 10
        df = pd.read_csv("Ket_qua_Phan_cum.csv")
        # Đổi tên cột index thành CustomerID
        if 'Unnamed: 0' in df.columns:
            df.rename(columns={'Unnamed: 0': 'CustomerID'}, inplace=True)
        return df
    except:
        return None

df = load_data()

if df is not None:
    # 3. Sidebar bộ lọc
    st.sidebar.header("Bộ lọc")
    clusters = sorted(df['Cluster'].unique())
    selected_cluster = st.sidebar.selectbox("Chọn Cụm Khách Hàng:", ["Tất cả"] + list(clusters))

    # 4. Hiển thị Metrics (Chỉ số chính)
    col1, col2 = st.columns(2)
    col1.metric("Tổng Khách Hàng", len(df))
    col2.metric("Số Lượng Cụm", len(clusters))

    # 5. Biểu đồ & Dữ liệu
    st.header(f"Phân tích cụm: {selected_cluster}")
    
    # Lọc dữ liệu theo cụm chọn
    if selected_cluster != "Tất cả":
        filtered_df = df[df['Cluster'] == selected_cluster]
    else:
        filtered_df = df

    # Cột 1: Biểu đồ, Cột 2: Bảng dữ liệu
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Phân bố khách hàng")
        # Biểu đồ cột đếm số lượng
        fig = px.bar(filtered_df['Cluster'].value_counts().reset_index(), 
                     x='Cluster', y='count', 
                     color='Cluster',
                     labels={'count': 'Số khách', 'Cluster': 'Cụm'})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Danh sách khách hàng tiêu biểu")
        st.dataframe(filtered_df.head(10), height=300)
    
    # 6. Tìm hành vi mua sắm nổi bật
    st.subheader("Hành vi mua sắm nổi bật (Top Rules)")
    # Lọc các cột bắt đầu bằng 'Rule_'
    rule_cols = [c for c in filtered_df.columns if c.startswith('Rule_')]
    
    if rule_cols:
        # Tính tỷ lệ trung bình (Mean > 0 nghĩa là có xuất hiện)
        top_rules = filtered_df[rule_cols].mean().sort_values(ascending=False).head(5)
        st.bar_chart(top_rules)
        st.info("Trục Y thể hiện tỷ lệ khách hàng trong nhóm thỏa mãn luật này.")
    
else:
    st.error("⚠️ Chưa thấy file 'Ket_qua_Phan_cum.csv'. Hãy chạy Cell 10 trong Notebook để xuất file trước!")
