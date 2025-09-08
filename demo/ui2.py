import gradio as gr
import os
from demo.locales import LOCALES


def create_ui(processor, root_dir, human_matting_models, face_detect_models, language):
    # Defaults: prefer English if available
    default_lang = "en" if (language and "en" in language) else (language[0] if language else "en")
    if os.environ.get("DEFAULT_LANG") in language:
        default_lang = os.environ.get("DEFAULT_LANG")

    # Pick defaults safely
    default_matting = human_matting_models[0] if human_matting_models else "modnet_photographic_portrait_matting"
    default_face = face_detect_models[0] if face_detect_models else "mtcnn"

    theme = None
    try:
        theme = gr.themes.Soft(primary_hue="blue", neutral_hue="slate")
    except Exception:
        pass

    demo = gr.Blocks(title="AI IDPhotos", theme=theme)

    with demo:
        gr.Markdown("# AI IDPhotos Tool")
        with gr.Row():
            with gr.Column(scale=7):
                img_input = gr.Image(height=360, label=None, show_label=False)
                with gr.Row():
                    language_options = gr.Dropdown(language, label="Language", value=default_lang)
                    face_detect_model_options = gr.Dropdown(face_detect_models or ["mtcnn"], label=LOCALES["face_model"][default_lang]["label"], value=default_face)
                    matting_model_options = gr.Dropdown(human_matting_models or [default_matting], label=LOCALES["matting_model"][default_lang]["label"], value=default_matting)

                with gr.Tab(LOCALES["key_param"][default_lang]["label"]):
                    mode_options = gr.Radio(LOCALES["size_mode"][default_lang]["choices"], label=LOCALES["size_mode"][default_lang]["label"], value=LOCALES["size_mode"][default_lang]["choices"][0])
                    with gr.Row():
                        size_list_options = gr.Dropdown(LOCALES["size_list"][default_lang]["choices"], label=LOCALES["size_list"][default_lang]["label"], value=LOCALES["size_list"][default_lang]["choices"][0])
                    with gr.Row():
                        custom_size_height_px = gr.Number(value=413, label=LOCALES["custom_size_px"][default_lang]["height"], interactive=True)
                        custom_size_width_px = gr.Number(value=295, label=LOCALES["custom_size_px"][default_lang]["width"], interactive=True)
                    with gr.Row():
                        custom_size_height_mm = gr.Number(value=35, label=LOCALES["custom_size_mm"][default_lang]["height"], interactive=True)
                        custom_size_width_mm = gr.Number(value=25, label=LOCALES["custom_size_mm"][default_lang]["width"], interactive=True)

                    color_options = gr.Dropdown(LOCALES["bg_color"][default_lang]["choices"], label=LOCALES["bg_color"][default_lang]["label"], value=LOCALES["bg_color"][default_lang]["choices"][0])
                    with gr.Row():
                        custom_color_R = gr.Number(value=0, label="R", interactive=True)
                        custom_color_G = gr.Number(value=0, label="G", interactive=True)
                        custom_color_B = gr.Number(value=0, label="B", interactive=True)
                    custom_color_hex_value = gr.Text(value="000000", label="Hex", interactive=True)
                    render_options = gr.Radio(LOCALES["render_mode"][default_lang]["choices"], label=LOCALES["render_mode"][default_lang]["label"], value=LOCALES["render_mode"][default_lang]["choices"][0])

                    plugin_options = gr.CheckboxGroup(LOCALES["plugin"][default_lang]["choices"], label=LOCALES["plugin"][default_lang]["label"], value=LOCALES["plugin"][default_lang].get("value", []))

                with gr.Accordion(LOCALES["advance_param"][default_lang]["label"], open=False):
                    head_measure_ratio_option = gr.Slider(minimum=0.1, maximum=0.5, value=0.2, step=0.01, label=LOCALES["head_measure_ratio"][default_lang]["label"], interactive=True)
                    top_distance_option = gr.Slider(minimum=0.02, maximum=0.5, value=0.12, step=0.01, label=LOCALES["top_distance"][default_lang]["label"], interactive=True)
                    image_kb_options = gr.Radio(LOCALES["image_kb"][default_lang]["choices"], label=LOCALES["image_kb"][default_lang]["label"], value=LOCALES["image_kb"][default_lang]["choices"][0])
                    custom_image_kb_size = gr.Slider(minimum=10, maximum=1000, value=50, label=LOCALES["image_kb_size"][default_lang]["label"], interactive=True)
                    image_dpi_options = gr.Radio(LOCALES["image_dpi"][default_lang]["choices"], label=LOCALES["image_dpi"][default_lang]["label"], value=LOCALES["image_dpi"][default_lang]["choices"][0])
                    custom_image_dpi_size = gr.Slider(minimum=72, maximum=600, value=300, label=LOCALES["image_dpi_size"][default_lang]["label"], interactive=True)

                with gr.Accordion(LOCALES["beauty_tab"][default_lang]["label"], open=False):
                    whitening_option = gr.Slider(label=LOCALES["whitening_strength"][default_lang]["label"], minimum=0, maximum=15, value=2, step=1, interactive=True)
                    brightness_option = gr.Slider(label=LOCALES["brightness_strength"][default_lang]["label"], minimum=-5, maximum=25, value=0, step=1, interactive=True)
                    contrast_option = gr.Slider(label=LOCALES["contrast_strength"][default_lang]["label"], minimum=-10, maximum=50, value=0, step=1, interactive=True)
                    saturation_option = gr.Slider(label=LOCALES["saturation_strength"][default_lang]["label"], minimum=-10, maximum=50, value=0, step=1, interactive=True)
                    sharpen_option = gr.Slider(label=LOCALES["sharpen_strength"][default_lang]["label"], minimum=0, maximum=5, value=0, step=1, interactive=True)

                with gr.Accordion(LOCALES["watermark_tab"][default_lang]["label"], open=False):
                    watermark_options = gr.Radio(LOCALES["watermark_switch"][default_lang]["choices"], label=LOCALES["watermark_switch"][default_lang]["label"], value=LOCALES["watermark_switch"][default_lang]["choices"][0])
                    watermark_text_options = gr.Text(max_length=20, label=LOCALES["watermark_text"][default_lang]["label"], value=LOCALES["watermark_text"][default_lang]["value"], placeholder=LOCALES["watermark_text"][default_lang]["placeholder"], interactive=False)
                    watermark_text_color = gr.ColorPicker(label=LOCALES["watermark_color"][default_lang]["label"], value="#FFFFFF", interactive=False)
                    watermark_text_size = gr.Slider(minimum=10, maximum=100, value=20, label=LOCALES["watermark_size"][default_lang]["label"], interactive=False, step=1)
                    watermark_text_opacity = gr.Slider(minimum=0, maximum=1, value=0.15, label=LOCALES["watermark_opacity"][default_lang]["label"], interactive=False, step=0.01)
                    watermark_text_angle = gr.Slider(minimum=0, maximum=360, value=30, label=LOCALES["watermark_angle"][default_lang]["label"], interactive=False, step=1)
                    watermark_text_space = gr.Slider(minimum=10, maximum=200, value=25, label=LOCALES["watermark_space"][default_lang]["label"], interactive=False, step=1)

                with gr.Accordion(LOCALES["print_tab"][default_lang]["label"], open=False):
                    print_options = gr.Radio(choices=LOCALES["print_switch"][default_lang]["choices"], label=LOCALES["print_switch"][default_lang]["label"], value=LOCALES["print_switch"][default_lang]["choices"][0])

                img_but = gr.Button(LOCALES["button"][default_lang]["label"], elem_id="btn", variant="primary")

            # Right panel results
            with gr.Column(scale=5, elem_id="right_panel", visible=False) as result_panel:
                notification = gr.Text(label=LOCALES["notification"][default_lang]["label"], visible=False)
                with gr.Row():
                    img_output_standard = gr.Image(label=LOCALES["standard_photo"][default_lang]["label"], height=320, format="png", interactive=False, visible=False)
                    img_output_standard_hd = gr.Image(label=LOCALES["hd_photo"][default_lang]["label"], height=320, format="png", interactive=False, visible=False)
                img_output_layout = gr.Image(label=LOCALES["layout_photo"][default_lang]["label"], height=320, format="png", interactive=False, visible=False)
                with gr.Accordion(LOCALES["template_photo"][default_lang]["label"], open=False) as template_image_accordion:
                    img_output_template = gr.Gallery(label=LOCALES["template_photo"][default_lang]["label"], height=320, format="png")
                with gr.Accordion(LOCALES["matting_image"][default_lang]["label"], open=False):
                    with gr.Row():
                        img_output_standard_png = gr.Image(label=LOCALES["standard_photo_png"][default_lang]["label"], height=320, format="png", elem_id="standard_photo_png", interactive=False)
                        img_output_standard_hd_png = gr.Image(label=LOCALES["hd_photo_png"][default_lang]["label"], height=320, format="png", elem_id="hd_photo_png", interactive=False)

        # Bind
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
                result_panel,
            ],
        )

    return demo
