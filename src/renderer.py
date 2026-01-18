# ============================================================================
# HTML 渲染引擎模組 (HTML Rendering Engine Module)
# ============================================================================
# 說明：將結構化的簡報資料轉換為精美的 HTML 網頁
# 功能：使用 Jinja2 模板引擎生成響應式網頁簡報
# 特色：簡報視覺風格設計，支援多種視覺風格
# 架構：採用模板模式 (Template Pattern)
# ============================================================================

# 第三方函式庫匯入
from jinja2 import Environment, BaseLoader, select_autoescape  # Jinja2 模板引擎
from typing import List  # 型別提示

# 專案內部模組匯入
from src.models import SlideContent  # 簡報頁面內容資料模型
from src.styles import StyleProfile  # 風格設定檔資料模型


# ============================================================================
# 安全渲染器類別 (Secure Renderer)
# ============================================================================
class PresentationRenderer:
    """
    HTML 簡報渲染器
    
    功能：
    - 將簡報資料轉換為完整的 HTML 網頁
    - 整合 CSS 樣式與 Jinja2 模板
    - 支援響應式設計與視覺風格
    - 提供安全的渲染環境
    
    設計理念：
    - 簡報視覺風格：使用路線色彩與站點編號
    - 極簡設計：留白充足，視覺層次清晰
    - 響應式佈局：適應不同螢幕尺寸
    
    使用範例：
        renderer = SecureRenderer()
        html = renderer.render(slides, style_profile)
    """
    
    # ------------------------------------------------------------------------
    # 初始化方法 (Constructor)
    # ------------------------------------------------------------------------
    def __init__(self):
        """
        初始化渲染器
        
        功能：
        - 建立 Jinja2 模板環境
        - 載入 CSS 樣式表
        - 定義 HTML 模板結構
        """
        # 建立 Jinja2 模板環境
        # BaseLoader: 不從檔案系統載入模板，而是從字串載入
        # autoescape=False: 不自動轉義 HTML (因為我們需要插入 Base64 圖片)
        self.env = Environment(loader=BaseLoader(), autoescape=False)
        
        # 載入 CSS 樣式表
        self._load_presentation_css()
        
        # 載入 HTML 模板
        self._load_html_template()
    
    # ------------------------------------------------------------------------
    # 私有方法：載入 CSS 樣式表 (Private Method: Load CSS)
    # ------------------------------------------------------------------------
    def _load_presentation_css(self):
        """
        定義簡報視覺風格的 CSS 樣式表
        
        設計特色：
        - 16:9 寬螢幕比例
        - 簡報路線色帶設計
        - 站點編號徽章
        - 玻璃擬態背景（半透明白色）
        - 進度指示器
        - 卡片陰影與圓角
        """
        self.presentation_css = """
        <style>
            /* ========== 全局樣式 (Global Styles) ========== */
            
            /* 網頁主體：移除邊距，設定字體與背景色 */
            body { 
                margin: 0;  /* 移除預設邊距 */
                font-family: 'Microsoft JhengHei', sans-serif;  /* 使用微軟正黑體 */
                background: #f5f5f5;  /* 淺灰色背景 */
            }
            
            /* 容器：限制最大寬度，置中對齊，垂直堆疊 */
            .container { 
                max-width: 1200px;  /* 最大寬度 */
                margin: 20px auto;  /* 垂直邊距 20px，水平自動置中 */
                display: flex;  /* 使用 Flexbox 佈局 */
                flex-direction: column;  /* 垂直排列 */
                gap: 40px;  /* 子元素間距 40px */
            }
            
            /* ========== 簡報卡片 (Slide Card) ========== */
            
            /* 簡報頁面：16:9 比例，圓角陰影，背景圖片 */
            .slide { 
                position: relative;  /* 相對定位（作為子元素的定位基準） */
                width: 100%;  /* 寬度 100% */
                aspect-ratio: 16/9;  /* 長寬比 16:9 */
                border-radius: 16px;  /* 圓角 */
                overflow: hidden;  /* 隱藏溢出內容 */
                box-shadow: 0 12px 40px rgba(0,0,0,0.18);  /* 柔和陰影 */
                background-size: cover;  /* 背景圖片覆蓋整個區域 */
                background-position: center;  /* 背景圖片置中 */
                z-index: 1;  /* 圖層順序 */
            }
            
            /* ========== 簡報路線元素 (Presentation Line Elements) ========== */
            
            /* 簡報路線色帶：橫跨頂部的彩色條紋 */
            .presentation-line {
                position: absolute;  /* 絕對定位 */
                top: 12%;  /* 距離頂部 12% */
                left: 0;  /* 對齊左側 */
                width: 100%;  /* 寬度 100% */
                height: 18px;  /* 高度 18px */
                z-index: 3;  /* 圖層順序（在背景之上） */
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);  /* 微妙陰影 */
            }
            
            /* 站點編號徽章：圓形徽章顯示頁碼 */
            .station-badge {
                position: absolute;  /* 絕對定位 */
                top: 7%;  /* 距離頂部 7% */
                left: 5%;  /* 距離左側 5% */
                width: 70px;  /* 寬度 70px */
                height: 70px;  /* 高度 70px */
                background: white;  /* 白色背景 */
                border: 6px solid;  /* 6px 實線邊框（顏色由行內樣式決定） */
                border-radius: 50%;  /* 圓形 */
                display: flex;  /* 使用 Flexbox 佈局 */
                align-items: center;  /* 垂直置中 */
                justify-content: center;  /* 水平置中 */
                font-weight: 900;  /* 字體粗細：超粗 */
                font-size: 32px;  /* 字體大小 */
                z-index: 4;  /* 圖層順序（在路線色帶之上） */
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);  /* 立體陰影 */
            }
            
            /* ========== 進度指示器 (Progress Indicator) ========== */
            
            /* 進度點容器：右上角的點狀進度條 */
            .progress-dots {
                position: absolute;  /* 絕對定位 */
                top: 30px;  /* 距離頂部 30px */
                right: 40px;  /* 距離右側 40px */
                z-index: 10;  /* 圖層順序（最上層） */
                display: flex;  /* 使用 Flexbox 佈局 */
                gap: 10px;  /* 點之間的間距 */
            }
            
            /* 進度點：單個圓點 */
            .progress-dot {
                width: 14px;  /* 寬度 */
                height: 14px;  /* 高度 */
                border-radius: 50%;  /* 圓形 */
                background: rgba(255,255,255,0.4);  /* 半透明白色（未啟用狀態） */
                transition: all 0.3s;  /* 平滑過渡動畫 */
            }
            
            /* 進度點（啟用狀態）：當前頁面的指示點 */
            .progress-dot.active {
                background: rgba(255,255,255,0.95);  /* 不透明白色 */
                box-shadow: 0 0 12px rgba(255,255,255,0.8);  /* 發光效果 */
            }
            
            /* ========== 文字內容區域 (Text Content Area) ========== */
            
            /* 文字內容容器：主要文字區域 */
            .text-content {
                position: absolute;  /* 絕對定位 */
                top: 22%;  /* 距離頂部 22% */
                left: 8%;  /* 距離左側 8% */
                width: 65%;  /* 寬度 65% */
                z-index: 5;  /* 圖層順序 */
            }
            
            /* 標題樣式：大標題文字 */
            h1 { 
                font-size: 48px;  /* 字體大小 */
                margin: 0 0 25px 0;  /* 邊距（下方 25px） */
                letter-spacing: 1.5px;  /* 字母間距 */
                font-weight: 900;  /* 字體粗細：超粗 */
                color: #1a1a1a;  /* 深灰色文字 */
                background: rgba(255,255,255,0.96);  /* 半透明白色背景（玻璃擬態） */
                padding: 20px 30px;  /* 內邊距 */
                display: inline-block;  /* 行內區塊元素 */
                border-radius: 12px;  /* 圓角 */
                box-shadow: 0 4px 20px rgba(0,0,0,0.12);  /* 柔和陰影 */
                border-left: 8px solid;  /* 左側彩色邊框（顏色由行內樣式決定） */
            }
            
            /* 段落樣式：主要內容文字 */
            p { 
                font-size: 24px;  /* 字體大小 */
                line-height: 1.8;  /* 行高（提升可讀性） */
                white-space: pre-line;  /* 保留換行符號 */
                font-weight: 500;  /* 字體粗細：中等 */
                color: #2a2a2a;  /* 深灰色文字 */
                background: rgba(255,255,255,0.94);  /* 半透明白色背景 */
                padding: 25px 30px;  /* 內邊距 */
                border-radius: 10px;  /* 圓角 */
                box-shadow: 0 3px 15px rgba(0,0,0,0.1);  /* 柔和陰影 */
                margin-top: 15px;  /* 上邊距 */
            }
        </style>
        """
    
    # ------------------------------------------------------------------------
    # 私有方法：載入 HTML 模板 (Private Method: Load Template)
    # ------------------------------------------------------------------------
    def _load_html_template(self):
        """
        定義 HTML 模板結構
        
        功能：
        - 使用 Jinja2 模板語法
        - 支援變數插值與迴圈
        - 整合 CSS 與動態資料
        
        模板變數：
        - slides: 簡報頁面列表
        - style: 風格設定檔
        - css: CSS 樣式表
        
        Jinja2 語法說明：
        - {{ variable }}: 變數插值
        - {% for ... %}: 迴圈
        - {% if ... %}: 條件判斷
        - {{ "格式" | format(變數) }}: 格式化過濾器
        """
        self.template = """
        <!DOCTYPE html>
        <html>
        <head>
            <!-- 設定字元編碼為 UTF-8 -->
            <meta charset="UTF-8">
            
            <!-- 插入 CSS 樣式表 -->
            {{ css }}
        </head>
        <body>
            <!-- 主容器 -->
            <div class="container">
            
            <!-- 遍歷所有簡報頁面 -->
            {% for slide in slides %}
                <!-- 步驟 1: 取得當前頁面的路線顏色 -->
                {% set color = style.logic_color_map.get(slide.framework_section, '#333') %}
                
                <!-- 步驟 2: 建立簡報卡片 -->
                <!-- 背景圖片：使用 Base64 編碼的圖片（若存在） -->
                <div class="slide" style="background-image: url('{% if slide.background_image_base64 %}data:image/png;base64,{{ slide.background_image_base64 }}{% endif %}');">
                    
                    <!-- 步驟 3: 繪製捷運路線色帶 -->
                    <div class="metro-line" style="background-color: {{ color }};"></div>
                    
                    <!-- 步驟 4: 繪製站點編號徽章 -->
                    <!-- loop.index 是 Jinja2 提供的迴圈計數器（從 1 開始） -->
                    <!-- %02d 表示格式化為兩位數（例如：01, 02, ...） -->
                    <div class="station-badge" style="border-color: {{ color }}; color: {{ color }}">
                        {{ "%02d" | format(loop.index) }}
                    </div>
                    
                    <!-- 步驟 5: 繪製進度指示器 -->
                    <div class="progress-dots">
                        <!-- 遍歷所有頁面以建立進度點 -->
                        {% for i in range(1, slides|length + 1) %}
                        <!-- 當前頁面的進度點會加上 active 類別 -->
                        <div class="progress-dot{% if i == loop.index %} active{% endif %}" 
                             style="{% if i == loop.index %}border: 2px solid {{ color }};{% endif %}">
                        </div>
                        {% endfor %}
                    </div>
                    
                    <!-- 步驟 6: 繪製文字內容區域 -->
                    <div class="text-content">
                        <!-- 標題：左側邊框使用路線顏色 -->
                        <h1 style="border-left-color: {{ color }};">{{ slide.title }}</h1>
                        
                        <!-- 內容：自動換行 -->
                        <p>{{ slide.body_text }}</p>
                    </div>
                </div>
            {% endfor %}
            
            </div> <!-- 結束 container -->
        </body>
        </html>
        """
    
    # ------------------------------------------------------------------------
    # 公開方法：渲染簡報 (Public Method: Render Presentation)
    # ------------------------------------------------------------------------
    def render(self, slides: List[SlideContent], style: StyleProfile) -> str:
        """
        渲染簡報為 HTML 字串
        
        功能：
        - 將簡報資料與風格設定結合
        - 使用 Jinja2 模板引擎生成完整 HTML
        - 返回可直接儲存或顯示的 HTML 字串
        
        參數：
            slides (List[SlideContent]): 簡報頁面列表
            style (StyleProfile): 風格設定檔（包含配色與視覺設定）
        
        回傳：
            str: 完整的 HTML 網頁字串
        
        使用範例：
            html_output = renderer.render(slides, metro_style)
            with open('presentation.html', 'w', encoding='utf-8') as f:
                f.write(html_output)
        """
        # 步驟 1: 從字串建立 Jinja2 模板物件
        tpl = self.env.from_string(self.template)
        
        # 步驟 2: 渲染模板，傳入資料變數
        # slides: 簡報頁面列表
        # style: 風格設定檔（用於取得配色資訊）
        # css: CSS 樣式表字串
        return tpl.render(slides=slides, style=style, css=self.presentation_css)


# ============================================================================
# 模組定義完成
# ============================================================================
#
# 技術細節：
# 1. Jinja2 模板引擎：提供強大的模板語法與變數插值
# 2. 玻璃擬態設計 (Glassmorphism)：半透明白色背景
# 3. 響應式設計：使用 aspect-ratio 與百分比單位
# 4. CSS Flexbox：靈活的佈局系統
#
# 擴充指南：
# 1. 新增模板：建立新的 CSS 與 HTML 模板方法
# 2. 自訂樣式：修改 _load_metro_css() 中的 CSS 規則
# 3. 互動功能：可加入 JavaScript 實現頁面切換動畫
#
# 設計模式：
# - 模板模式 (Template Pattern)：定義固定結構，填入可變資料
# - 策略模式 (Strategy Pattern)：可切換不同的視覺風格
# ============================================================================