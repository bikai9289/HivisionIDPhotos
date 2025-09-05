import argparse
import os
from demo.processor import IDPhotoProcessor
from demo.enhanced_ui import create_enhanced_ui
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
        + "\n"
        + "No existing portrait segmentation model was found, please check the files in the hivision/creator/weights directory."
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

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="HivisionIDPhoto - AI智能证件照制作工具")
    argparser.add_argument(
        "--port", type=int, default=7860, help="服务器端口号"
    )
    argparser.add_argument(
        "--host", type=str, default="0.0.0.0", help="服务器主机地址"
    )
    argparser.add_argument(
        "--root_path",
        type=str,
        default=None,
        help="服务器根路径，默认为None (='/')，例如 '/myapp'",
    )
    argparser.add_argument(
        "--mode",
        type=str,
        default="enhanced",
        choices=["original", "enhanced"],
        help="界面模式：original=原版界面，enhanced=增强版界面"
    )
    
    args = argparser.parse_args()

    processor = IDPhotoProcessor()

    # 根据模式选择不同的UI
    if args.mode == "enhanced":
        demo = create_enhanced_ui(
            processor,
            root_dir,
            HUMAN_MATTING_MODELS_CHOICE,
            FACE_DETECT_MODELS_CHOICE,
            LANGUAGE,
        )
        print("🚀 启动增强版HivisionIDPhoto界面...")
        print("✨ 包含SEO优化、隐私保护、简单/专业模式切换等功能")
    else:
        from demo.ui import create_ui
        demo = create_ui(
            processor,
            root_dir,
            HUMAN_MATTING_MODELS_CHOICE,
            FACE_DETECT_MODELS_CHOICE,
            LANGUAGE,
        )
        print("📷 启动原版HivisionIDPhoto界面...")
    
    # 如果RUN_MODE是Beast，打印已开启野兽模式
    if os.getenv("RUN_MODE") == "beast":
        print("[Beast mode activated.] 已开启野兽模式。")

    print(f"🌐 服务将运行在: http://{args.host}:{args.port}")
    print(f"🔧 界面模式: {args.mode}")
    print("🔒 隐私保护: 图片完全本地处理，不会上传到服务器")
    
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        favicon_path=os.path.join(root_dir, "assets/hivision_logo.png"),
        root_path=args.root_path,
        show_api=False,
    )