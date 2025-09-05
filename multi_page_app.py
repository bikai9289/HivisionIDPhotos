import argparse
import os
import gradio as gr
from demo.processor import IDPhotoProcessor
from demo.ui import create_ui
from hivision.creator.choose_handler import HUMAN_MATTING_MODELS

root_dir = os.path.dirname(os.path.abspath(__file__))

# 获取存在的人像分割模型列表
HUMAN_MATTING_MODELS_EXIST = [
    os.path.splitext(file)[0]
    for file in os.listdir(os.path.join(root_dir, "hivision/creator/weights"))
    if file.endswith(".onnx") or file.endswith(".mnn")
]
HUMAN_MATTING_MODELS_CHOICE = [
    model for model in HUMAN_MATTING_MODELS if model in HUMAN_MATTING_MODELS_EXIST
]

if len(HUMAN_MATTING_MODELS_CHOICE) == 0:
    raise ValueError(
        "未找到任何存在的人像分割模型，请检查 hivision/creator/weights 目录下的文件"
    )

FACE_DETECT_MODELS = ["face++ (联网Online API)", "mtcnn"]
FACE_DETECT_MODELS_EXPAND = (
    ["retinaface-resnet50"]
    if os.path.exists(
        os.path.join(
            root_dir, "hivision/creator/retinaface/weights/retinaface-resnet50.onnx"
        )
    )
    else []
)
FACE_DETECT_MODELS_CHOICE = FACE_DETECT_MODELS + FACE_DETECT_MODELS_EXPAND
LANGUAGE = ["zh", "en", "ko", "ja"]

def load_markdown_content(file_path):
    """加载markdown文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "内容加载失败"

def create_passport_page():
    """创建护照签证页面"""
    content = load_markdown_content(os.path.join(root_dir, "demo/assets/passport_page.md"))
    
    with gr.Blocks(
        title="护照签证照片制作专家 - AI IDPhotos",
        head="""
        <head>
            <meta name="description" content="专业护照签证照片制作工具，支持50+国家标准，AI智能抠图换背景，符合各国领事馆要求，避免签证被拒风险。">
            <meta name="keywords" content="护照照片,签证照片,美国签证照片,英国签证照片,护照照片制作,签证照片要求,AI护照照片">
            
            <!-- Open Graph -->
            <meta property="og:title" content="护照签证照片制作专家 - 符合各国标准 | AI IDPhotos">
            <meta property="og:description" content="专业护照签证照片制作，支持美国、英国、加拿大等50+国家标准，AI智能处理，3秒生成合规照片。">
            
            <!-- 结构化数据 -->
            <script type="application/ld+json">
            {
                "@context": "https://schema.org/",
                "@type": "Service",
                "name": "护照签证照片制作",
                "provider": {
                    "@type": "Organization", 
                    "name": "AI IDPhotos"
                },
                "description": "专业护照签证照片制作服务，支持50+国家标准",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "CNY"
                }
            }
            </script>
        </head>
        """,
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="gray"),
        css="""
        .passport-cta {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            padding: 15px 30px !important;
            border-radius: 25px !important;
            font-weight: bold !important;
            text-decoration: none !important;
            display: inline-block !important;
            margin: 10px !important;
            transition: all 0.3s ease !important;
        }
        .passport-cta:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
        }
        """
    ) as passport_demo:
        
        gr.HTML(content)
        
        with gr.Row():
            gr.HTML("""
            <div style="text-align: center; padding: 30px;">
                <a href="/" class="passport-cta">🚀 立即制作护照照片</a>
                <a href="/resume" class="passport-cta" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;">💼 制作简历照片</a>
            </div>
            """)
    
    return passport_demo

def create_resume_page():
    """创建求职简历页面"""
    content = load_markdown_content(os.path.join(root_dir, "demo/assets/resume_page.md"))
    
    with gr.Blocks(
        title="求职简历照片制作专家 - 提升面试成功率 | AI IDPhotos", 
        head="""
        <head>
            <meta name="description" content="专业简历照片制作工具，AI智能美化，多行业风格选择，提升面试成功率60%，适用于金融、互联网、创意设计等各行业。">
            <meta name="keywords" content="简历照片,求职照片,面试照片,职业照片,简历头像,LinkedIn照片,专业形象照片">
            
            <!-- Open Graph -->
            <meta property="og:title" content="求职简历照片制作专家 - 提升面试成功率 | AI IDPhotos">
            <meta property="og:description" content="AI智能制作专业简历照片，多行业风格，提升面试成功率，完全免费使用。">
            
            <!-- 结构化数据 -->
            <script type="application/ld+json">
            {
                "@context": "https://schema.org/",
                "@type": "Service",
                "name": "简历照片制作",
                "provider": {
                    "@type": "Organization",
                    "name": "AI IDPhotos"
                },
                "description": "专业简历照片制作服务，提升面试成功率",
                "offers": {
                    "@type": "Offer",
                    "price": "0", 
                    "priceCurrency": "CNY"
                }
            }
            </script>
        </head>
        """,
        theme=gr.themes.Soft(primary_hue="green", secondary_hue="gray"),
        css="""
        .resume-cta {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            color: white !important;
            padding: 15px 30px !important;
            border-radius: 25px !important;
            font-weight: bold !important;
            text-decoration: none !important;
            display: inline-block !important;
            margin: 10px !important;
            transition: all 0.3s ease !important;
        }
        .resume-cta:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(17,153,142,0.4) !important;
        }
        """
    ) as resume_demo:
        
        gr.HTML(content)
        
        with gr.Row():
            gr.HTML("""
            <div style="text-align: center; padding: 30px;">
                <a href="/" class="resume-cta">🚀 立即制作简历照片</a>
                <a href="/passport" class="resume-cta" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;">🛂 制作护照照片</a>
            </div>
            """)
    
    return resume_demo

def create_main_app():
    """创建主应用"""
    processor = IDPhotoProcessor()
    
    return create_ui(
        processor,
        root_dir,
        HUMAN_MATTING_MODELS_CHOICE,
        FACE_DETECT_MODELS_CHOICE,
        LANGUAGE,
    )

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--port", type=int, default=7860, help="The port number of the server")
    argparser.add_argument("--host", type=str, default="127.0.0.1", help="The host of the server")
    argparser.add_argument("--root_path", type=str, default=None, help="The root path of the server")
    args = argparser.parse_args()

    # 创建多页面应用
    main_app = create_main_app()
    passport_app = create_passport_page()
    resume_app = create_resume_page()

    # 使用 Gradio 的 mount_gradio_app 功能来创建多页面
    # 注意：这里需要使用 FastAPI 来实现真正的多页面路由
    # 当前版本先展示主应用，后续可以扩展为完整的多页面系统
    
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")
    
    # 启动主应用
    main_app.launch(
        server_name=args.host,
        server_port=args.port,
        favicon_path=os.path.join(root_dir, "assets/hivision_logo.png"),
        root_path=args.root_path,
        show_api=False,
    )