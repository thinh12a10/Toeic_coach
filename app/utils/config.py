TEXT_GENERATOR_MODELS = [
    # --- Gemini 2.5 Models (Recommended Default) ---
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro",
    "models/gemini-2.5-flash-lite",
    
    # --- Gemini 3.x Models (Newest Preview) ---
    "models/gemini-3.1-pro-preview",
    "models/gemini-3-pro-preview",
    "models/gemini-3-flash-preview",
    
    # --- Gemini 2.0 Models ---
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-lite-001",
    
    # --- Stable / Alias Links ---
    "models/gemini-flash-latest",
    "models/gemini-pro-latest",
    "models/gemini-flash-lite-latest",
    
    # --- Open Weights Models ---
    "models/gemma-4-26b-a4b-it",
    "models/gemma-4-31b-it",
    
    # --- Audio/TTS Generation Text Capabilities ---
    "models/gemini-2.5-flash-preview-tts",
    "models/gemini-2.5-pro-preview-tts"
]

EVALUATION_MODELS = [
    # --- Nhóm 1: Gemini 2.5 (Tối ưu nhất cho Production, hiểu âm thanh tốt) ---
    "models/gemini-2.5-flash",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.5-pro",
    
    # --- Nhóm 2: Các bản tối ưu hóa cho Giọng nói (TTS/Audio Preview) ---
    "models/gemini-2.5-flash-preview-tts",
    "models/gemini-2.5-pro-preview-tts",
    
    # --- Nhóm 3: Gemini 3.x (Thế hệ mới nhất, xử lý ngữ điệu tốt) ---
    "models/gemini-3.1-pro-preview",
    "models/gemini-3-pro-preview",
    "models/gemini-3-flash-preview",
    
    # --- Nhóm 4: Các Alias ổn định (Trỏ đến bản Flash/Pro mới nhất) ---
    "models/gemini-flash-latest",
    "models/gemini-flash-lite-latest",
    "models/gemini-pro-latest",
    
    # --- Nhóm 5: Gemini 2.0 (Các bản cũ hơn làm phương án fallback cuối cùng) ---
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-lite-001"
]