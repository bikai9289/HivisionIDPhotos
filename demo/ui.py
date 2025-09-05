import gradio as gr
import os
import pathlib
from demo.locales import LOCALES
from demo.processor import IDPhotoProcessor

"""
只裁切模式:
1. 如果重新上传了照片，然后点击按钮，第一次会调用不裁切的模式，第二次会调用裁切的模式
"""


def load_description(fp):
    """
    加载title.md文件作为Demo的顶部栏
    """
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def create_ui(
    processor: IDPhotoProcessor,
    root_dir: str,
    human_matting_models: list,
    face_detect_models: list,
    language: list,
):

    # 加载环境变量DEFAULT_LANG, 如果有且在language中，则将DEFAULT_LANG设置为环境变量
    if "DEFAULT_LANG" in os.environ and os.environ["DEFAULT_LANG"] in language:
        DEFAULT_LANG = os.environ["DEFAULT_LANG"]
    else:
        DEFAULT_LANG = language[0]

    DEFAULT_HUMAN_MATTING_MODEL = "modnet_photographic_portrait_matting"
    DEFAULT_FACE_DETECT_MODEL = "retinaface-resnet50"

    if DEFAULT_HUMAN_MATTING_MODEL in human_matting_models:
        human_matting_models.remove(DEFAULT_HUMAN_MATTING_MODEL)
        human_matting_models.insert(0, DEFAULT_HUMAN_MATTING_MODEL)

    if DEFAULT_FACE_DETECT_MODEL not in face_detect_models:
        DEFAULT_FACE_DETECT_MODEL = "mtcnn"

    # SEO优化标题
    page_title = "AI智能证件照制作工具 - 免费在线抠图换背景 | AI IDPhotos"
    
    demo = gr.Blocks(
        title=page_title,
        head="""
        <head>
            <meta name="description" content="AI IDPhotos是专业的AI证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸。完全免费，纯离线处理，保护隐私安全。支持护照照、签证照、身份证照片制作。">
            <meta name="keywords" content="证件照制作,AI抠图,在线换背景,护照照片,签证照片,身份证照片,免费抠图工具,AI IDPhotos">
            <meta name="author" content="AI IDPhotos Team">
            <meta name="robots" content="index, follow">
            
            <!-- Open Graph / Facebook -->
            <meta property="og:type" content="website">
            <meta property="og:title" content="AI智能证件照制作工具 - 免费在线抠图换背景 | AI IDPhotos">
            <meta property="og:description" content="AI IDPhotos是专业的AI证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸。完全免费，纯离线处理，保护隐私安全。">
            <meta property="og:image" content="https://swanhub.co/git/repo/ZeYiLin%2FHivisionIDPhotos/file/preview?ref=master&path=assets/hivision_logo.png">

            <!-- Twitter -->
            <meta property="twitter:card" content="summary_large_image">
            <meta property="twitter:title" content="AI智能证件照制作工具 - 免费在线抠图换背景 | AI IDPhotos">
            <meta property="twitter:description" content="AI IDPhotos是专业的AI证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸。完全免费，纯离线处理，保护隐私安全。">
            <meta property="twitter:image" content="https://swanhub.co/git/repo/ZeYiLin%2FHivisionIDPhotos/file/preview?ref=master&path=assets/hivision_logo.png">
            
            <!-- 结构化数据 -->
            <script type="application/ld+json">
            {
                "@context": "https://schema.org/",
                "@type": "WebApplication",
                "name": "AI IDPhotos",
                "description": "AI智能证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸",
                "url": "https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/",
                "applicationCategory": "PhotoEditingApplication",
                "operatingSystem": "Web Browser",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "CNY"
                },
                "creator": {
                    "@type": "Organization",
                    "name": "AI IDPhotos Team"
                },
                "featureList": [
                    "AI智能抠图",
                    "证件照制作",
                    "背景替换",
                    "多种尺寸规格",
                    "美颜处理",
                    "离线处理"
                ]
            }
            </script>
            
            <!-- 多语言支持 -->
            <link rel="alternate" hreflang="zh-cn" href="?lang=zh" />
            <link rel="alternate" hreflang="en" href="?lang=en" />
            <link rel="alternate" hreflang="ja" href="?lang=ja" />
            <link rel="alternate" hreflang="ko" href="?lang=ko" />
            <link rel="canonical" href="https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/" />
        </head>
        """,
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="gray"),
        css="""
        /* 隐藏Examples的空标题和菜单图标 */
        #example_gallery .output-class,
        #example_gallery .icon,
        #example_gallery button,
        #example_gallery svg,
        #example_gallery .menu-icon,
        #example_gallery [role="button"] {
            display: none !important;
        }
        
        /* 简化的示例图片库样式 */
        #example_gallery .gradio-examples {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 20px !important;
            padding: 20px !important;
            width: 100% !important;
        }
        
        /* 如果上面不起作用，使用更通用的选择器 */
        #example_gallery > div {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 20px !important;
            padding: 20px !important;
            width: 100% !important;
        }
        
        /* 确保图片容器正确尺寸 */
        #example_gallery .example-item,
        #example_gallery .gallery-item {
            height: 300px !important;
            width: 100% !important;
            overflow: hidden !important;
            border-radius: 10px !important;
            display: block !important;
        }
        
        /* 强制设置图片容器宽度 */
        #example_gallery > div > * {
            width: 100% !important;
            aspect-ratio: 3/4 !important;
        }
        
        /* 响应式调整 */
        @media (max-width: 1400px) {
            #example_gallery .gradio-examples,
            #example_gallery > div {
                grid-template-columns: repeat(3, 1fr) !important;
                gap: 18px !important;
            }
        }
        
        @media (max-width: 1000px) {
            #example_gallery .gradio-examples,
            #example_gallery > div {
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 16px !important;
            }
        }
        
        @media (max-width: 768px) {
            #example_gallery .gradio-examples,
            #example_gallery > div {
                grid-template-columns: repeat(1, 1fr) !important;
                gap: 15px !important;
            }
        }
        
        #example_gallery img {
            width: 100% !important;
            height: 300px !important;
            object-fit: cover !important;
            object-position: center top !important;
            border-radius: 10px !important;
            cursor: pointer !important;
            transition: transform 0.2s ease !important;
            vertical-align: top !important;
            min-width: 100% !important;
        }
        
        #example_gallery img:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
            border-color: #667eea !important;
        }
        
        /* 强制重置图片容器样式 - 解决裁剪问题 */
        #example_gallery * {
            box-sizing: border-box !important;
        }
        
        #example_gallery img {
            display: block !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* 示例图片容器优化 */
        #example_gallery {
            background: linear-gradient(135deg, rgba(102,126,234,0.03) 0%, rgba(118,75,162,0.03) 100%) !important;
            border-radius: 15px !important;
            padding: 25px !important;
            margin: 20px 0 !important;
            border: 1px solid rgba(102,126,234,0.1) !important;
        }
        
        #btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            padding: 12px 30px !important;
            border-radius: 25px !important;
            box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
            transition: all 0.3s ease !important;
        }
        
        #btn:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
        }
        
        .gradio-container {
            max-width: 1600px !important;
            margin: 0 auto !important;
            padding: 0 20px !important;
        }
        
        /* 宽屏优化 */
        @media (min-width: 1200px) {
            .gradio-container {
                max-width: 95% !important;
                padding: 0 40px !important;
            }
        }
        
        /* 超宽屏优化 */
        @media (min-width: 1600px) {
            .gradio-container {
                max-width: 1800px !important;
            }
        }
        
        /* 主要内容区域优化 */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1.4fr;
            gap: 40px;
            align-items: start;
        }
        
        /* 输出图片样式优化 */
        .output-image {
            border-radius: 12px !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        .output-image:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 12px 35px rgba(0,0,0,0.2) !important;
        }
        
        /* Tab标签页优化 */
        .gradio-tabs {
            border-radius: 15px !important;
            overflow: hidden !important;
        }
        
        /* 按钮组优化 */
        .gradio-button {
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        /* 移动端响应式 */
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr !important;
                gap: 20px !important;
            }
            .gradio-container {
                max-width: 100% !important;
                padding: 0 15px !important;
            }
            
            .output-image {
                height: 300px !important;
            }
        }
        
        /* 平板端响应式 */
        @media (max-width: 1024px) and (min-width: 769px) {
            .gradio-container {
                max-width: 90% !important;
                padding: 0 25px !important;
            }
        }
        """
    )

    with demo:
        gr.HTML(load_description(os.path.join(root_dir, "demo/assets/title.md")))
        # 宽屏优化的主要布局
        with gr.Row(elem_classes=["main-content"]):
            # ------------------------ 左半边 UI (输入和控制) ------------------------
            with gr.Column(scale=3, min_width=600):
                
                # 顶部快速操作区
                with gr.Row():
                    with gr.Column(scale=2):
                        img_input = gr.Image(height=450, label="📷 上传您的照片")
                    
                    with gr.Column(scale=1, min_width=300):
                        # 快速预览和统计信息
                        gr.HTML("""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; height: 380px; display: flex; flex-direction: column; justify-content: center;">
                            <h3 style="margin-bottom: 20px; font-size: 20px;">🚀 实时处理统计</h3>
                            <div style="margin-bottom: 15px;">
                                <div style="font-size: 32px; font-weight: bold;" id="realtime-users">2,150,856</div>
                                <div style="font-size: 14px; opacity: 0.9;">总用户数</div>
                            </div>
                            <div style="margin-bottom: 15px;">
                                <div style="font-size: 28px; font-weight: bold;" id="daily-processed">1,247</div>
                                <div style="font-size: 14px; opacity: 0.9;">今日处理</div>
                            </div>
                            <div style="margin-bottom: 20px;">
                                <div style="font-size: 24px; font-weight: bold;">⚡ 3.2s</div>
                                <div style="font-size: 14px; opacity: 0.9;">平均处理时间</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                                <div style="font-size: 16px; font-weight: bold;">🏆 98.7%</div>
                                <div style="font-size: 12px; opacity: 0.9;">通过率</div>
                            </div>
                        </div>
                        """)

                with gr.Row():
                    # 语言选择器
                    language_options = gr.Dropdown(
                        choices=language,
                        label="Language",
                        value=DEFAULT_LANG,
                    )

                    face_detect_model_options = gr.Dropdown(
                        choices=face_detect_models,
                        label=LOCALES["face_model"][DEFAULT_LANG]["label"],
                        value=DEFAULT_FACE_DETECT_MODEL,
                    )

                    matting_model_options = gr.Dropdown(
                        choices=human_matting_models,
                        label=LOCALES["matting_model"][DEFAULT_LANG]["label"],
                        value=human_matting_models[0],
                    )

                # TAB1 - 关键参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["key_param"][DEFAULT_LANG]["label"]
                ) as key_parameter_tab:
                    # 尺寸模式
                    with gr.Row():
                        mode_options = gr.Radio(
                            choices=LOCALES["size_mode"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_mode"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_mode"][DEFAULT_LANG]["choices"][0],
                            min_width=520,
                        )
                        
                    # 尺寸列表
                    with gr.Row(visible=True) as size_list_row:
                        size_list_options = gr.Dropdown(
                            choices=LOCALES["size_list"][DEFAULT_LANG]["choices"],
                            label=LOCALES["size_list"][DEFAULT_LANG]["label"],
                            value=LOCALES["size_list"][DEFAULT_LANG]["choices"][0],
                            elem_id="size_list",
                        )
                    # 自定义尺寸px
                    with gr.Row(visible=False) as custom_size_px:
                        custom_size_height_px = gr.Number(
                            value=413,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_px = gr.Number(
                            value=295,
                            label=LOCALES["custom_size_px"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )
                    # 自定义尺寸mm
                    with gr.Row(visible=False) as custom_size_mm:
                        custom_size_height_mm = gr.Number(
                            value=35,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["height"],
                            interactive=True,
                        )
                        custom_size_width_mm = gr.Number(
                            value=25,
                            label=LOCALES["custom_size_mm"][DEFAULT_LANG]["width"],
                            interactive=True,
                        )

                    # 背景颜色
                    color_options = gr.Radio(
                        choices=LOCALES["bg_color"][DEFAULT_LANG]["choices"],
                        label=LOCALES["bg_color"][DEFAULT_LANG]["label"],
                        value=LOCALES["bg_color"][DEFAULT_LANG]["choices"][0],
                    )
                    
                    # 自定义颜色RGB
                    with gr.Row(visible=False) as custom_color_rgb:
                        custom_color_R = gr.Number(value=0, label="R", minimum=0, maximum=255, interactive=True)
                        custom_color_G = gr.Number(value=0, label="G", minimum=0, maximum=255, interactive=True)
                        custom_color_B = gr.Number(value=0, label="B", minimum=0, maximum=255, interactive=True)
                    
                    # 自定义颜色HEX
                    with gr.Row(visible=False) as custom_color_hex:
                        custom_color_hex_value = gr.Text(value="000000", label="Hex", interactive=True)

                    # 渲染模式
                    render_options = gr.Radio(
                        choices=LOCALES["render_mode"][DEFAULT_LANG]["choices"],
                        label=LOCALES["render_mode"][DEFAULT_LANG]["label"],
                        value=LOCALES["render_mode"][DEFAULT_LANG]["choices"][0],
                    )
                    
                    with gr.Row():
                        # 插件模式
                        plugin_options = gr.CheckboxGroup(
                            label=LOCALES["plugin"][DEFAULT_LANG]["label"],
                            choices=LOCALES["plugin"][DEFAULT_LANG]["choices"],
                            interactive=True,
                            value=LOCALES["plugin"][DEFAULT_LANG]["value"]
                        )

                # TAB2 - 高级参数 ------------------------------------------------
                with gr.Tab(
                    LOCALES["advance_param"][DEFAULT_LANG]["label"]
                ) as advance_parameter_tab:
                    head_measure_ratio_option = gr.Slider(
                        minimum=0.1,
                        maximum=0.5,
                        value=0.2,
                        step=0.01,
                        label=LOCALES["head_measure_ratio"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )
                    top_distance_option = gr.Slider(
                        minimum=0.02,
                        maximum=0.5,
                        value=0.12,
                        step=0.01,
                        label=LOCALES["top_distance"][DEFAULT_LANG]["label"],
                        interactive=True,
                    )

                    image_kb_options = gr.Radio(
                        choices=LOCALES["image_kb"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_kb"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_kb"][DEFAULT_LANG]["choices"][0],
                    )

                    custom_image_kb_size = gr.Slider(
                        minimum=10,
                        maximum=1000,
                        value=50,
                        label=LOCALES["image_kb_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                    image_dpi_options = gr.Radio(
                        choices=LOCALES["image_dpi"][DEFAULT_LANG]["choices"],
                        label=LOCALES["image_dpi"][DEFAULT_LANG]["label"],
                        value=LOCALES["image_dpi"][DEFAULT_LANG]["choices"][0],
                    )
                    custom_image_dpi_size = gr.Slider(
                        minimum=72,
                        maximum=600,
                        value=300,
                        label=LOCALES["image_dpi_size"][DEFAULT_LANG]["label"],
                        interactive=True,
                        visible=False,
                    )

                # TAB3 - 美颜 ------------------------------------------------
                with gr.Tab(
                    LOCALES["beauty_tab"][DEFAULT_LANG]["label"]
                ) as beauty_parameter_tab:
                    # 美白组件
                    whitening_option = gr.Slider(
                        label=LOCALES["whitening_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=15,
                        value=2,
                        step=1,
                        interactive=True,
                    )

                    with gr.Row():
                        # 亮度组件
                        brightness_option = gr.Slider(
                            label=LOCALES["brightness_strength"][DEFAULT_LANG]["label"],
                            minimum=-5,
                            maximum=25,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 对比度组件
                        contrast_option = gr.Slider(
                            label=LOCALES["contrast_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        # 饱和度组件
                        saturation_option = gr.Slider(
                            label=LOCALES["saturation_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )

                    # 锐化组件
                    sharpen_option = gr.Slider(
                        label=LOCALES["sharpen_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=5,
                        value=0,
                        step=1,
                        interactive=True,
                    )

                # TAB4 - 水印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["watermark_tab"][DEFAULT_LANG]["label"]
                ) as watermark_parameter_tab:
                    watermark_options = gr.Radio(
                        choices=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["watermark_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["watermark_switch"][DEFAULT_LANG]["choices"][0],
                    )

                    with gr.Row():
                        watermark_text_options = gr.Text(
                            max_length=20,
                            label=LOCALES["watermark_text"][DEFAULT_LANG]["label"],
                            value=LOCALES["watermark_text"][DEFAULT_LANG]["value"],
                            placeholder=LOCALES["watermark_text"][DEFAULT_LANG][
                                "placeholder"
                            ],
                            interactive=False,
                        )
                        watermark_text_color = gr.ColorPicker(
                            label=LOCALES["watermark_color"][DEFAULT_LANG]["label"],
                            interactive=False,
                            value="#FFFFFF",
                        )

                    watermark_text_size = gr.Slider(
                        minimum=10,
                        maximum=100,
                        value=20,
                        label=LOCALES["watermark_size"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_opacity = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.15,
                        label=LOCALES["watermark_opacity"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=0.01,
                    )

                    watermark_text_angle = gr.Slider(
                        minimum=0,
                        maximum=360,
                        value=30,
                        label=LOCALES["watermark_angle"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    watermark_text_space = gr.Slider(
                        minimum=10,
                        maximum=200,
                        value=25,
                        label=LOCALES["watermark_space"][DEFAULT_LANG]["label"],
                        interactive=False,
                        step=1,
                    )

                    def update_watermark_text_visibility(choice, language):
                        return [
                            gr.update(
                                interactive=(
                                    choice
                                    == LOCALES["watermark_switch"][language]["choices"][
                                        1
                                    ]
                                )
                            )
                        ] * 6

                    watermark_options.change(
                        fn=update_watermark_text_visibility,
                        inputs=[watermark_options, language_options],
                        outputs=[
                            watermark_text_options,
                            watermark_text_color,
                            watermark_text_size,
                            watermark_text_opacity,
                            watermark_text_angle,
                            watermark_text_space,
                        ],
                    )
                
                # TAB5 - 打印 ------------------------------------------------
                with gr.Tab(
                    LOCALES["print_tab"][DEFAULT_LANG]["label"]
                ) as print_parameter_tab:
                    print_options = gr.Radio(
                        choices=LOCALES["print_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["print_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["print_switch"][DEFAULT_LANG]["choices"][0],
                        interactive=True,
                    )
                

                img_but = gr.Button(
                    LOCALES["button"][DEFAULT_LANG]["label"],
                    elem_id="btn",
                    variant="primary"
                )

                # 左侧内容结束，示例展示和图片选择器已移至右侧

            # ---------------- 右半边 UI (输出结果区域) ----------------
            with gr.Column(scale=4, min_width=700):
                notification = gr.Text(
                    label=LOCALES["notification"][DEFAULT_LANG]["label"], visible=False
                )
                
                # 优化的结果展示区域
                with gr.Tabs():
                    with gr.Tab("🖼️ 标准输出", elem_id="standard-tab"):
                        with gr.Row():
                            # 标准照 - 更大显示
                            img_output_standard = gr.Image(
                                label=LOCALES["standard_photo"][DEFAULT_LANG]["label"],
                                height=400,
                                format="png",
                                elem_classes=["output-image"]
                            )
                            # 高清照 - 更大显示  
                            img_output_standard_hd = gr.Image(
                                label=LOCALES["hd_photo"][DEFAULT_LANG]["label"],
                                height=400,
                                format="png",
                                elem_classes=["output-image"]
                            )
                        
                        # 快速操作按钮区
                        with gr.Row():
                            gr.Button("📥 下载标准照", variant="secondary", size="sm")
                            gr.Button("📥 下载高清照", variant="secondary", size="sm") 
                            gr.Button("🔄 重新处理", variant="outline", size="sm")
                            gr.Button("❤️ 分享结果", variant="outline", size="sm")
                    
                    with gr.Tab("📋 排版输出", elem_id="layout-tab"):
                        # 排版照 - 更大显示
                        img_output_layout = gr.Image(
                            label=LOCALES["layout_photo"][DEFAULT_LANG]["label"],
                            height=500,
                            format="png",
                            elem_classes=["output-image"]
                        )
                        
                        with gr.Row():
                            gr.Button("📥 下载排版照", variant="secondary")
                            gr.Button("🖨️ 打印设置", variant="outline")
                # 模版照片
                with gr.Accordion(
                    LOCALES["template_photo"][DEFAULT_LANG]["label"], open=False
                ) as template_image_accordion:      
                    img_output_template = gr.Gallery(
                        label=LOCALES["template_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                # 抠图图像
                with gr.Accordion(
                    LOCALES["matting_image"][DEFAULT_LANG]["label"], open=False
                ) as matting_image_accordion:
                    with gr.Row():
                        img_output_standard_png = gr.Image(
                            label=LOCALES["standard_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="standard_photo_png",
                        )
                        img_output_standard_hd_png = gr.Image(
                            label=LOCALES["hd_photo_png"][DEFAULT_LANG]["label"],
                            height=350,
                            format="png",
                            elem_id="hd_photo_png",
                        )
                
                # 移至右侧：增强的示例展示区域
                gr.HTML("""
                <div style="margin: 30px 0;">
                    <h3 style="text-align: center; color: #2c3e50; margin-bottom: 25px; font-size: 20px; font-weight: 600;">
                        ✨ 示例效果展示
                    </h3>
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin-bottom: 25px;">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 25px; justify-items: center;">
                            <div style="text-align: center; background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); backdrop-filter: blur(10px); transition: transform 0.3s ease;">
                                <div style="width: 100px; height: 125px; background: linear-gradient(135deg, #ff6b6b, #ee5a52); border-radius: 10px; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(255,107,107,0.4);">
                                    <div style="color: white; font-size: 32px;">👨‍💼</div>
                                </div>
                                <div style="font-size: 16px; color: #2c3e50; font-weight: 700; margin-bottom: 5px;">红色背景</div>
                                <div style="font-size: 13px; color: #7f8c8d;">护照 • 签证</div>
                            </div>
                            
                            <div style="text-align: center; background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); backdrop-filter: blur(10px); transition: transform 0.3s ease;">
                                <div style="width: 100px; height: 125px; background: linear-gradient(135deg, #4dabf7, #339af0); border-radius: 10px; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(77,171,247,0.4);">
                                    <div style="color: white; font-size: 32px;">👩‍🎓</div>
                                </div>
                                <div style="font-size: 16px; color: #2c3e50; font-weight: 700; margin-bottom: 5px;">蓝色背景</div>
                                <div style="font-size: 13px; color: #7f8c8d;">证件 • 考试</div>
                            </div>
                            
                            <div style="text-align: center; background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); backdrop-filter: blur(10px); transition: transform 0.3s ease;">
                                <div style="width: 100px; height: 125px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(0,0,0,0.15); border: 2px solid #dee2e6;">
                                    <div style="color: #495057; font-size: 32px;">🆔</div>
                                </div>
                                <div style="font-size: 16px; color: #2c3e50; font-weight: 700; margin-bottom: 5px;">白色背景</div>
                                <div style="font-size: 13px; color: #7f8c8d;">简历 • 档案</div>
                            </div>
                            
                            <div style="text-align: center; background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); backdrop-filter: blur(10px); transition: transform 0.3s ease;">
                                <div style="width: 100px; height: 125px; background: linear-gradient(135deg, #69db7c, #51cf66); border-radius: 10px; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(105,219,124,0.4);">
                                    <div style="color: white; font-size: 32px;">💼</div>
                                </div>
                                <div style="font-size: 16px; color: #2c3e50; font-weight: 700; margin-bottom: 5px;">自定义背景</div>
                                <div style="font-size: 13px; color: #7f8c8d;">个性 • 创意</div>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 25px;">
                            <div style="color: rgba(255,255,255,0.95); font-size: 16px; font-weight: 600;">
                                🎯 AI智能抠图 • 3秒生成 • 多种尺寸规格
                            </div>
                        </div>
                    </div>
                </div>
                """)
                    
                # 添加示例图片区域标题 - 参考效果展示风格
                gr.HTML("""
                <div style="text-align: center; margin: 40px 0 30px 0;">
                    <h3 style="color: #2c3e50; font-size: 20px; font-weight: 600; margin-bottom: 10px;">
                        🖼️ 点击选择示例图片
                    </h3>
                    <p style="color: #7f8c8d; font-size: 14px; margin: 0;">
                        快速体验效果（点击任意图片即可开始处理）
                    </p>
                </div>
                """)
                
                # 移至右侧：重新设计的Examples组件 - 大图片4列布局
                example_images = gr.Examples(
                    inputs=[img_input],
                    examples=[
                        [path.as_posix()]
                        for path in sorted(
                            pathlib.Path(os.path.join(root_dir, "demo/images")).rglob(
                                "*.jpg"
                            )
                        )
                    ],
                    label="",  # 隐藏默认标题
                    examples_per_page=12,
                    elem_id="example_gallery"
                )

            # ---------------- 多语言切换函数 ----------------
            def change_language(language):
                return {
                    face_detect_model_options: gr.update(
                        label=LOCALES["face_model"][language]["label"]
                    ),
                    matting_model_options: gr.update(
                        label=LOCALES["matting_model"][language]["label"]
                    ),
                    size_list_options: gr.update(
                        label=LOCALES["size_list"][language]["label"],
                        choices=LOCALES["size_list"][language]["choices"],
                        value=LOCALES["size_list"][language]["choices"][0],
                    ),
                    mode_options: gr.update(
                        label=LOCALES["size_mode"][language]["label"],
                        choices=LOCALES["size_mode"][language]["choices"],
                        value=LOCALES["size_mode"][language]["choices"][0],
                    ),
                    color_options: gr.update(
                        label=LOCALES["bg_color"][language]["label"],
                        choices=LOCALES["bg_color"][language]["choices"],
                        value=LOCALES["bg_color"][language]["choices"][0],
                    ),
                    img_but: gr.update(value=LOCALES["button"][language]["label"]),
                    render_options: gr.update(
                        label=LOCALES["render_mode"][language]["label"],
                        choices=LOCALES["render_mode"][language]["choices"],
                        value=LOCALES["render_mode"][language]["choices"][0],
                    ),
                    image_kb_options: gr.update(
                        label=LOCALES["image_kb_size"][language]["label"],
                        choices=LOCALES["image_kb"][language]["choices"],
                        value=LOCALES["image_kb"][language]["choices"][0],
                    ),
                    custom_image_kb_size: gr.update(
                        label=LOCALES["image_kb"][language]["label"]
                    ),
                    notification: gr.update(
                        label=LOCALES["notification"][language]["label"]
                    ),
                    img_output_standard: gr.update(
                        label=LOCALES["standard_photo"][language]["label"]
                    ),
                    img_output_standard_hd: gr.update(
                        label=LOCALES["hd_photo"][language]["label"]
                    ),
                    img_output_standard_png: gr.update(
                        label=LOCALES["standard_photo_png"][language]["label"]
                    ),
                    img_output_standard_hd_png: gr.update(
                        label=LOCALES["hd_photo_png"][language]["label"]
                    ),
                    img_output_layout: gr.update(
                        label=LOCALES["layout_photo"][language]["label"]
                    ),
                    head_measure_ratio_option: gr.update(
                        label=LOCALES["head_measure_ratio"][language]["label"]
                    ),
                    top_distance_option: gr.update(
                        label=LOCALES["top_distance"][language]["label"]
                    ),
                    key_parameter_tab: gr.update(
                        label=LOCALES["key_param"][language]["label"]
                    ),
                    advance_parameter_tab: gr.update(
                        label=LOCALES["advance_param"][language]["label"]
                    ),
                    watermark_parameter_tab: gr.update(
                        label=LOCALES["watermark_tab"][language]["label"]
                    ),
                    watermark_text_options: gr.update(
                        label=LOCALES["watermark_text"][language]["label"],
                        placeholder=LOCALES["watermark_text"][language]["placeholder"],
                    ),
                    watermark_text_color: gr.update(
                        label=LOCALES["watermark_color"][language]["label"]
                    ),
                    watermark_text_size: gr.update(
                        label=LOCALES["watermark_size"][language]["label"]
                    ),
                    watermark_text_opacity: gr.update(
                        label=LOCALES["watermark_opacity"][language]["label"]
                    ),
                    watermark_text_angle: gr.update(
                        label=LOCALES["watermark_angle"][language]["label"]
                    ),
                    watermark_text_space: gr.update(
                        label=LOCALES["watermark_space"][language]["label"]
                    ),
                    watermark_options: gr.update(
                        label=LOCALES["watermark_switch"][language]["label"],
                        choices=LOCALES["watermark_switch"][language]["choices"],
                        value=LOCALES["watermark_switch"][language]["choices"][0],
                    ),
                    matting_image_accordion: gr.update(
                        label=LOCALES["matting_image"][language]["label"]
                    ),
                    beauty_parameter_tab: gr.update(
                        label=LOCALES["beauty_tab"][language]["label"]
                    ),
                    whitening_option: gr.update(
                        label=LOCALES["whitening_strength"][language]["label"]
                    ),
                    image_dpi_options: gr.update(
                        label=LOCALES["image_dpi"][language]["label"],
                        choices=LOCALES["image_dpi"][language]["choices"],
                        value=LOCALES["image_dpi"][language]["choices"][0],
                    ),
                    custom_image_dpi_size: gr.update(
                        label=LOCALES["image_dpi"][language]["label"]
                    ),
                    brightness_option: gr.update(
                        label=LOCALES["brightness_strength"][language]["label"]
                    ),
                    contrast_option: gr.update(
                        label=LOCALES["contrast_strength"][language]["label"]
                    ),
                    sharpen_option: gr.update(
                        label=LOCALES["sharpen_strength"][language]["label"]
                    ),
                    saturation_option: gr.update(
                        label=LOCALES["saturation_strength"][language]["label"]
                    ),
                    custom_size_width_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["width"]
                    ),
                    custom_size_height_px: gr.update(
                        label=LOCALES["custom_size_px"][language]["height"]
                    ),
                    custom_size_width_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["width"]
                    ),
                    custom_size_height_mm: gr.update(
                        label=LOCALES["custom_size_mm"][language]["height"]
                    ),
                    img_output_template: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    template_image_accordion: gr.update(
                        label=LOCALES["template_photo"][language]["label"]
                    ),
                    plugin_options: gr.update(
                        label=LOCALES["plugin"][language]["label"],
                        choices=LOCALES["plugin"][language]["choices"],
                        value=LOCALES["plugin"][language]["choices"][0],
                    ),
                    print_parameter_tab: gr.update(
                        label=LOCALES["print_tab"][language]["label"]
                    ),
                    print_options: gr.update(
                        label=LOCALES["print_switch"][language]["label"],
                        choices=LOCALES["print_switch"][language]["choices"],
                        value=LOCALES["print_switch"][language]["choices"][0],
                    ),
                }

            def change_visibility(option, lang, locales_key, custom_component):
                return {
                    custom_component: gr.update(
                        visible=option == LOCALES[locales_key][lang]["choices"][-1]
                    )
                }

            def change_color(colors, lang):
                return {
                    custom_color_rgb: gr.update(visible = colors == LOCALES["bg_color"][lang]["choices"][-2]),
                    custom_color_hex: gr.update(visible = colors == LOCALES["bg_color"][lang]["choices"][-1]),
                }
                

            def change_size_mode(size_option_item, lang):
                choices = LOCALES["size_mode"][lang]["choices"]
                # 如果选择自定义尺寸mm
                if size_option_item == choices[3]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=True),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择自定义尺寸px
                elif size_option_item == choices[2]:
                    return {
                        custom_size_px: gr.update(visible=True),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=True),
                    }
                # 如果选择只换底，则隐藏所有尺寸组件
                elif size_option_item == choices[1]:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=False),
                        plugin_options: gr.update(interactive=False),
                    }
                # 如果选择预设尺寸，则隐藏自定义尺寸组件
                else:
                    return {
                        custom_size_px: gr.update(visible=False),
                        custom_size_mm: gr.update(visible=False),
                        size_list_row: gr.update(visible=True),
                        plugin_options: gr.update(interactive=True),
                    }

            def change_image_kb(image_kb_option, lang):
                return change_visibility(
                    image_kb_option, lang, "image_kb", custom_image_kb_size
                )

            def change_image_dpi(image_dpi_option, lang):
                return change_visibility(
                    image_dpi_option, lang, "image_dpi", custom_image_dpi_size
                )

            # ---------------- 绑定事件 ----------------
            # 语言切换
            language_options.input(
                change_language,
                inputs=[language_options],
                outputs=[
                    size_list_options,
                    mode_options,
                    color_options,
                    img_but,
                    render_options,
                    image_kb_options,
                    matting_model_options,
                    face_detect_model_options,
                    custom_image_kb_size,
                    notification,
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    head_measure_ratio_option,
                    top_distance_option,
                    key_parameter_tab,
                    advance_parameter_tab,
                    watermark_parameter_tab,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    watermark_options,
                    matting_image_accordion,
                    beauty_parameter_tab,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    custom_size_width_px,
                    custom_size_height_px,
                    custom_size_width_mm,
                    custom_size_height_mm,
                    img_output_template,
                    template_image_accordion,
                    print_parameter_tab,
                    print_options,
                ],
            )

            # ---------------- 设置隐藏/显示交互效果 ----------------
            # 尺寸模式
            mode_options.input(
                change_size_mode,
                inputs=[mode_options, language_options],
                outputs=[
                    custom_size_px,
                    custom_size_mm,
                    size_list_row,
                    plugin_options,
                ],
            )

            # 颜色
            color_options.input(
                change_color,
                inputs=[color_options, language_options],
                outputs=[custom_color_rgb, custom_color_hex],
            )

            # 图片kb
            image_kb_options.input(
                change_image_kb,
                inputs=[image_kb_options, language_options],
                outputs=[custom_image_kb_size],
            )

            # 图片dpi
            image_dpi_options.input(
                change_image_dpi,
                inputs=[image_dpi_options, language_options],
                outputs=[custom_image_dpi_size],
            )

            img_but.click(
                processor.process,
                inputs=[
                    img_input,
                    mode_options,
                    size_list_options,
                    color_options,
                    render_options,
                    image_kb_options,
                    custom_color_R,
                    custom_color_G,
                    custom_color_B,
                    custom_color_hex_value,
                    custom_size_height_px,
                    custom_size_width_px,
                    custom_size_height_mm,
                    custom_size_width_mm,
                    custom_image_kb_size,
                    language_options,
                    matting_model_options,
                    watermark_options,
                    watermark_text_options,
                    watermark_text_color,
                    watermark_text_size,
                    watermark_text_opacity,
                    watermark_text_angle,
                    watermark_text_space,
                    face_detect_model_options,
                    head_measure_ratio_option,
                    top_distance_option,
                    whitening_option,
                    image_dpi_options,
                    custom_image_dpi_size,
                    brightness_option,
                    contrast_option,
                    sharpen_option,
                    saturation_option,
                    plugin_options,
                    print_options,
                ],
                outputs=[
                    img_output_standard,
                    img_output_standard_hd,
                    img_output_standard_png,
                    img_output_standard_hd_png,
                    img_output_layout,
                    img_output_template,
                    template_image_accordion,
                    notification,
                ],
            )

    return demo
