from config.settings import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    SIDEBAR_BG, TEXT_COLOR
)

def get_custom_css():
    """
    Trả về CSS string để inject vào Streamlit.

    Giải thích cho người mới:
        Streamlit cho phép chèn CSS bằng st.markdown().
        CSS = ngôn ngữ trang trí web (màu sắc, font, layout...).
        
    """
    return f"""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG};
        }}
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}

        /* Main background */
        .stApp {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Upload button */
        .stFileUploader > div > button {{
            background-color: {SECONDARY_COLOR};
            color: black;
        }}

        /* Primary buttons */
        .stButton > button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }}
        .stButton > button:hover {{
            background-color: #0056b3;
        }}

        /* Response area */
        .response-box {{
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
        }}
    </style>
    """