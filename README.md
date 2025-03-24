# Gemini Image Editing Tool

## Overview
The **Gemini Image Editing Tool** is a web-based interface that utilizes Google's Gemini API for AI-driven image generation and editing. Built using **Gradio**, this tool allows users to upload images, input prompts, and generate modified outputs using the **Gemini-2.0-flash-exp** model.

## Features
- **AI-Powered Image Editing:** Modify images based on user-provided prompts.
- **Text and Image Generation:** Depending on the API response, it can return either an edited image or a textual response.
- **Gradio UI Integration:** Provides an easy-to-use frontend for seamless interaction.
- **API Key Configuration:** Users can enter their own **Google Gemini API Key** for personalized access.

## Installation
### Prerequisites
Ensure that you have the following dependencies installed:
- Python 3.8+
- Anaconda (optional but recommended)

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/hainqh2506/gemini_img_edit.git
   cd gemini-image-edit
   ```
2. **Create a Virtual Environment (Optional but Recommended)**
   ```sh
   conda create --name gemini_env python=3.10
   conda activate gemini_env
   ```
   Or using venv:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```sh
   python app.py
   ```

## Usage
1. **Upload an image** (PNG format is recommended).
2. **Enter a prompt** describing the desired modification.
3. **Provide a Gemini API Key** (if not set in environment variables).
4. Click **"Generate"** to process the request.
5. The tool will display the modified image or return a text response if the model doesn't generate an image.

## API Key Configuration
You need a valid **Google Gemini API Key** to use this tool. Get yours from [Google AI Studio](https://aistudio.google.com/apikey).

You can set the API Key in two ways:
1. **Manually enter it in the UI.**
2. **Set it as an environment variable:**
   ```sh
   export GEMINI_API_KEY="your-api-key-here"
   ```
   On Windows:
   ```sh
   set GEMINI_API_KEY="your-api-key-here"
   ```

## Known Issues & Troubleshooting
- **Model Returns Text Instead of an Image:**
  - Try adjusting the prompt.
  - Ensure the API Key is valid.
  - Restart the application and try again.
- **ModuleNotFoundError (e.g., `orjson` not found):**
  - Install missing dependencies using:
    ```sh
    pip install orjson
    ```
  - Run the application inside the virtual environment.

## Example Prompts
| Example Image | Prompt |
|--------------|--------|
| `data/1.webp` | "Change text to 'AMEER'" |
| `data/2.webp` | "Remove the spoon from the hand only" |
| `data/3.webp` | "Change text to 'Make it'" |
| `data/1.jpg` | "Add Joker style only on face" |
| `data/1777043.jpg` | "Add Joker style only on face" |
| `data/2807615.jpg` | "Add lipstick on lips only" |

## License
This project is licensed under the MIT License.

## Acknowledgments
- **[Gradio](https://gradio.app/)** for the UI framework.
- **[Google Gemini](https://ai.google.dev/)** for the AI model.

For any issues or contributions, feel free to submit a pull request or open an issue on GitHub!

