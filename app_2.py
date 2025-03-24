import json
import os
import time
import uuid
import tempfile
from PIL import Image, ImageDraw, ImageFont
import gradio as gr
import base64
import mimetypes

from google import genai
from google.genai import types
MODEL_NAME = "gemini-2.0-flash-exp-image-generation"

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)

def generate(text, file_name=None, api_key=None, model=MODEL_NAME):
    client = genai.Client(api_key=(api_key.strip() if api_key and api_key.strip() != ""
                                     else os.environ.get("GEMINI_API_KEY")))
    
    files = [client.files.upload(file=file_name)] if file_name else []
    
    contents = [types.Content(
        role="user",
        parts=[types.Part.from_text(text=text)] + (
            [types.Part.from_uri(file_uri=files[0].uri, mime_type=files[0].mime_type)] if files else []
        ),
    )]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_modalities=["image", "text"],
        response_mime_type="text/plain",
    )

    text_response = ""
    image_path = None
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        temp_path = tmp.name
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
            candidate = chunk.candidates[0].content.parts[0]
            if candidate.inline_data:
                save_binary_file(temp_path, candidate.inline_data.data)
                print(f"Image saved: {temp_path}")
                image_path = temp_path
                break
            else:
                text_response += chunk.text + "\n"
    
    del files
    return image_path, text_response

def process_image_and_prompt(composite_pil, prompt, gemini_api_key):
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            composite_pil.save(tmp.name)
        
        image_path, text_response = generate(prompt, file_name=tmp.name, api_key=gemini_api_key)
        
        if image_path:
            result_img = Image.open(image_path).convert("RGB")
            return [result_img], ""
        return None, text_response
    except Exception as e:
        raise gr.Error(f"Error: {e}", duration=5)

def generate_image_from_text(prompt, gemini_api_key):
    try:
        image_path, text_response = generate(prompt, api_key=gemini_api_key)
        
        if image_path:
            result_img = Image.open(image_path).convert("RGB")
            return [result_img], ""
        return None, text_response
    except Exception as e:
        raise gr.Error(f"Error: {e}", duration=5)

with gr.Blocks(css_paths="style.css") as demo:
    gr.HTML("""<h1>Gemini Image Editing & Generation</h1>""")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Image")
            gemini_api_key = gr.Textbox(lines=1, placeholder="Enter Gemini API Key")
            prompt_input = gr.Textbox(lines=2, placeholder="Enter prompt here...")
            submit_edit_btn = gr.Button("Edit Image")
            submit_generate_btn = gr.Button("Generate New Image")
        
        with gr.Column():
            output_gallery = gr.Gallery(label="Generated Outputs")
            output_text = gr.Textbox(label="Gemini Output")
    
    submit_edit_btn.click(
        fn=process_image_and_prompt,
        inputs=[image_input, prompt_input, gemini_api_key],
        outputs=[output_gallery, output_text],
    )
    
    submit_generate_btn.click(
        fn=generate_image_from_text,
        inputs=[prompt_input, gemini_api_key],
        outputs=[output_gallery, output_text],
    )
    
    demo.queue(max_size=50).launch()
