import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
from sqlalchemy import create_engine  # type: ignore
import json
import streamlit.components.v1 as components  # type: ignore
import os

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Olist Logistics", page_icon="🚚")
st.markdown("""
<style>
    /* Ẩn toàn bộ giao diện mặc định của Streamlit (Menu, Header, Footer, Margin) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px !important; margin: 0px !important; max-width: 100% !important;}
    iframe {border: none; width: 100%; height: 100vh;}
</style>
""", unsafe_allow_html=True)

BRAZIL_COORD = {
    'AC': (-9.02, -70.81), 'AL': (-9.53, -36.75), 'AM': (-3.41, -65.85),
    'AP': (1.41, -51.77), 'BA': (-12.57, -41.70), 'CE': (-5.20, -39.53),
    'DF': (-15.78, -47.93), 'ES': (-19.19, -40.34), 'GO': (-15.82, -49.83),
    'MA': (-5.42, -45.44), 'MG': (-18.10, -44.38), 'MS': (-20.51, -54.54),
    'MT': (-12.64, -55.42), 'PA': (-5.53, -52.29), 'PB': (-7.28, -36.72),
    'PE': (-8.28, -35.07), 'PI': (-8.28, -43.68), 'PR': (-24.89, -51.55),
    'RJ': (-22.84, -43.15), 'RN': (-5.22, -36.52), 'RO': (-11.22, -62.80),
    'RR': (1.89, -61.22), 'RS': (-30.01, -51.22), 'SC': (-27.33, -49.44),
    'SE': (-10.57, -37.38), 'SP': (-23.55, -46.64), 'TO': (-10.25, -48.25)
}

STATE_TO_REGION = {
    'SP': 'SE', 'RJ': 'SE', 'MG': 'SE', 'ES': 'SE',
    'RS': 'S', 'PR': 'S', 'SC': 'S',
    'BA': 'NE', 'PE': 'NE', 'CE': 'NE', 'MA': 'NE', 'PB': 'NE', 'RN': 'NE', 'AL': 'NE', 'SE': 'NE', 'PI': 'NE',
    'GO': 'CW', 'MT': 'CW', 'MS': 'CW', 'DF': 'CW',
    'AM': 'N', 'PA': 'N', 'RO': 'N', 'RR': 'N', 'AP': 'N', 'AC': 'N', 'TO': 'N'
}

@st.cache_data(show_spinner=False)
def load_data():
    try:
        if "DB_URL" in st.secrets:
            db_url = st.secrets["DB_URL"]
        else:
            db_url = "postgresql://olist_user:olist_password@localhost:5432/olist_db"
            
        engine = create_engine(db_url)
        return pd.read_sql("SELECT * FROM public.gold_kpi_by_state", engine)
    except Exception as e:
        st.error(f"Lỗi kết nối Data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    data_list = []
    for _, row in df.iterrows():
        state = row['customer_state']
        data_list.append({
            'state': state,
            'region': STATE_TO_REGION.get(state, 'SE'),
            'lat': BRAZIL_COORD.get(state, (0,0))[0],
            'lng': BRAZIL_COORD.get(state, (0,0))[1],
            'orders': int(row['total_orders']),
            'otd': float(row['ontime_delivery_rate']),
            'time': float(row['avg_delivery_time']),
            'freight': float(row['avg_freight_value'])
        })
    
    json_data = json.dumps(data_list)
    
    # Đọc template HTML gốc của user
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Inject Dữ liệu thật từ PostgreSQL vào biến JS của HTML Template
    final_html = html_content.replace("// __PYTHON_DATA_INJECTION__", f"const RAW = {json_data};")
    
    # Render Dashboard bằng Component (Height 1000px đủ rộng cho 1 màn hình)
    components.html(final_html, height=1000, scrolling=True)
else:
    st.error("⚠️ Không thể tải dữ liệu từ PostgreSQL.")