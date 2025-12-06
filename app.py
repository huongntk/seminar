import streamlit as st
import pandas as pd
from nlp.engine import classify_sentiment
from database.sqlite_helper import init_db, insert_record, get_history, clear_history


# --------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------
st.set_page_config(
    page_title="Vietnamese Sentiment Assistant",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="expanded"
)

init_db()

if 'history_limit' not in st.session_state:
    st.session_state.history_limit = 50
# --------------------------------------------------------------------
# CSS - FULL MODERN DASHBOARD THEME
# --------------------------------------------------------------------
st.markdown("""
<style>

    /* ===== GLOBAL CONTENT BACKGROUND ===== */
    main[data-testid="stAppViewContainer"] {
        background: #FAF7F2 !important;    /* Kem sáng */
    }

    h1, h2, h3, p, span, div {
        color: #1F2937;
    }

    /* ===== SIDEBAR NÂNG CẤP PREMIUM ===== */
    [data-testid="stSidebar"] {
        background: #1F2937 !important;
        padding: 40px 24px;
        border-right: 2px solid #0D141C;
        box-shadow: inset -5px 0px 10px rgba(0,0,0,0.45);
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 800;
        color: #F9FAFB;
        margin-bottom: 28px;

        text-transform: uppercase;
        letter-spacing: 1.2px;        /* làm chữ sang hơn */
        text-shadow: 0px 2px 4px rgba(0,0,0,0.35);
    }


    /* MENU ITEM chỉnh lại spacing + alignment */
    div[role='radiogroup'] > label {
        width: 100%;
        background: #F1F3F7;
        border: 2px solid #D5DAE2;
        border-radius: 12px;

        padding: 14px 18px !important;
        margin-bottom: 18px;               /* tăng khoảng cách giữa 2 ô */

        display: flex;
        align-items: center;
        justify-content: flex-start;       /* căn trái đều */
        gap: 12px;                         /* icon ↔ text rộng hơn */

        font-size: 16px;
        font-weight: 700;
        color: #1F2937 !important;

        box-shadow: 
            0px 3px 8px rgba(0,0,0,0.18),
            inset 0px 1px 0px rgba(255,255,255,0.7);

        transition: all 0.25s ease;
    }

    /* Khi active thì text + icon tịnh tiến nhẹ để tạo cảm giác “được nhấn” */
    div[role='radiogroup'] label[data-selected="true"] {
        padding-left: 22px !important;      /* đẩy text sang phải */
        transform: translateX(6px);
    }

    /* Active — nổi mạnh + phát sáng + rõ nét */
    div[role='radiogroup'] label[data-selected="true"] {
        background: #3B82F6 !important;
        border-color: #93C5FD !important;
        color: #FFFFFF !important;

        transform: translateX(8px) scale(1.05);
        
        box-shadow:
            0px 8px 22px rgba(59,130,246,0.45),
            inset 0px 0px 6px rgba(255,255,255,0.25);
    }

    /* Thanh highlight trái sắc nét */
    div[role='radiogroup'] > label::before {
        content: "";
        width: 0px;
        height: 100%;
        position: absolute;
        left: 0;
        top: 0;
        border-radius: 12px 0 0 12px;
        background: linear-gradient(180deg, #93C5FD, #3B82F6);
        transition: 0.25s ease;
    }

    /* Hover hiển thị highlight trái */
    div[role='radiogroup'] > label:hover::before {
        width: 6px;
    }

    /* Active highlight mạnh hơn */
    div[role='radiogroup'] label[data-selected="true"]::before {
        width: 8px;
    }

    /* ===== RADIO MENU ITEM ===== */
    div[role='radiogroup'] > label {
        background: #F1F3F7;
        border: 1.8px solid #D2D8E0;
        border-radius: 14px;

        padding: 14px 18px !important;
        margin-bottom: 14px;
        cursor: pointer;

        color: #1F2937 !important;
        font-size: 16px;
        font-weight: 600;

        display: flex;
        align-items: center;
        gap: 8px;

        position: relative;
        transition: all 0.22s ease;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        overflow: hidden;
    }

    /* Hover */
    div[role='radiogroup'] > label:hover {
        background: #E8ECF3;
        border-color: #3B82F6;
        transform: translateX(6px) scale(1.03);
        box-shadow: 0px 6px 16px rgba(0,0,0,0.18);
    }

    /* Active */
    div[role='radiogroup'] label[data-selected="true"] {
        background: #3B82F6 !important;
        border-color: #2563EB !important;
        color: #FFFFFF !important;

        transform: translateX(8px) scale(1.05);
        box-shadow: 0px 8px 20px rgba(59,130,246,0.35) !important;
    }

    /* Ripple Effect */
    div[role='radiogroup'] > label:active::after {
        content: "➜";
        position: absolute;
        top: var(--y);
        left: var(--x);
        width: 0px;
        height: 0px;
        background: rgba(59,130,246,0.25);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: ripple 0.55s linear;
    }

    @keyframes ripple {
        from { width: 0; height: 0; opacity: 0.45; }
        to   { width: 260px; height: 260px; opacity: 0; }
    }


    /* ===== MAIN UI ===== */
    .page-title {
        font-size: 36px;
        font-weight: 900;
        color: #1F2937;
    }

    .subtitle {
        font-size: 17px;
        color: #4B5563;
        margin-bottom: 18px;
    }

    /* Kết quả */
    .result-box {
        margin-top: 20px;
        padding: 22px;
        border-radius: 14px;
        font-size: 26px;
        font-weight: 800;
        text-align: center;
        color: white;
    }

    .pos { background: #22C55E; }
    .neg { background: #EF4444; }
    .neu { background: #6B7280; }
    /* ============================
    TONE MÀU VINTAGE + NỔI BẬT
    ============================ */

    /* Nền chính – đậm hơn & ấm hơn */
    main[data-testid="stAppViewContainer"] {
        background: #E8DFC8 !important;   /* màu kem đậm lấy từ ảnh */
        padding-top: 40px;
    }

    /* Tiêu đề nổi mạnh hơn */
    .page-title {
        font-size: 44px;
        font-weight: 900;
        color: #2A2A2A;
        margin-bottom: 10px;
        text-shadow: 1px 2px 2px rgba(0,0,0,0.15);
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #5C5448;
        margin-bottom: 20px;
    }

    /* Text Area – box vintage nổi bật */
    textarea {
        background: #F5EFE2 !important;   /* kem sáng hơn nền */
        border: 2px solid #C4B59A !important;
        border-radius: 12px !important;
        color: #2A2A2A !important;

        padding: 16px !important;
        font-size: 16px !important;

        box-shadow:
            0px 3px 8px rgba(0,0,0,0.18),
            inset 0px 1px 0px rgba(255,255,255,0.7);
    }

    /* Nút phân tích – phong cách vintage đậm */
    button[kind="secondary"] {
        background: #D9C7A7 !important;
        border: 2px solid #B8A58A !important;
        color: #2A2A2A !important;

        font-weight: 700;
        padding: 12px 0px;
        border-radius: 12px !important;

        box-shadow:
            0px 3px 8px rgba(0,0,0,0.25),
            inset 0px 1px 0px rgba(255,255,255,0.5);

        transition: 0.25s ease;
    }

    button[kind="secondary"]:hover {
        background: #CCB999 !important;
        transform: translateY(-2px);
        box-shadow:
            0px 5px 12px rgba(0,0,0,0.35),
            inset 0px 1px 1px rgba(255,255,255,0.6);
    }

    /* Result box — nổi mạnh như card thống kê trong ảnh */
    .result-box {
        background: #F5EFE2 !important;
        border: 2px solid #C4B59A !important;

        padding: 22px;
        margin-top: 26px;

        border-radius: 12px;
        font-size: 28px;
        font-weight: 900;
        color: #2A2A2A;

        box-shadow:
            0px 4px 12px rgba(0,0,0,0.25),
            inset 0px 1px 0px rgba(255,255,255,0.7);
    }

    /* Màu sắc biến thể vintage */
    .pos { background: #00FF33 !important; }
    .neg { background: #993399 !important; }
    .neu { background: #D4D4D4 !important; }
    /* ============================
   TONE NỀN VINTAGE TOÀN TRANG
   ============================ */
main[data-testid="stAppViewContainer"] {
    background: #E8DFC8 !important;
    padding-top: 40px !important;
}

/* ============================
          CARD WRAPPER
   ============================ */
.page-card {
    background: #F5EFE2;
    border: 2px solid #C8BBA4;
    border-radius: 16px;

    padding: 28px 34px;
    margin: 20px auto;
    width: 90%;
    max-width: 900px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

    /* ============================
            BREADCRUMB MỚI
    ============================ */
    .breadcrumb {
        font-size: 15px;
        font-weight: 600;
        color: #6B6357;

        display: flex;
        align-items: center;
        gap: 6px;

        margin-bottom: 14px;
    }

    .breadcrumb .divider {
        color: #948B7D;
    }

    /* ============================
        TITLE + SUBTITLE
    ============================ */
    .page-title {
        font-size: 36px;
        font-weight: 900;
        color: #2A2A2A;
        margin-bottom: 6px;
        text-shadow: 1px 2px 2px rgba(0,0,0,0.15);
    }

    .subtitle {
        font-size: 17px;
        color: #5C5448;
        margin-bottom: 20px;
    }

    /* ============================
            TEXT AREA
    ============================ */
    textarea {
        background: #F5EFE2 !important;
        border: 2px solid #C4B59A !important;
        border-radius: 12px !important;

        padding: 15px !important;
        font-size: 16px !important;
        color: #2A2A2A !important;

        box-shadow:
            0px 3px 8px rgba(0,0,0,0.18),
            inset 0px 1px 0px rgba(255,255,255,0.7);
    }

    /* ============================
            BUTTON
    ============================ */
    button[kind="secondary"] {
        background: #D9C7A7 !important;
        border: 2px solid #B8A58A !important;
        color: #2A2A2A !important;

        padding: 12px 0px;
        font-weight: 700;
        border-radius: 12px !important;

        box-shadow:
            0px 3px 8px rgba(0,0,0,0.2),
            inset 0px 1px 0px rgba(255,255,255,0.5);

        transition: 0.25s ease;
    }

    button[kind="secondary"]:hover {
        background: #CCB999 !important;
        transform: translateY(-2px);
    }

    /* ============================
            RESULT BOX
    ============================ */
    .result-box {
        background: #F5EFE2 !important;
        border: 2px solid #C4B59A !important;
        padding: 20px;
        margin-top: 24px;

        border-radius: 12px;
        font-size: 28px;
        font-weight: 900;
        color: #2A2A2A;

        box-shadow:
            0px 4px 12px rgba(0,0,0,0.25),
            inset 0px 1px 0px rgba(255,255,255,0.6);
    }

    /* màu theo tông vintage */
    .pos { background: #00FF33 !important; }
    .neg { background: #993399 !important; }
    .neu { background: #D8D8D8 !important; }

        /* DASHBOARD STAT BOX */
    .stat-box {
        background: #F0E7D8;
        border: 2px solid #C8BBA4;
        border-radius: 14px;

        padding: 20px 26px;
        width: 100%;
        
        box-shadow: 0px 6px 16px rgba(0,0,0,0.20),
                    inset 0px 1px 0px rgba(255,255,255,0.7);

        position: relative;
        margin-bottom: 18px;
    }

    .stat-value {
        font-size: 40px;
        font-weight: 900;
        color: #2A2A2A;
        margin: 0;
    }

    .stat-label {
        font-size: 16px;
        font-weight: 600;
        color: #5C5448;
        margin-top: -4px;
    }

    .stat-icon {
        position: absolute;
        right: 12px;
        top: 12px;
        opacity: 0.18;
        font-size: 58px;
    }
      
            

</style>


<script>
/* Ripple JS */
document.addEventListener("DOMContentLoaded", function() {
    const labels = document.querySelectorAll("div[role='radiogroup'] > label");
    labels.forEach(label => {
        label.addEventListener("mousedown", function(e){
            const rect = this.getBoundingClientRect();
            this.style.setProperty("--x", (e.clientX - rect.left) + "px");
            this.style.setProperty("--y", (e.clientY - rect.top) + "px");
        });
    });
});
</script>

""", unsafe_allow_html=True)


# --------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>Chức năng</div>", unsafe_allow_html=True)
    selected = st.radio("", ["Phân tích cảm xúc", "Quản lý dữ liệu"], label_visibility="collapsed")

# --------------------------------------------------------------------
# PAGE: PHÂN TÍCH CẢM XÚC
# --------------------------------------------------------------------
if selected == "Phân tích cảm xúc":

    # ====== LAYOUT 2 CỘT KHÔNG PAGE-CARD ======
    col_left, col_right = st.columns([2.2, 1])

    # -------- LEFT CONTENT --------
    with col_left:
        st.markdown("""
            <div class="breadcrumb">
                Dashboard <span class="divider">›</span> Phân tích cảm xúc
            </div>

            <div class="page-title">Phân tích cảm xúc</div>
            
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(
            "<div style='text-align:center; margin-top:10px;'>",
            unsafe_allow_html=True
        )
        st.image("asset/image/picture1.png", width=230)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:16px; color:#5C5448; margin-bottom:6px;'>"
        "Nhập một câu tiếng Việt bất kỳ để phân tích:"
        "</div>",
        unsafe_allow_html=True
    )

    # ===== TEXT AREA =====
    text = st.text_area(
        "Nội dung cần phân tích",
        placeholder="Ví dụ: hôm nay thời tiết thật đẹp!",
        height=140,
        label_visibility="collapsed"
    )

    # ===== SUBMIT BUTTON =====
    if st.button("🔍 Phân tích", use_container_width=True):

        if len(text.strip()) < 2:
            st.warning("⚠ Vui lòng nhập câu đầy đủ.")
        else:
            result = classify_sentiment(text.strip())
            sentiment = result["sentiment"]
            score = result["score"]

            insert_record(text.strip(), sentiment)

            label = (
                "TÍCH CỰC" if sentiment == "POSITIVE"
                else "TIÊU CỰC" if sentiment == "NEGATIVE"
                else "TRUNG LẬP"
            )
            css_class = (
                "pos" if sentiment == "POSITIVE"
                else "neg" if sentiment == "NEGATIVE"
                else "neu"
            )

            st.markdown(
                f"<div class='result-box {css_class}'>{label} </div>",
                unsafe_allow_html=True
            )

# --------------------------------------------------------------------
# PAGE: QUẢN LÝ DỮ LIỆU (Lịch sử + Thống kê)
# --------------------------------------------------------------------
elif selected == "Quản lý dữ liệu":

    st.markdown("""
        <div class="page-title">Quản lý dữ liệu</div>
        <div class="subtitle">Theo dõi lịch sử & thống kê cảm xúc.</div>
        <br>
    """, unsafe_allow_html=True)

    # ======================
    # TẠO 2 TAB
    # ======================
    tab1, tab2 = st.tabs(["📄 Lịch sử", "📊 Thống kê"])

    # ============================================================
    # TAB 1 – LỊCH SỬ
    # ============================================================
    with tab1:

        st.markdown("<div class='page-title'>Lịch sử phân tích</div>", unsafe_allow_html=True)

        rows = get_history(st.session_state.history_limit)

        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Câu", "Cảm xúc", "Thời gian"])
            df = df.drop(columns=["ID"]).sort_values("Thời gian", ascending=False)

            st.dataframe(df, use_container_width=True)

            # --- NÚT TẢI THÊM ---
            # Chỉ hiển thị nút nếu số lượng bản ghi hiện tại = giới hạn
            if len(rows) == st.session_state.history_limit:
                
                def load_more():
                    """Tăng giới hạn lên thêm 50 bản ghi."""
                    st.session_state.history_limit += 50
                
                st.button("⏬ Tải thêm 50 bản ghi", on_click=load_more, use_container_width=True)
            # --- NÚT XÓA TOÀN BỘ LỊCH SỬ ---
            if st.button("🗑 Xóa toàn bộ lịch sử", use_container_width=True):
                clear_history()
                st.session_state.history_limit = 50
                st.success("Đã xoá toàn bộ dữ liệu!")
                st.rerun()
        else:
            st.info("Chưa có dữ liệu nào.")

    # ============================================================
    # TAB 2 – THỐNG KÊ
    # ============================================================
    with tab2:

        st.markdown("<div class='page-title'>Thống kê cảm xúc</div>", unsafe_allow_html=True)

        rows = get_history(500)

        if not rows:
            st.info("Chưa có dữ liệu để thống kê.")
        else:
            df = pd.DataFrame(rows, columns=["ID", "Câu", "Cảm xúc", "Thời gian"])

            # --- Đếm số lượng theo cảm xúc ---
            total = len(df)
            pos = len(df[df["Cảm xúc"] == "POSITIVE"])
            neg = len(df[df["Cảm xúc"] == "NEGATIVE"])
            neu = len(df[df["Cảm xúc"] == "NEUTRAL"])

            # ======================
            # 4 CARDS THỐNG KÊ
            # ======================
            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{total}</div>
                    <div class="stat-label">Tổng câu</div>
                    <div class="stat-icon">📘</div>
                </div>
            """, unsafe_allow_html=True)

            col2.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{pos}</div>
                    <div class="stat-label">Tích cực</div>
                    <div class="stat-icon">😊</div>
                </div>
            """, unsafe_allow_html=True)

            col3.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{neg}</div>
                    <div class="stat-label">Tiêu cực</div>
                    <div class="stat-icon">😞</div>
                </div>
            """, unsafe_allow_html=True)

            col4.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{neu}</div>
                    <div class="stat-label">Trung lập</div>
                    <div class="stat-icon">😐</div>
                </div>
            """, unsafe_allow_html=True)

            st.write("")  
            st.write("")  

            # ======================
            # BIỂU ĐỒ CỘT
            # ======================
            st.subheader("📊 Biểu đồ phân bố cảm xúc")

            chart_data = pd.DataFrame({
                "Loại cảm xúc": ["Tích cực", "Tiêu cực", "Trung lập"],
                "Số lượng": [pos, neg, neu]
            })

            st.bar_chart(chart_data, x="Loại cảm xúc", y="Số lượng")

            st.write("")  

            # ======================
            # BIỂU ĐỒ TRÒN (PLOTLY)
            # ======================
            import plotly.express as px

            fig = px.pie(
                chart_data,
                names="Loại cảm xúc",
                values="Số lượng",
                color="Loại cảm xúc",
                color_discrete_map={
                    "Tích cực": "#4ade80",
                    "Tiêu cực": "#f87171",
                    "Trung lập": "#d4d4d4"
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')

            st.subheader("🟢 Biểu đồ tròn cảm xúc")
            st.plotly_chart(fig, use_container_width=True)
