# ============================================================================
# AI 圖像生成提供者模組 (AI Image Generation Provider Module)
# ============================================================================
# 說明：封裝與 Google Gemini 3 API 的互動邏輯
# 功能：使用 Imagen 3 模型生成專業資訊圖表
# 架構：採用提供者模式 (Provider Pattern)，便於未來擴充其他 AI 服務
# ============================================================================

# 標準函式庫匯入
import logging  # 日誌記錄功能
import base64  # Base64 編碼解碼功能
import asyncio  # 非同步程式支援
import tempfile  # 臨時檔案處理
import os  # 作業系統介面

# 第三方函式庫匯入
from google import genai  # Google Generative AI SDK
from google.genai import types  # Google GenAI 型別定義

# 專案內部模組匯入
from src.models import ImageGenRequest, ImageGenResult  # 請求與回應資料模型

# 初始化日誌記錄器 (Logger)
# __name__ 會自動使用當前模組名稱作為 logger 名稱
logger = logging.getLogger(__name__)


# ============================================================================
# Gemini 3 圖像生成提供者類別 (Gemini 3 Image Generation Provider)
# ============================================================================
class Gemini3Provider:
    """
    Google Gemini 3 圖像生成服務提供者
    
    功能：
    - 使用 Imagen 3 模型生成高品質資訊圖表
    - 支援多模態回應 (文字 + 圖像)
    - 提供非同步 API 呼叫介面
    - 完整的錯誤處理與日誌記錄
    
    使用範例：
        provider = Gemini3Provider(api_key="YOUR_API_KEY", model_name="gemini-3-pro-image-preview")
        result = await provider.generate(ImageGenRequest(prompt="生成捷運站場景"))
    """
    
    # ------------------------------------------------------------------------
    # 初始化方法 (Constructor)
    # ------------------------------------------------------------------------
    def __init__(self, api_key: str, model_name: str):
        """
        初始化 Gemini 3 提供者
        
        參數：
            api_key (str): Google API 金鑰，用於身份驗證
            model_name (str): 模型名稱，例如 "gemini-3-pro-image-preview"
        """
        # 建立 Google GenAI 客戶端實例
        self.client = genai.Client(api_key=api_key)
        
        # 儲存模型名稱供後續使用
        self.model_name = model_name
    
    # ------------------------------------------------------------------------
    # 公開方法：生成圖像 (Public Method: Generate Image)
    # ------------------------------------------------------------------------
    async def generate(self, request: ImageGenRequest) -> ImageGenResult:
        """
        非同步生成圖像 (主要入口方法)
        
        功能：
        - 接收圖像生成請求
        - 呼叫 AI 模型生成圖像
        - 處理回應並轉換為標準格式
        - 提供完整的錯誤處理
        
        參數：
            request (ImageGenRequest): 包含提示詞與參數的請求物件
        
        回傳：
            ImageGenResult: 包含生成結果、圖像資料或錯誤訊息的回應物件
        """
        # 記錄開始生成的日誌 (截取前 80 個字元避免日誌過長)
        logger.info(f"📊 Imagen 3 正在生成資訊圖表: {request.prompt[:80]}...")
        
        try:
            # 步驟 1: 非同步執行 SDK 呼叫
            # 使用 asyncio.to_thread 將同步的 SDK 呼叫轉為非同步執行
            # 這樣可以避免阻塞事件循環 (event loop)
            response = await asyncio.to_thread(self._call_sdk, request)
            
            # 步驟 2: 解析 API 回應
            result = self._parse_response(response)
            
            # 步驟 3: 記錄結果日誌
            if result.success:
                logger.info("✅ 圖表生成成功")
            else:
                logger.warning(f"⚠️ 圖表生成失敗: {result.error}")
            
            # 步驟 4: 返回結果
            return result
            
        except Exception as e:
            # 捕捉所有未預期的錯誤
            logger.error(f"❌ API 呼叫失敗: {e}")
            
            # 返回失敗結果 (而非拋出例外，確保呼叫端總是能收到回應)
            return ImageGenResult(success=False, error=str(e))
    
    # ------------------------------------------------------------------------
    # 私有方法：呼叫 SDK (Private Method: Call SDK)
    # ------------------------------------------------------------------------
    def _call_sdk(self, request: ImageGenRequest):
        """
        呼叫 Google Gemini SDK 執行實際的圖像生成
        
        功能：
        - 建立聊天會話 (Chat Session)
        - 配置多模態回應 (TEXT + IMAGE)
        - 啟用 Google 搜尋工具輔助生成
        - 發送提示詞並取得回應
        
        參數：
            request (ImageGenRequest): 圖像生成請求物件
        
        回傳：
            Response: Google GenAI SDK 的回應物件
        
        技術細節：
        - 使用 Gemini 3 Pro Image Preview 模型
        - 支援多模態輸出 (文字 + 圖像)
        - 整合 Google 搜尋增強生成品質
        """
        # 建立聊天會話
        chat = self.client.chats.create(
            model=self.model_name,  # 指定使用的模型名稱
            config=types.GenerateContentConfig(
                # 配置回應模式：同時支援文字與圖像輸出
                response_modalities=['TEXT', 'IMAGE'],
                
                # 啟用 Google 搜尋工具
                # 功能：讓 AI 能夠搜尋最新資訊以提升生成品質
                tools=[{"google_search": {}}]
            )
        )
        
        # 發送使用者的提示詞並返回回應
        return chat.send_message(request.prompt)
    
    # ------------------------------------------------------------------------
    # 私有方法：解析回應 (Private Method: Parse Response)
    # ------------------------------------------------------------------------
    def _parse_response(self, response) -> ImageGenResult:
        """
        解析 Google GenAI 的多模態回應
        
        功能：
        - 從回應中提取文字內容
        - 從回應中提取圖像並轉換為 Base64 編碼
        - 處理各種可能的回應格式
        - 提供詳細的錯誤處理與日誌
        
        參數：
            response: Google GenAI SDK 的回應物件
        
        回傳：
            ImageGenResult: 包含解析結果的標準化回應物件
        
        處理流程：
        1. 遍歷回應的所有部分 (parts)
        2. 分別提取文字與圖像內容
        3. 將圖像轉換為 Base64 編碼字串
        4. 組合成標準化的結果物件
        """
        try:
            # 初始化變數
            text_content = None  # 儲存 AI 生成的文字說明
            image_b64 = None     # 儲存 Base64 編碼的圖像資料
            
            # 步驟 1: 遍歷回應的各個部分
            # Google GenAI 的回應可能包含多個 part (文字、圖像等)
            for part in response.parts:
                
                # 步驟 1.1: 處理文字部分
                if part.text is not None:
                    text_content = part.text
                    # 記錄文字內容 (截取前 80 字元)
                    logger.info(f"📝 收到文字回應: {text_content[:80]}...")
                
                # 步驟 1.2: 處理圖像部分
                elif image := part.as_image():
                    # 將 Google GenAI 的 Image 物件轉換為 Base64 字串
                    # 注意：part.as_image() 返回 google.genai.types.Image 物件
                    
                    try:
                        # 步驟 A: 建立臨時檔案
                        # 原因：google.genai.types.Image.save() 只接受檔案路徑
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            tmp_path = tmp_file.name  # 取得臨時檔案路徑
                        
                        # 步驟 B: 將圖像保存到臨時檔案
                        image.save(tmp_path)
                        
                        # 步驟 C: 讀取檔案內容 (二進位模式)
                        with open(tmp_path, 'rb') as f:
                            img_bytes = f.read()
                        
                        # 步驟 D: 刪除臨時檔案 (清理資源)
                        os.unlink(tmp_path)
                        
                        # 步驟 E: 轉換為 Base64 編碼字串
                        # 注意：這裡只返回純 Base64 字串，不包含 data:image/png;base64, 前綴
                        # 原因：前綴會在 renderer 模組中統一添加
                        image_b64 = base64.b64encode(img_bytes).decode('utf-8')
                        
                        # 記錄成功日誌 (顯示圖片大小)
                        logger.info(f"✅ 圖片生成成功 ({len(img_bytes)} bytes)")
                        
                    except Exception as img_err:
                        # 圖像轉換失敗的錯誤處理
                        logger.error(f"⚠️ 圖片轉換失敗: {img_err}")
                        
                        # 記錄除錯資訊 (協助問題排查)
                        logger.info(f"🔍 Image type: {type(image)}, attributes: {dir(image)}")
                        
                        # 重新拋出例外以便外層捕捉
                        raise
            
            # 步驟 2: 根據解析結果建立回應物件
            if image_b64:
                # 成功生成圖像
                return ImageGenResult(
                    success=True,
                    image_base64=image_b64,
                    text_content=text_content
                )
            else:
                # 未生成圖像 (可能只有文字回應)
                logger.warning("⚠️ 未生成圖片")
                return ImageGenResult(
                    success=False,
                    error="未生成圖片",
                    text_content=text_content
                )
            
        except Exception as e:
            # 步驟 3: 處理解析過程中的任何錯誤
            logger.error(f"⚠️ 解析回應時發生錯誤: {e}")
            
            # 記錄除錯資訊 (協助問題排查)
            logger.info(f"📦 Response type: {type(response)}, attributes: {dir(response)}")
            
            # 返回失敗結果
            return ImageGenResult(
                success=False,
                error=f"解析失敗: {e}"
            )


# ============================================================================
# 模組定義完成
# ============================================================================
#
# 擴充指南：
# 1. 新增其他 AI 服務：建立類似的 Provider 類別 (如 DallEProvider)
# 2. 實作共同介面：可定義 BaseProvider 抽象類別統一介面
# 3. 錯誤處理：所有公開方法都應返回結果而非拋出例外
#
# 設計模式：
# - 提供者模式 (Provider Pattern)：封裝外部服務的存取
# - 適配器模式 (Adapter Pattern)：將 Google API 轉換為內部格式
# ============================================================================