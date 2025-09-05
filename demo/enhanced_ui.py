import gradio as gr
import os
import pathlib
from demo.locales import LOCALES
from demo.processor import IDPhotoProcessor

"""
Enhanced UI with SEO optimization and better user experience
增强版UI，包含SEO优化和更好的用户体验
"""

def load_description(fp):
    """
    加载title.md文件作为Demo的顶部栏
    """
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def create_enhanced_ui(
    processor: IDPhotoProcessor,
    root_dir: str,
    human_matting_models: list,
    face_detect_models: list,
    language: list,
):
    # 加载环境变量DEFAULT_LANG
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

    # SEO优化的页面标题和描述
    page_title = "AI智能证件照制作工具 - 免费在线抠图换背景 | HivisionIDPhoto"
    page_description = "HivisionIDPhoto是专业的AI证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸。完全免费，纯离线处理，保护隐私安全。支持护照照、签证照、身份证照片制作。"
    
    # 创建自定义CSS
    custom_css = """
    <style>
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .quick-start-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        margin: 20px 0;
    }
    .mode-toggle {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .simple-mode .advanced-controls {
        display: none !important;
    }
    .privacy-notice {
        background: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 15px;
        margin: 20px 0;
        color: #2e7d32;
    }
    </style>
    """

    # 创建增强的HTML头部
    html_head = f"""
    <head>
        <title>{page_title}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="{page_description}">
        <meta name="keywords" content="证件照制作,AI抠图,在线换背景,护照照片,签证照片,身份证照片,免费抠图工具,HivisionIDPhoto">
        <meta name="author" content="HivisionIDPhoto Team">
        <meta name="robots" content="index, follow">
        
        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/">
        <meta property="og:title" content="{page_title}">
        <meta property="og:description" content="{page_description}">
        <meta property="og:image" content="https://swanhub.co/git/repo/ZeYiLin%2FHivisionIDPhotos/file/preview?ref=master&path=assets/hivision_logo.png">

        <!-- Twitter -->
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:url" content="https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/">
        <meta property="twitter:title" content="{page_title}">
        <meta property="twitter:description" content="{page_description}">
        <meta property="twitter:image" content="https://swanhub.co/git/repo/ZeYiLin%2FHivisionIDPhotos/file/preview?ref=master&path=assets/hivision_logo.png">
        
        <!-- Structured Data -->
        <script type="application/ld+json">
        {{
            "@context": "https://schema.org/",
            "@type": "WebApplication",
            "name": "HivisionIDPhoto",
            "description": "{page_description}",
            "url": "https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/",
            "applicationCategory": "PhotoEditingApplication",
            "operatingSystem": "Web Browser",
            "offers": {{
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "CNY"
            }},
            "creator": {{
                "@type": "Organization",
                "name": "HivisionIDPhoto Team"
            }},
            "featureList": [
                "AI智能抠图",
                "证件照制作",
                "背景替换",
                "多种尺寸规格",
                "美颜处理",
                "离线处理"
            ]
        }}
        </script>
        
        <!-- hreflang for multilingual -->
        <link rel="alternate" hreflang="zh-cn" href="?lang=zh" />
        <link rel="alternate" hreflang="en" href="?lang=en" />
        <link rel="alternate" hreflang="ja" href="?lang=ja" />
        <link rel="alternate" hreflang="ko" href="?lang=ko" />
        <link rel="canonical" href="https://7860-inxx0p1bgz3fp6r98vuvg-6532622b.e2b.dev/" />
        
        {custom_css}
    </head>
    """

    # 创建Gradio界面
    demo = gr.Blocks(
        title=page_title,
        head=html_head,
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="gray"
        )
    )

    with demo:
        # 使用增强的标题文件
        gr.HTML(load_description(os.path.join(root_dir, "demo/assets/enhanced_title.md")))
        
        # 隐私保护提示
        gr.HTML("""
        <div class="privacy-notice">
            🔒 <strong>隐私保护承诺</strong>：您上传的照片将在本地处理，不会上传到服务器或第三方，确保您的个人隐私安全。
        </div>
        """)
        
        # 模式切换
        with gr.Row():
            mode_switch = gr.Radio(
                choices=["简单模式", "专业模式"],
                value="简单模式",
                label="操作模式",
                info="简单模式隐藏高级参数，专业模式显示所有选项"
            )
        
        with gr.Row():
            # ------------------------ 左半边 UI ------------------------
            with gr.Column():
                gr.HTML("<h3>📤 上传照片</h3>")
                img_input = gr.Image(height=400)

                with gr.Row():
                    # 语言选择器
                    language_options = gr.Dropdown(
                        choices=language,
                        label="Language / 语言",
                        value=DEFAULT_LANG,
                    )

                    face_detect_model_options = gr.Dropdown(
                        choices=face_detect_models,
                        label=LOCALES["face_model"][DEFAULT_LANG]["label"],
                        value=DEFAULT_FACE_DETECT_MODEL,
                        visible=False,  # 在简单模式下隐藏
                        elem_classes=["advanced-controls"]
                    )

                    matting_model_options = gr.Dropdown(
                        choices=human_matting_models,
                        label=LOCALES["matting_model"][DEFAULT_LANG]["label"],
                        value=human_matting_models[0],
                        visible=False,  # 在简单模式下隐藏
                        elem_classes=["advanced-controls"]
                    )

                # 快速预设（简单模式）
                with gr.Group() as simple_presets:
                    gr.HTML("<h3>🎯 快速选择</h3>")
                    with gr.Row():
                        preset_buttons = []
                        presets = [
                            ("护照照片", "295x413", "#FFFFFF"),
                            ("签证照片", "354x472", "#FFFFFF"),
                            ("身份证照", "358x441", "#FFFFFF"),
                            ("一寸照", "295x413", "#FF0000"),
                            ("二寸照", "413x579", "#FF0000"),
                        ]
                        for preset_name, size, bg_color in presets:
                            btn = gr.Button(preset_name, variant="secondary")
                            preset_buttons.append((btn, preset_name, size, bg_color))

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

                # 高级参数（只在专业模式显示）
                with gr.Tab(
                    LOCALES["advance_param"][DEFAULT_LANG]["label"],
                    elem_classes=["advanced-controls"]
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

                # 美颜参数
                with gr.Tab(
                    LOCALES["beauty_tab"][DEFAULT_LANG]["label"],
                    elem_classes=["advanced-controls"]
                ) as beauty_parameter_tab:
                    whitening_option = gr.Slider(
                        label=LOCALES["whitening_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=15,
                        value=2,
                        step=1,
                        interactive=True,
                    )

                    with gr.Row():
                        brightness_option = gr.Slider(
                            label=LOCALES["brightness_strength"][DEFAULT_LANG]["label"],
                            minimum=-5,
                            maximum=25,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        contrast_option = gr.Slider(
                            label=LOCALES["contrast_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )
                        saturation_option = gr.Slider(
                            label=LOCALES["saturation_strength"][DEFAULT_LANG]["label"],
                            minimum=-10,
                            maximum=50,
                            value=0,
                            step=1,
                            interactive=True,
                        )

                    sharpen_option = gr.Slider(
                        label=LOCALES["sharpen_strength"][DEFAULT_LANG]["label"],
                        minimum=0,
                        maximum=5,
                        value=0,
                        step=1,
                        interactive=True,
                    )

                # 水印参数
                with gr.Tab(
                    LOCALES["watermark_tab"][DEFAULT_LANG]["label"],
                    elem_classes=["advanced-controls"]
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
                            placeholder=LOCALES["watermark_text"][DEFAULT_LANG]["placeholder"],
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
                
                # 打印排版
                with gr.Tab(
                    LOCALES["print_tab"][DEFAULT_LANG]["label"],
                    elem_classes=["advanced-controls"]
                ) as print_parameter_tab:
                    print_options = gr.Radio(
                        choices=LOCALES["print_switch"][DEFAULT_LANG]["choices"],
                        label=LOCALES["print_switch"][DEFAULT_LANG]["label"],
                        value=LOCALES["print_switch"][DEFAULT_LANG]["choices"][0],
                        interactive=True,
                    )

                # 主要操作按钮
                img_but = gr.Button(
                    "🚀 " + LOCALES["button"][DEFAULT_LANG]["label"],
                    elem_id="btn",
                    variant="primary",
                    size="lg",
                    elem_classes=["quick-start-btn"]
                )

                # 示例图片
                example_images = gr.Examples(
                    inputs=[img_input],
                    examples=[
                        [path.as_posix()]
                        for path in sorted(
                            pathlib.Path(os.path.join(root_dir, "demo/images")).rglob("*.jpg")
                        )
                    ],
                    label="📸 示例图片 - 点击试用"
                )

            # ---------------- 右半边 UI ----------------
            with gr.Column():
                gr.HTML("<h3>📥 下载结果</h3>")
                notification = gr.Text(
                    label=LOCALES["notification"][DEFAULT_LANG]["label"], 
                    visible=False
                )
                
                with gr.Row():
                    # 标准照
                    img_output_standard = gr.Image(
                        label=LOCALES["standard_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                    # 高清照
                    img_output_standard_hd = gr.Image(
                        label=LOCALES["hd_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                
                # 排版照
                img_output_layout = gr.Image(
                    label=LOCALES["layout_photo"][DEFAULT_LANG]["label"],
                    height=350,
                    format="png",
                )
                
                # 模版照片
                with gr.Accordion(
                    LOCALES["template_photo"][DEFAULT_LANG]["label"], 
                    open=False
                ) as template_image_accordion:      
                    img_output_template = gr.Gallery(
                        label=LOCALES["template_photo"][DEFAULT_LANG]["label"],
                        height=350,
                        format="png",
                    )
                
                # 抠图图像
                with gr.Accordion(
                    LOCALES["matting_image"][DEFAULT_LANG]["label"], 
                    open=False
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

        # 添加使用提示和帮助信息
        gr.HTML("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;">
            <h3>💡 使用提示</h3>
            <ul style="text-align: left; margin: 10px 0;">
                <li>📷 <strong>照片要求</strong>：建议上传正面免冠照片，光线充足，背景简单</li>
                <li>🎯 <strong>简单模式</strong>：适合普通用户，使用预设模板快速制作</li>
                <li>⚙️ <strong>专业模式</strong>：提供更多自定义选项，适合有特殊需求的用户</li>
                <li>🔒 <strong>隐私安全</strong>：所有处理均在本地进行，不会上传您的照片</li>
                <li>💾 <strong>保存方式</strong>：右键点击生成的图片选择"保存图片"</li>
            </ul>
        </div>
        """)

        # 添加常见问题
        with gr.Accordion("❓ 常见问题", open=False):
            gr.HTML("""
            <div style="text-align: left; padding: 20px;">
                <h4>Q: 支持哪些照片格式？</h4>
                <p>A: 支持JPG、PNG、JPEG等常见图片格式。</p>
                
                <h4>Q: 生成的照片尺寸准确吗？</h4>
                <p>A: 是的，我们严格按照各类证件照的标准尺寸要求制作。</p>
                
                <h4>Q: 可以批量处理多张照片吗？</h4>
                <p>A: 当前版本支持单张处理，批量处理功能正在开发中。</p>
                
                <h4>Q: 照片会被保存在服务器上吗？</h4>
                <p>A: 不会。所有处理都在您的浏览器本地进行，保护您的隐私安全。</p>
            </div>
            """)

        # 模式切换功能（需要添加JavaScript）
        mode_switch_js = """
        function toggleMode(mode) {
            const advancedElements = document.querySelectorAll('.advanced-controls');
            if (mode === '简单模式') {
                document.body.classList.add('simple-mode');
                advancedElements.forEach(el => el.style.display = 'none');
            } else {
                document.body.classList.remove('simple-mode');
                advancedElements.forEach(el => el.style.display = 'block');
            }
        }
        """
        
        gr.HTML(f"<script>{mode_switch_js}</script>")

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
                img_but: gr.update(value="🚀 " + LOCALES["button"][language]["label"]),
                render_options: gr.update(
                    label=LOCALES["render_mode"][language]["label"],
                    choices=LOCALES["render_mode"][language]["choices"],
                    value=LOCALES["render_mode"][language]["choices"][0],
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

        def update_watermark_text_visibility(choice, language):
            return [
                gr.update(
                    interactive=(
                        choice
                        == LOCALES["watermark_switch"][language]["choices"][1]
                    )
                )
            ] * 6

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
                matting_model_options,
                face_detect_model_options,
            ],
        )

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

        # 水印
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

        # 主要处理函数
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