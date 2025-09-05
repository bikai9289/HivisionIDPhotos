import gradio as gr
import os
from demo.ui import create_ui

def create_enhanced_ui(
    processor,
    root_dir: str,
    human_matting_models: list,
    face_detect_models: list,
    language: list,
):
    """
    创建增强版UI，基于原有UI增加SEO优化
    """
    
    # SEO优化的页面标题和描述
    page_title = "AI智能证件照制作工具 - 免费在线抠图换背景 | HivisionIDPhoto"
    page_description = "HivisionIDPhoto是专业的AI证件照制作工具，支持一键抠图、智能换背景、多种证件照尺寸。完全免费，纯离线处理，保护隐私安全。支持护照照、签证照、身份证照片制作。"
    
    # 创建自定义HTML头部
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
    </head>
    """

    # 先创建基础UI
    demo = create_ui(processor, root_dir, human_matting_models, face_detect_models, language)
    
    # 更新页面标题和添加HTML头部
    demo.title = page_title
    
    # 在原有界面基础上添加增强的标题内容
    with demo:
        # 在顶部添加增强的内容
        enhanced_header = gr.HTML("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 10px 0; text-align: center;">
            <h2 style="margin: 0; font-size: 24px;">🎯 专业AI证件照制作 | 免费 • 离线 • 安全</h2>
            <p style="margin: 10px 0 0 0;">支持护照照、签证照、身份证照等多种规格 | 一键智能抠图 | 3秒生成专业证件照</p>
        </div>
        """, visible=True)
        
        # 添加隐私保护提示
        privacy_notice = gr.HTML("""
        <div style="background: #e8f5e8; border: 1px solid #4caf50; border-radius: 8px; padding: 15px; margin: 10px 0; color: #2e7d32;">
            🔒 <strong>隐私保护承诺</strong>：您上传的照片将在本地处理，不会上传到服务器或第三方，确保您的个人隐私安全。
        </div>
        """, visible=True)
        
        # 添加功能特色
        features = gr.HTML("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">🎯</div>
                <h3 style="margin: 10px 0; color: #2c3e50;">一键智能抠图</h3>
                <p style="margin: 0; color: #7f8c8d;">AI自动识别人像，精准去除背景</p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">📏</div>
                <h3 style="margin: 10px 0; color: #2c3e50;">标准尺寸预设</h3>
                <p style="margin: 0; color: #7f8c8d;">护照、签证、身份证等常用规格</p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="font-size: 36px; margin-bottom: 10px;">🔒</div>
                <h3 style="margin: 10px 0; color: #2c3e50;">隐私保护</h3>
                <p style="margin: 0; color: #7f8c8d;">纯离线处理，图片不上传服务器</p>
            </div>
        </div>
        """, visible=True)
        
        # 添加使用提示
        tips = gr.HTML("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #2c3e50; margin-top: 0;">💡 使用提示</h3>
            <ul style="text-align: left; margin: 10px 0; color: #495057;">
                <li>📷 <strong>照片要求</strong>：建议上传正面免冠照片，光线充足，背景简单</li>
                <li>🎯 <strong>操作简单</strong>：上传照片 → 选择规格 → 下载结果</li>
                <li>🔒 <strong>隐私安全</strong>：所有处理均在本地进行，不会上传您的照片</li>
                <li>💾 <strong>保存方式</strong>：右键点击生成的图片选择"保存图片"</li>
            </ul>
        </div>
        """, visible=True)
    
    return demo