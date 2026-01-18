# ============================================================================
# 簡報視覺風格定義模組 (Presentation Style Definitions)
# ============================================================================
# 說明：定義多種視覺風格的配置，包含 AI 提示詞、配色方案、吉祥物動作
# 用途：為簡報生成系統提供不同的視覺主題選擇
# 架構：採用策略模式 (Strategy Pattern)，便於擴充新風格
# ============================================================================

# 標準函式庫匯入
from enum import Enum  # 用於定義列舉型別
from typing import Dict  # 用於型別提示 (字典型別)

# 第三方函式庫匯入
from pydantic import BaseModel, Field  # 資料驗證與設定框架


# ============================================================================
# 1. 風格類型列舉 (Style Type Enumeration)
# ============================================================================
class StyleType(str, Enum):
    """
    風格類型列舉類別
    
    功能：定義系統支援的所有視覺風格類型
    繼承：str 和 Enum，使其既可作為字串也可作為列舉使用
    """
    
    # 預設風格
    DEFAULT = "default"
    
    # 台北捷運風格 - 明亮簡潔的大眾運輸標誌美學
    TAIPEI_METRO = "taipei_metro"
    
    # 現代文青咖啡館風格 - 溫暖自然光與木質家具
    MODERN_CAFE = "modern_cafe"
    
    # 清水模極簡風格 - 工業美學與幾何造型
    MINIMAL_CONCRETE = "minimal_concrete"
    
    # 溫暖木質風格 - 北歐設計與自然材質
    WARM_WOOD = "warm_wood"
    
    # 科技漸層風格 - 未來感與霓虹光暈效果
    TECH_GRADIENT = "tech_gradient"
    
    # 扁平化資訊圖表風格 - 向量圖形與粗描邊線條
    FLAT_INFOGRAPHIC = "flat_infographic"


# ============================================================================
# 2. 風格設定檔模型 (Style Profile Model)
# ============================================================================
class StyleProfile(BaseModel):
    """
    風格設定檔資料模型
    
    功能：
    - 定義單一風格的完整配置資訊
    - 包含 AI 生成圖像的提示詞策略
    - 提供邏輯配色映射 (Logic-based Color Mapping)
    - 設定吉祥物在不同場景的動作描述
    
    設計理念：
    - 反熵設計 (Anti-Entropy)：保持畫面極簡、留白充足
    - 邏輯配色：根據簡報框架章節使用不同色彩
    - 動態敘事：吉祥物動作配合內容情境
    """
    
    # 風格名稱 (用於顯示與識別)
    name: str
    
    # 版面範本名稱 (對應到特定的排版模板)
    layout_template_name: str
    
    # AI 圖像生成的基礎提示詞修飾器
    # 用於指導 AI 生成符合該風格的背景圖像
    base_prompt_modifier: str
    
    # 邏輯配色映射表 (框架章節 → 色彩代碼)
    # 例如：{"point_opening": "#E3002C", "reasons": "#C48C31"}
    logic_color_map: Dict[str, str] = Field(default_factory=dict)
    
    # 吉祥物動作映射表 (框架章節 → 動作描述)
    # 例如：{"point_opening": "Standing at attention, saluting"}
    mascot_actions: Dict[str, str] = Field(default_factory=dict)



# ============================================================================
# 3. 風格定義集合 (Style Definitions Collection)
# ============================================================================

# ----------------------------------------------------------------------------
# 3.1 台北捷運風格 (Taipei Metro Style)
# ----------------------------------------------------------------------------
METRO_STYLE = StyleProfile(
    # 風格識別名稱
    name="Taipei Metro",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 給 Gemini 的完整指令
    # 設計理念：反熵設計 - 保持畫面極簡，避免文字與浮水印
    base_prompt_modifier=(
        "Style: Clean, bright, professional public transport signage aesthetic. "  # 風格：乾淨明亮的專業大眾運輸標誌美學
        "Background: Minimalist white subway station environment, glossy textures, wide angle, "  # 背景：極簡白色捷運站環境，光滑質感，廣角視野
        "abstract geometric patterns inspired by metro maps. "  # 抽象幾何圖案靈感來自捷運地圖
        "Composition: Leave ample white space in the center for text overlay. "  # 構圖：中央留白充足供文字疊加
        "Constraint: NO TEXT, NO WATERMARKS, NO CHARACTERS, professional corporate style only."  # 限制：無文字、無浮水印、無角色，僅專業企業風格
    ),
    
    # [邏輯配色映射] 根據簡報框架章節使用對應的捷運路線顏色
    logic_color_map={
        "point_opening": "#E3002C",  # 紅線 (淡水信義線) - 用於核心論述開場
        "reasons":       "#C48C31",  # 棕線 (文湖線) - 用於數據分析與原因說明
        "examples":      "#0070BD",  # 藍線 (板南線) - 用於關鍵樞紐與實例展示
        "point_closing": "#008659",  # 綠線 (松山新店線) - 用於執行方案與結論
        "default":       "#333333"   # 預設深灰色 - 用於未明確分類的內容
    },
    
    # [動態敘事] 已移除吉祥物以符合專業商業需求
    mascot_actions={}
)


# ----------------------------------------------------------------------------
# 3.2 現代文青咖啡館風格 (Modern Cafe Style)
# ----------------------------------------------------------------------------
MODERN_CAFE_STYLE = StyleProfile(
    # 風格識別名稱
    name="Modern Cafe",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 溫暖舒適的咖啡館氛圍
    base_prompt_modifier=(
        "Style: Cozy modern cafe interior, natural lighting from large windows, professional atmosphere. "  # 風格：舒適的現代咖啡館室內，大窗戶自然採光，專業氛圍
        "Background: Wooden furniture, hanging plants, soft beige walls, warm atmosphere. "  # 背景：木質家具、吊掛植物、柔和米色牆面、溫暖氛圍
        "Lighting: Soft morning sunlight, warm tones. "  # 光線：柔和的晨光，溫暖色調
        "Composition: Minimalist with central space for content. "  # 構圖：極簡風格，中央留白供內容使用
        "Constraint: NO TEXT, NO WATERMARKS, NO CHARACTERS in the image."  # 限制：無文字、無浮水印、無角色
    ),
    
    # [邏輯配色映射] 咖啡館色系 - 以咖啡、焦糖、木質色調為主
    logic_color_map={
        "point_opening": "#8B4513",  # 深咖啡色 (SaddleBrown) - 開場
        "reasons":       "#D2691E",  # 焦糖色 (Chocolate) - 分析
        "examples":      "#6B8E23",  # 橄欖綠 (OliveDrab) - 案例
        "point_closing": "#CD853F",  # 秘魯棕 (Peru) - 結論
        "default":       "#5D4E37"   # 深咖啡棕 - 預設
    },
    
    # [動態敘事] 已移除吉祥物以符合專業商業需求
    mascot_actions={}
)


# ----------------------------------------------------------------------------
# 3.3 清水模極簡風格 (Minimal Concrete Style)
# ----------------------------------------------------------------------------
MINIMAL_CONCRETE_STYLE = StyleProfile(
    # 風格識別名稱
    name="Minimal Concrete",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 工業美學與建築感
    base_prompt_modifier=(
        "Style: Minimalist concrete architecture, industrial aesthetic, professional corporate feel. "  # 風格：極簡混凝土建築，工業美學，專業企業感
        "Background: Smooth concrete walls, subtle shadows, geometric shapes. "  # 背景：光滑混凝土牆面、微妙陰影、幾何造型
        "Lighting: Soft diffused natural light, monochromatic tones. "  # 光線：柔和漫射自然光，單色調
        "Composition: Architectural minimalism with central focus area. "  # 構圖：建築極簡主義，中央聚焦區域
        "Constraint: NO TEXT, NO WATERMARKS, NO CHARACTERS in the image."  # 限制：無文字、無浮水印、無角色
    ),
    
    # [邏輯配色映射] 灰階色系 - 混凝土質感
    logic_color_map={
        "point_opening": "#708090",  # 石板灰 (SlateGray) - 開場
        "reasons":       "#2F4F4F",  # 深石板灰 (DarkSlateGray) - 分析
        "examples":      "#696969",  # 暗灰 (DimGray) - 案例
        "point_closing": "#778899",  # 亮石板灰 (LightSlateGray) - 結論
        "default":       "#808080"   # 灰色 (Gray) - 預設
    },
    
    # [動態敘事] 已移除吉祥物以符合專業商業需求
    mascot_actions={}
)


# ----------------------------------------------------------------------------
# 3.4 溫暖木質風格 (Warm Wood Style)
# ----------------------------------------------------------------------------
WARM_WOOD_STYLE = StyleProfile(
    # 風格識別名稱
    name="Warm Wood",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 北歐設計與自然材質
    base_prompt_modifier=(
        "Style: Warm wooden interior, Scandinavian design aesthetic, professional setting. "  # 風格：溫暖木質室內，斯堪地那維亞設計美學，專業環境
        "Background: Natural wood panels, soft fabric textures, indoor plants. "  # 背景：天然木質板材、柔軟布料質感、室內植物
        "Lighting: Warm ambient light, cozy yet professional atmosphere. "  # 光線：溫暖環境光，舒適且專業的氛圍
        "Composition: Clean layout with central content area. "  # 構圖：簡潔版面，中央內容區域
        "Constraint: NO TEXT, NO WATERMARKS, NO CHARACTERS in the image."  # 限制：無文字、無浮水印、無角色
    ),
    
    # [邏輯配色映射] 木質與自然色系
    logic_color_map={
        "point_opening": "#DEB887",  # 淺木色 (BurlyWood) - 開場
        "reasons":       "#CD853F",  # 秘魯棕 (Peru) - 分析
        "examples":      "#8FBC8F",  # 深海綠 (DarkSeaGreen) - 案例
        "point_closing": "#F4A460",  # 沙褐色 (SandyBrown) - 結論
        "default":       "#D2B48C"   # 棕褐色 (Tan) - 預設
    },
    
    # [動態敘事] 已移除吉祥物以符合專業商業需求
    mascot_actions={}
)


# ----------------------------------------------------------------------------
# 3.5 科技漸層風格 (Tech Gradient Style)
# ----------------------------------------------------------------------------
TECH_GRADIENT_STYLE = StyleProfile(
    # 風格識別名稱
    name="Tech Gradient",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 未來科技感
    base_prompt_modifier=(
        "Style: Modern tech aesthetic with smooth gradients, futuristic professional feel. "  # 風格：現代科技美學，流暢漸層，未來專業感
        "Background: Flowing gradient colors (blue to purple to pink), subtle geometric patterns. "  # 背景：流動漸層色彩 (藍→紫→粉)，微妙幾何圖案
        "Lighting: Soft neon glow, digital atmosphere. "  # 光線：柔和霓虹光暈，數位氛圍
        "Composition: Tech-inspired layout with focus on data visualization aesthetic. "  # 構圖：科技風格版面，專注於數據視覺化美學
        "Constraint: NO TEXT, NO WATERMARKS, NO CHARACTERS in the image."  # 限制：無文字、無浮水印、無角色
    ),
    
    # [邏輯配色映射] 霓虹漸層色系
    logic_color_map={
        "point_opening": "#667EEA",  # 靛藍 (Indigo) - 開場
        "reasons":       "#764BA2",  # 紫色 (Purple) - 分析
        "examples":      "#F093FB",  # 粉紫 (Pink-Purple) - 案例
        "point_closing": "#4FACFE",  # 天藍 (Sky Blue) - 結論
        "default":       "#7F7FD5"   # 淺紫 (Light Purple) - 預設
    },
    
    # [動態敘事] 已移除吉祥物以符合專業商業需求
    mascot_actions={}
)


# ----------------------------------------------------------------------------
# 3.6 扁平化資訊圖表風格 (Flat Infographic Style)
# ----------------------------------------------------------------------------
FLAT_INFOGRAPHIC_STYLE = StyleProfile(
    # 風格識別名稱
    name="Flat Infographic",
    
    # 對應的排版模板
    layout_template_name="metro",
    
    # [AI 圖像生成提示詞] 商業簡報與資訊視覺化
    base_prompt_modifier=(
        "Style: Modern flat design with vector graphics and bold outlines. "  # 風格：現代扁平設計，向量圖形與粗線條輪廓
        "Background: Clean infographic layout with geometric shapes, icons, and subtle patterns. "  # 背景：乾淨的資訊圖表版面，幾何形狀、圖示與微妙圖案
        "Visual elements: Simple line art, bold strokes (3-4px), professional business icons. "  # 視覺元素：簡單線條藝術、粗描邊 (3-4px)、專業商業圖示
        "Composition: Minimalist composition with clear visual hierarchy. "  # 構圖：極簡構圖具清晰視覺層次
        "Color palette: Professional corporate colors with high contrast. "  # 色彩：專業企業色彩，高對比度
        "Aesthetic: Corporate presentation style, isometric elements optional. "  # 美學：企業簡報風格，可選用等軸測元素
        "Constraint: NO TEXT, NO WATERMARKS, pure vector-style visual background only."  # 限制：無文字、無浮水印，純向量風格視覺背景
    ),
    
    # [邏輯配色映射] 企業簡報色系 - 高對比度專業配色
    logic_color_map={
        "point_opening": "#2563EB",  # 企業藍 (Enterprise Blue) - 開場介紹
        "reasons":       "#DC2626",  # 警示紅 (Alert Red) - 問題分析
        "examples":      "#059669",  # 成功綠 (Success Green) - 解決方案展示
        "point_closing": "#7C3AED",  # 行動紫 (Action Purple) - 執行計畫結論
        "default":       "#1E293B"   # 深灰藍 (Dark Slate) - 預設
    },
    
    # [動態敘事] 已移除人物圖示，保持純粹的資訊圖表美學
    mascot_actions={}
)


# ============================================================================
# 4. 風格註冊表 (Style Registry)
# ============================================================================
class StyleRegistry:
    """
    風格註冊表類別
    
    功能：
    - 集中管理所有可用的視覺風格
    - 提供統一的風格查詢介面
    - 實作註冊表模式 (Registry Pattern)
    
    使用方式：
        style = StyleRegistry.get(StyleType.TAIPEI_METRO)
        style = StyleRegistry.get("taipei_metro")  # 也支援字串查詢
    """
    
    # 私有類別變數：風格映射表
    # 結構：{風格類型列舉 : 風格設定檔物件}
    _styles = {
        StyleType.TAIPEI_METRO: METRO_STYLE,            # 台北捷運風格
        StyleType.MODERN_CAFE: MODERN_CAFE_STYLE,        # 現代文青咖啡館風格
        StyleType.MINIMAL_CONCRETE: MINIMAL_CONCRETE_STYLE,  # 清水模極簡風格
        StyleType.WARM_WOOD: WARM_WOOD_STYLE,            # 溫暖木質風格
        StyleType.TECH_GRADIENT: TECH_GRADIENT_STYLE,    # 科技漸層風格
        StyleType.FLAT_INFOGRAPHIC: FLAT_INFOGRAPHIC_STYLE  # 扁平化資訊圖表風格
    }

    @classmethod
    def get(cls, style_type: str) -> StyleProfile:
        """
        取得指定風格的設定檔
        
        參數：
            style_type (str): 風格類型識別碼
                             可以是 StyleType 列舉值或對應的字串
        
        回傳：
            StyleProfile: 對應的風格設定檔物件
                         若找不到指定風格，則回傳預設的 METRO_STYLE
        
        範例：
            >>> style = StyleRegistry.get(StyleType.MODERN_CAFE)
            >>> style = StyleRegistry.get("modern_cafe")  # 效果相同
        """
        # 從註冊表中查詢風格，若不存在則回傳預設風格
        return cls._styles.get(style_type, METRO_STYLE)


# ============================================================================
# 模組定義完成
# ============================================================================
# 
# 擴充指南：
# 1. 新增風格類型：在 StyleType 列舉中添加新的風格代碼
# 2. 定義風格配置：創建新的 StyleProfile 實例
# 3. 註冊風格：在 StyleRegistry._styles 中加入映射關係
# 
# 設計模式：
# - 策略模式 (Strategy Pattern)：不同風格可互換使用
# - 註冊表模式 (Registry Pattern)：集中管理風格實例
# - 工廠模式 (Factory Pattern)：透過 StyleRegistry.get() 獲取實例
# ============================================================================