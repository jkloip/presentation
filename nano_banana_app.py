# ============================================================================
# 🍌 Nano Banana Pro - 超萌簡報生成器 🎨
# ============================================================================
# 功能說明：
# 1. 活潑趣味的香蕉主題介面設計
# 2. 卡通風格的視覺呈現
# 3. 豐富的動畫效果與互動體驗
# 4. 可愛的表情符號與鼓勵訊息
# 5. 漸層色彩與圓潤設計風格
# ============================================================================

import os
import base64
import logging
import asyncio
import tempfile
from datetime import datetime
from typing import Dict
from io import BytesIO
import json

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.models import AppConfig, ImageGenRequest, SlideContent
from src.providers import Gemini3Provider
from src.styles import StyleRegistry, StyleType
from src.exporter import PptxExporter
from src.renderer import PresentationRenderer

# ============================================================================
# 初始化設定
# ============================================================================
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 設定頁面配置 - Nano Banana Pro 風格
st.set_page_config(
    page_title="🍌 Nano Banana Pro - 超萌簡報生成器",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 自訂 CSS 樣式 - 活潑有趣風格
# ============================================================================
st.markdown("""
<style>
    /* 主要背景漸層 - 香蕉黃到天空藍 */
    .stApp {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFE082 25%, #FFECB3 50%, #B3E5FC 100%);
    }
    
    /* 標題樣式 - 可愛圓潤字體 */
    h1 {
        font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif;
        color: #FF6F00;
        text-shadow: 3px 3px 6px rgba(255, 111, 0, 0.3);
        animation: bounce 1s ease-in-out infinite;
    }
    
    h2, h3 {
        font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif;
        color: #F57C00;
    }
    
    /* 彈跳動畫 */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* 按鈕樣式 - 圓潤可愛 */
    .stButton > button {
        border-radius: 25px !important;
        border: 3px solid #FF6F00 !important;
        background: linear-gradient(135deg, #FFD54F 0%, #FFCA28 100%) !important;
        color: #4E342E !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 15px rgba(255, 111, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) rotate(2deg) !important;
        box-shadow: 0 6px 20px rgba(255, 111, 0, 0.5) !important;
        background: linear-gradient(135deg, #FFCA28 0%, #FFA000 100%) !important;
    }
    
    /* 輸入框樣式 - 圓潤邊框 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 3px solid #FFB300 !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    /* 選擇框樣式 */
    .stSelectbox > div > div {
        border-radius: 15px !important;
        border: 3px solid #FFB300 !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* 側邊欄樣式 - 淺色漸層 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF9C4 0%, #FFECB3 50%, #FFE082 100%) !important;
        border-right: 5px solid #FF6F00 !important;
    }
    
    /* 卡片樣式 - 可愛陰影 */
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px rgba(255, 152, 0, 0.3) !important;
        border: 3px solid #FFCA28 !important;
    }
    
    /* 成功訊息樣式 */
    .stSuccess {
        background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%) !important;
        border-radius: 15px !important;
        border-left: 5px solid #4CAF50 !important;
        padding: 15px !important;
        animation: slideIn 0.5s ease-out !important;
    }
    
    /* 警告訊息樣式 */
    .stWarning {
        background: linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%) !important;
        border-radius: 15px !important;
        border-left: 5px solid #FF9800 !important;
        padding: 15px !important;
    }
    
    /* 錯誤訊息樣式 */
    .stError {
        background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%) !important;
        border-radius: 15px !important;
        border-left: 5px solid #F44336 !important;
        padding: 15px !important;
    }
    
    /* 資訊訊息樣式 */
    .stInfo {
        background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%) !important;
        border-radius: 15px !important;
        border-left: 5px solid #03A9F4 !important;
        padding: 15px !important;
    }
    
    /* 滑入動畫 */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* 度量指標樣式 */
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        color: #FF6F00 !important;
        font-weight: bold !important;
    }
    
    /* 擴展器樣式 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%) !important;
        border-radius: 15px !important;
        border: 2px solid #FFB300 !important;
        font-weight: bold !important;
    }
    
    /* 進度條樣式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FFD54F 0%, #FF6F00 100%) !important;
        border-radius: 10px !important;
    }
    
    /* 分隔線樣式 */
    hr {
        border: 2px dashed #FFB300 !important;
        opacity: 0.6 !important;
    }
    
    /* 圖片容器樣式 */
    .stImage {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(255, 152, 0, 0.4) !important;
        border: 4px solid #FFD54F !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 定價配置
# ============================================================================
PRICING = {
    "imagen3_per_image": 0.04,
    "text_input_per_1k_tokens": 0.00025,
    "text_output_per_1k_tokens": 0.001,
}

# ============================================================================
# Session State 初始化
# ============================================================================
if "slides" not in st.session_state:
    st.session_state.slides = []

if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0

if "total_images" not in st.session_state:
    st.session_state.total_images = 0

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

if "encouragement_count" not in st.session_state:
    st.session_state.encouragement_count = 0

# ============================================================================
# 趣味鼓勵訊息庫
# ============================================================================
ENCOURAGEMENT_MESSAGES = [
    "🍌 太棒了！香蕉能量滿滿！",
    "🎨 你的創意就像香蕉一樣甜美！",
    "✨ 繼續加油！你是簡報魔法師！",
    "🌟 哇！這個設計超讚的！",
    "🚀 你的簡報要起飛啦！",
    "🎉 太厲害了！給你一個大大的讚！",
    "💪 你就是簡報製作達人！",
    "🌈 你的簡報充滿彩虹般的魔力！",
    "🎯 完美命中！這就是我們要的！",
    "⭐ 你是明日之星！繼續發光發熱！"
]

# ============================================================================
# 輔助函數
# ============================================================================

def get_random_encouragement():
    """取得隨機鼓勵訊息"""
    import random
    st.session_state.encouragement_count += 1
    return random.choice(ENCOURAGEMENT_MESSAGES)

def estimate_tokens(text: str) -> int:
    """估算文字的 Token 數量"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    estimated_tokens = (chinese_chars * 2) + (other_chars / 4)
    return int(estimated_tokens)

def calculate_cost(num_images: int, input_text: str, output_text: str = "") -> Dict:
    """計算 API 調用的總費用"""
    image_cost = num_images * PRICING["imagen3_per_image"]
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    input_cost = (input_tokens / 1000) * PRICING["text_input_per_1k_tokens"]
    output_cost = (output_tokens / 1000) * PRICING["text_output_per_1k_tokens"]
    total_cost = image_cost + input_cost + output_cost
    
    return {
        "image_cost": image_cost,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

def create_pptx_from_slides(slides: list) -> BytesIO:
    """從投影片資料創建 PowerPoint 簡報檔案"""
    exporter = PptxExporter()
    
    slide_contents = []
    for idx, slide_data in enumerate(slides):
        if not slide_data.get("generated") or not slide_data.get("image"):
            continue
        
        slide_content = SlideContent(
            slide_id=f"slide_{idx + 1}",
            framework_section=slide_data.get("style", "default"),
            title=slide_data.get("title", f"投影片 {idx + 1}"),
            body_text=slide_data.get("content", ""),
            background_image_base64=slide_data.get("image"),
            rationale=None
        )
        slide_contents.append(slide_content)
    
    style_type = StyleType.TAIPEI_METRO
    if slides and slides[0].get("style"):
        try:
            style_type = StyleType(slides[0]["style"])
        except ValueError:
            logger.warning(f"未知的風格類型: {slides[0]['style']}，使用預設台北捷運風格")
    
    style_profile = StyleRegistry.get(style_type)
    
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        exporter.export(slide_contents, tmp_path, style_profile)
        
        with open(tmp_path, "rb") as f:
            pptx_data = f.read()
        
        pptx_stream = BytesIO(pptx_data)
        pptx_stream.seek(0)
        
        return pptx_stream
    
    finally:
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"清理暫存檔案失敗: {e}")

def create_html_preview(slides: list) -> str:
    """從投影片資料創建 HTML 網頁預覽"""
    renderer = PresentationRenderer()
    
    slide_contents = []
    for idx, slide_data in enumerate(slides):
        if not slide_data.get("generated") or not slide_data.get("image"):
            continue
        
        slide_content = SlideContent(
            slide_id=f"slide_{idx + 1}",
            framework_section=slide_data.get("style", "default"),
            title=slide_data.get("title", f"投影片 {idx + 1}"),
            body_text=slide_data.get("content", ""),
            background_image_base64=slide_data.get("image"),
            rationale=None
        )
        slide_contents.append(slide_content)
    
    style_type = StyleType.TAIPEI_METRO
    if slides and slides[0].get("style"):
        try:
            style_type = StyleType(slides[0]["style"])
        except ValueError:
            logger.warning(f"未知的風格類型: {slides[0]['style']}，使用預設台北捷運風格")
    
    style_profile = StyleRegistry.get(style_type)
    html_output = renderer.render(slide_contents, style_profile)
    
    return html_output

async def generate_slide_image(provider: Gemini3Provider, prompt: str, style: str) -> Dict:
    """使用 Gemini 3 AI 生成單張投影片背景圖"""
    style_profile = StyleRegistry.get(style)
    style_prompt = style_profile.base_prompt_modifier
    full_prompt = f"{prompt}\n\n{style_prompt}"
    
    request = ImageGenRequest(prompt=full_prompt, aspect_ratio="16:9")
    result = await provider.generate(request)
    
    cost_info = calculate_cost(
        num_images=1,
        input_text=full_prompt,
        output_text=result.text_content or ""
    )
    
    return {
        "success": result.success,
        "image_base64": result.image_base64,
        "text_content": result.text_content,
        "error": result.error,
        "cost_info": cost_info
    }

# ============================================================================
# 主程式入口
# ============================================================================

def main():
    """Streamlit 應用程式主函數 - Nano Banana Pro 版本"""
    
    # 頁面標題 - 超級可愛風格
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 60px; margin-bottom: 10px;">
            🍌 Nano Banana Pro 🍌
        </h1>
        <p style="font-size: 24px; color: #F57C00; font-weight: bold;">
            超萌簡報生成器 ✨ 讓你的簡報充滿香蕉魔力！
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # 側邊欄 - 超可愛香蕉主題
    # ========================================================================
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h2>🎮 控制面板</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key 輸入
        if "api_key" not in st.session_state:
            st.session_state.api_key = os.getenv("GOOGLE_API_KEY", "")
        
        st.markdown("#### 🔑 API 金鑰設定")
        api_key_input = st.text_input(
            "Google API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="✨ 輸入你的魔法金鑰",
            help="前往 Google AI Studio 申請: https://aistudio.google.com/"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            api_key = api_key_input
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            st.success(f"✅ 金鑰已就緒！{masked_key}")
        else:
            st.warning("⚠️ 需要 API 金鑰才能施展魔法喔！")
            api_key = ""
        
        st.markdown("---")
        
        # 統計資訊 - 可愛風格
        st.markdown("#### 📊 成就統計")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🖼️ 圖片", st.session_state.total_images, 
                     delta="張" if st.session_state.total_images > 0 else None)
        with col2:
            st.metric("💰 花費", f"${st.session_state.total_cost:.3f}",
                     delta="USD" if st.session_state.total_cost > 0 else None)
        
        # 鼓勵計數器
        if st.session_state.encouragement_count > 0:
            st.info(f"🌟 已獲得 {st.session_state.encouragement_count} 次鼓勵！")
        
        # 定價資訊
        with st.expander("💵 價格資訊"):
            st.markdown(f"""
            - 🖼️ 圖片生成: **${PRICING['imagen3_per_image']}** / 張
            - 📝 輸入處理: **${PRICING['text_input_per_1k_tokens']}** / 1K tokens
            - ✍️ 輸出生成: **${PRICING['text_output_per_1k_tokens']}** / 1K tokens
            """)
        
        st.markdown("---")
        
        # 生成歷史
        if st.session_state.generation_history:
            st.markdown("#### 📜 歷史記錄")
            for i, record in enumerate(st.session_state.generation_history[-5:], 1):
                with st.expander(f"🕐 {record['time']}"):
                    st.write(f"**投影片**: {record['slide_title'][:20]}...")
                    st.write(f"**費用**: ${record['cost']:.4f}")
        
        st.markdown("---")
        
        # 趣味小貼士
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%); 
                    padding: 15px; border-radius: 15px; border: 3px solid #FFB300;">
            <h4 style="margin: 0; color: #F57C00;">💡 小貼士</h4>
            <p style="margin: 5px 0; font-size: 14px;">
            描述越詳細，AI 生成的圖片越精準！試著加入情境、色彩和氛圍描述吧！
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # 主內容區 - 投影片編輯
    # ========================================================================
    
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h2>🎨 開始創作你的超讚簡報！</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 新增投影片按鈕
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if st.button("🎉 新增投影片", use_container_width=True):
            st.session_state.slides.append({
                "title": f"🍌 投影片 {len(st.session_state.slides) + 1}",
                "content": "",
                "style": StyleType.TAIPEI_METRO,
                "image": None,
                "generated": False
            })
            st.balloons()  # 慶祝動畫！
            st.rerun()
    
    st.markdown("---")
    
    # 顯示投影片
    if not st.session_state.slides:
        st.markdown("""
        <div style="text-align: center; padding: 40px; 
                    background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%);
                    border-radius: 20px; border: 4px dashed #03A9F4;">
            <h3 style="color: #0277BD;">👆 還沒有投影片喔！</h3>
            <p style="font-size: 18px; color: #01579B;">
                點擊上方的「新增投影片」按鈕開始創作吧！🎨
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 使用標籤頁展示投影片
        tab_labels = []
        for idx, slide in enumerate(st.session_state.slides):
            emoji = "✅" if slide["generated"] else "📝"
            tab_labels.append(f"{emoji} {slide['title'][:15]}")
        
        tabs = st.tabs(tab_labels)
        
        for idx, tab in enumerate(tabs):
            with tab:
                slide = st.session_state.slides[idx]
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # 標題輸入
                    slide["title"] = st.text_input(
                        "🏷️ 投影片標題",
                        value=slide["title"],
                        key=f"title_{idx}",
                        placeholder="給你的投影片取個響亮的名字吧！"
                    )
                    
                    # 內容描述
                    slide["content"] = st.text_area(
                        "📝 內容描述（告訴 AI 你想要什麼樣的畫面）",
                        value=slide["content"],
                        height=120,
                        placeholder="例如：陽光明媚的海灘，有椰子樹和衝浪板，充滿夏日活力的氛圍 🏖️",
                        key=f"content_{idx}"
                    )
                    
                    # 風格選擇
                    style_options = [
                        ("🚇 台北捷運風格", StyleType.TAIPEI_METRO),
                        ("☕ 現代文青咖啡館", StyleType.MODERN_CAFE),
                        ("🏛️ 清水模極簡風", StyleType.MINIMAL_CONCRETE),
                        ("🌲 溫暖木質風", StyleType.WARM_WOOD),
                        ("🔮 科技漸層風", StyleType.TECH_GRADIENT),
                        ("📊 扁平資訊圖表風", StyleType.FLAT_INFOGRAPHIC)
                    ]
                    
                    if isinstance(slide["style"], str) and slide["style"] not in [s.value for s in StyleType]:
                        old_style_map = {
                            "professional": StyleType.TAIPEI_METRO,
                            "creative": StyleType.MODERN_CAFE,
                            "minimal": StyleType.MINIMAL_CONCRETE,
                            "tech": StyleType.TECH_GRADIENT,
                            "warm": StyleType.WARM_WOOD
                        }
                        slide["style"] = old_style_map.get(slide["style"], StyleType.TAIPEI_METRO)
                    
                    current_index = 0
                    for i, (_, style_type) in enumerate(style_options):
                        if slide["style"] == style_type:
                            current_index = i
                            break
                    
                    selected_style_name = st.selectbox(
                        "🎨 選擇視覺風格",
                        options=[name for name, _ in style_options],
                        index=current_index,
                        key=f"style_{idx}",
                        help="不同風格會有不同的視覺效果喔！"
                    )
                    
                    for name, style_type in style_options:
                        if name == selected_style_name:
                            slide["style"] = style_type
                            break
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 生成按鈕
                    if st.button(f"✨ 施展魔法", key=f"gen_{idx}", use_container_width=True):
                        if not api_key:
                            st.error("🔑 需要 API 金鑰才能施展魔法！")
                        elif not slide["content"].strip():
                            st.error("📝 請先描述你想要的畫面！")
                        else:
                            with st.spinner("🍌 香蕉魔法師正在施法中..."):
                                try:
                                    config = AppConfig(google_api_key=api_key)
                                    provider = Gemini3Provider(
                                        api_key=config.google_api_key,
                                        model_name=config.img_model
                                    )
                                    
                                    result = asyncio.run(
                                        generate_slide_image(
                                            provider,
                                            slide["content"],
                                            slide["style"]
                                        )
                                    )
                                    
                                    if result["success"]:
                                        slide["image"] = result["image_base64"]
                                        slide["generated"] = True
                                        
                                        cost = result["cost_info"]["total_cost"]
                                        st.session_state.total_cost += cost
                                        st.session_state.total_images += 1
                                        
                                        st.session_state.generation_history.append({
                                            "time": datetime.now().strftime("%H:%M:%S"),
                                            "slide_title": slide["title"],
                                            "cost": cost
                                        })
                                        
                                        encouragement = get_random_encouragement()
                                        st.success(f"{encouragement}\n費用: ${cost:.4f}")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.error(f"😢 施法失敗: {result['error']}")
                                
                                except Exception as e:
                                    st.error(f"💥 發生錯誤: {str(e)}")
                                    logger.error(f"生成錯誤: {e}", exc_info=True)
                    
                    # 刪除按鈕
                    if st.button(f"🗑️ 刪除", key=f"del_{idx}", use_container_width=True):
                        st.session_state.slides.pop(idx)
                        st.rerun()
                
                st.markdown("---")
                
                # 圖片顯示
                if slide["generated"] and slide["image"]:
                    st.markdown("""
                    <div style="text-align: center;">
                        <h3>🖼️ 你的傑作誕生了！</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        image_data = base64.b64decode(slide["image"])
                        st.image(image_data, use_container_width=True)
                        
                        col_a, col_b, col_c = st.columns([1, 1, 1])
                        with col_b:
                            st.download_button(
                                label="📥 下載圖片",
                                data=image_data,
                                file_name=f"{slide['title']}.png",
                                mime="image/png",
                                key=f"download_{idx}",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"😵 圖片顯示錯誤: {str(e)}")
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 30px; 
                                background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%);
                                border-radius: 15px; border: 3px dashed #FFB300;">
                        <h4 style="color: #F57C00;">🎨 準備好了嗎？</h4>
                        <p style="color: #E65100;">點擊「施展魔法」按鈕開始生成圖片吧！</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========================================================================
    # 批次操作區
    # ========================================================================
    if st.session_state.slides:
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h2>🚀 批次操作中心</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # 批次生成
        with col1:
            if st.button("🎨 全部生成", use_container_width=True):
                if not api_key:
                    st.error("🔑 需要 API 金鑰！")
                else:
                    ungenerated = [s for s in st.session_state.slides if not s["generated"]]
                    
                    if not ungenerated:
                        st.info("✅ 所有投影片都已完成！")
                    else:
                        with st.spinner(f"🍌 正在批次生成 {len(ungenerated)} 張投影片..."):
                            config = AppConfig(google_api_key=api_key)
                            provider = Gemini3Provider(
                                api_key=config.google_api_key,
                                model_name=config.img_model
                            )
                            
                            progress_bar = st.progress(0)
                            
                            for i, slide in enumerate(ungenerated):
                                try:
                                    result = asyncio.run(
                                        generate_slide_image(provider, slide["content"], slide["style"])
                                    )
                                    
                                    if result["success"]:
                                        slide["image"] = result["image_base64"]
                                        slide["generated"] = True
                                        cost = result["cost_info"]["total_cost"]
                                        st.session_state.total_cost += cost
                                        st.session_state.total_images += 1
                                    
                                    progress_bar.progress((i + 1) / len(ungenerated))
                                
                                except Exception as e:
                                    logger.error(f"批次生成錯誤: {e}")
                            
                            st.success(get_random_encouragement())
                            st.balloons()
                            st.rerun()
        
        # HTML 預覽
        with col2:
            if st.button("🌐 網頁預覽", use_container_width=True):
                generated_slides = [s for s in st.session_state.slides if s.get("generated")]
                
                if not generated_slides:
                    st.warning("⚠️ 請先生成至少一張投影片！")
                else:
                    with st.spinner("🔨 正在打造網頁..."):
                        try:
                            html_content = create_html_preview(st.session_state.slides)
                            
                            st.success(f"✅ 成功生成 {len(generated_slides)} 張投影片的網頁！")
                            
                            with st.expander("📺 點擊查看網頁預覽", expanded=True):
                                import streamlit.components.v1 as components
                                components.html(html_content, height=800, scrolling=True)
                            
                            st.download_button(
                                label="📥 下載 HTML",
                                data=html_content,
                                file_name=f"banana_presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                mime="text/html",
                                key="download_html"
                            )
                        except Exception as e:
                            st.error(f"😵 網頁生成錯誤: {str(e)}")
                            logger.error(f"HTML 預覽錯誤: {e}", exc_info=True)
        
        # 匯出 PPTX
        with col3:
            if st.button("📊 匯出簡報", use_container_width=True):
                generated_slides = [s for s in st.session_state.slides if s.get("generated")]
                
                if not generated_slides:
                    st.warning("⚠️ 請先生成至少一張投影片！")
                else:
                    with st.spinner("📦 正在打包簡報..."):
                        try:
                            pptx_stream = create_pptx_from_slides(st.session_state.slides)
                            
                            st.download_button(
                                label="📥 下載 PPTX",
                                data=pptx_stream,
                                file_name=f"banana_slides_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )
                            st.success(f"🎉 包含 {len(generated_slides)} 張投影片的簡報已就緒！")
                        except Exception as e:
                            st.error(f"😵 簡報生成錯誤: {str(e)}")
                            logger.error(f"PPTX 創建錯誤: {e}", exc_info=True)
        
        # 匯出 JSON
        with col4:
            if st.button("💾 存檔備份", use_container_width=True):
                export_data = {
                    "slides": st.session_state.slides,
                    "total_cost": st.session_state.total_cost,
                    "total_images": st.session_state.total_images,
                    "export_time": datetime.now().isoformat()
                }
                
                json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
                
                st.download_button(
                    label="📥 下載 JSON",
                    data=json_str,
                    file_name=f"banana_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                st.success("✅ 備份檔案已準備好！")
        
        # 清除所有
        with col5:
            if st.button("🧹 全部清除", use_container_width=True):
                if st.checkbox("確定要清除所有投影片嗎？", key="confirm_clear"):
                    st.session_state.slides = []
                    st.success("✅ 已清除！可以重新開始了！")
                    st.rerun()
    
    # 頁尾
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="font-size: 16px; color: #F57C00;">
            🍌 Made with love by Nano Banana Pro Team 🍌
        </p>
        <p style="font-size: 14px; color: #FF6F00;">
            ✨ 讓每一份簡報都充滿創意與樂趣！✨
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 程式進入點
# ============================================================================

if __name__ == "__main__":
    main()
