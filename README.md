# 🎨 Flux Kontext Creator for ComfyUI

A powerful ComfyUI custom node for text-based image editing using Black Forest Labs' Flux Kontext API. Transform your images with simple text instructions while maintaining character consistency and quality.

![Flux Kontext Creator](https://img.shields.io/badge/ComfyUI-Custom%20Node-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

![image](https://github.com/user-attachments/assets/d8c819a5-322e-4782-8e74-0899f7e1b862)


## ✨ Features

- **🖼️ Text-Based Image Editing**: Modify images using simple text instructions
- **🎭 Character Consistency**: Maintain character identity across multiple edits
- **⚡ Fast Processing**: 3-5 second generation times
- **🎯 Local Editing**: Target specific parts without affecting the rest
- **🎨 Style Transfer**: Apply different artistic styles while preserving elements
- **📝 Text Editing**: Modify text within images directly
- **🔄 Iterative Editing**: Build upon previous edits step-by-step

## 🚀 Supported Models

- **FLUX.1 Kontext [pro]**: Fast, iterative editing for production workflows
- **FLUX.1 Kontext [max]**: Maximum performance with enhanced typography and prompt precision

## 📋 Requirements

- ComfyUI (latest version recommended)
- Python 3.7+
- Black Forest Labs API key
- Required Python packages:
  - `requests`
  - `Pillow (PIL)`
  - `torch`
  - `numpy`

## 🛠️ Installation

### Method 1: ComfyUI Manager (Recommended)

1. Open ComfyUI Manager
2. Search for "Flux Kontext Creator"
3. Click Install
4. Restart ComfyUI

### Method 2: Git Clone

1. Navigate to your ComfyUI custom nodes directory:
```bash
cd ComfyUI/custom_nodes/
```

2. Clone the repository:
```bash
git clone https://github.com/ShmuelRonen/FluxKontextCreator.git
```

3. Install dependencies:
```bash
cd FluxKontextCreator
pip install -r requirements.txt
```

4. Restart ComfyUI

### Method 3: Manual Download

1. Download the latest release from [GitHub](https://github.com/ShmuelRonen/FluxKontextCreator/releases)
2. Extract to `ComfyUI/custom_nodes/FluxKontextCreator/`
3. Restart ComfyUI

## ⚙️ Configuration

### 1. Get Your API Key

1. Visit [Black Forest Labs API](https://api.bfl.ai)
2. Sign up for an account
3. Get your API key from the dashboard
4. You'll receive 200 free credits to start

### 2. Create config.ini File

**Step-by-step instructions:**

1. **Navigate to the node directory:**
   ```
   ComfyUI/custom_nodes/FluxKontextCreator/
   ```

2. **Create a new file called `config.ini`** (use any text editor)

3. **Copy and paste this template:**
   ```ini
   [API]
   # Your Black Forest Labs API key
   X_KEY=your-actual-api-key-here
   
   # API endpoint (use api.bfl.ai, not api.bfl.ml)
   BASE_URL=https://api.bfl.ai
   
   [SETTINGS]
   # Default timeout for API requests (seconds)
   TIMEOUT=60
   
   # Default safety tolerance (0-6)
   SAFETY_TOLERANCE=4
   
   # Default output format (png/jpeg)
   OUTPUT_FORMAT=png
   ```

4. **Replace `your-actual-api-key-here`** with your real API key

5. **Save the file** as `config.ini`

### 📁 File Structure Example

After installation, your directory should look like this:
```
ComfyUI/
└── custom_nodes/
    └── FluxKontextCreator/
        ├── __init__.py
        ├── flux_kontext_creator.py
        ├── config.ini          ← YOU CREATE THIS
        └── README.md
```

### 🔑 Real config.ini Example

If your API key is `bfl_12345abcdef`, your config.ini should look like:
```ini
[API]
X_KEY=bfl_12345abcdef
BASE_URL=https://api.bfl.ai

[SETTINGS]
TIMEOUT=60
SAFETY_TOLERANCE=4
OUTPUT_FORMAT=png
```

### ⚠️ Important Notes

- **Use `api.bfl.ai`** (the actual API) not `api.bfl.ml` (the documentation site)
- **No quotes** around the API key
- **No spaces** around the `=` sign
- The file **must be named exactly** `config.ini`
- **Keep your API key private** - don't share it publicly

## 🎯 Usage

### Basic Workflow

1. **Load Image**: Use "Load Image" node to import your source image
2. **Add Flux Kontext Creator**: Add the "🎨 Flux Kontext Creator" node to your workflow
3. **Connect**: Connect your image to the `input_image` input
4. **Configure**: Set your editing instruction and parameters
5. **Execute**: Run the workflow and get your edited image

### Example Prompts

```
✅ Good prompts:
"Change the car color to red"
"Add sunglasses to the person"
"Make the background a beach scene"
"Replace 'Hello' with 'Welcome'"
"Turn the cat into a dog"

❌ Avoid:
Empty instructions
Very long complex descriptions
Conflicting instructions
```

### Node Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input_image` | Source image to edit | Required |
| `edit_instruction` | Text description of desired changes | "Change the car color to red" |
| `model` | Choose pro or max model | flux-kontext-pro |
| `aspect_ratio` | Output image ratio | 1:1 |
| `output_format` | Image format (png/jpeg) | png |
| `safety_tolerance` | Content filtering level (0-6) | 4 |
| `seed` | Random seed (-1 for random) | -1 |
| `keep_original_on_fail` | Return original if editing fails | True |

### Safety Tolerance Guide

- **0-2**: Very strict content filtering
- **3-4**: Balanced filtering (recommended)
- **5-6**: More permissive for creative work

## 📖 Advanced Usage

### Iterative Editing

Chain multiple Flux Kontext Creator nodes to build complex edits:

```
Image → Kontext1 ("Add hat") → Kontext2 ("Change background") → Final Result
```

### Text Editing

For text within images, use quotation marks:
```
Replace 'Old Text' with 'New Text'
```

### Character Consistency

The model excels at maintaining character identity across edits:
```
"Put the same person in a different outfit"
"Move the character to a beach setting"
```

## 🐛 Troubleshooting

### Common Issues

**Node not appearing in ComfyUI:**
- Restart ComfyUI completely
- Check console for error messages
- Verify all dependencies are installed

**API Key errors:**
- Verify your API key in `config.ini`
- Ensure you have sufficient credits
- Check that BASE_URL is `https://api.bfl.ai`

**Image generation fails:**
- Check your prompt isn't empty
- Verify internet connection
- Try lowering safety_tolerance if content is blocked
- Check BFL service status

**Connection errors:**
- Verify API endpoint is correct
- Check firewall/network settings
- Try again after a few minutes

### Error Messages

| Error | Solution |
|-------|----------|
| "X_KEY not found" | Add API key to config.ini |
| "Invalid API key" | Check your API key is correct |
| "Insufficient credits" | Add credits to your BFL account |
| "Request timeout" | Check internet connection, try again |
| "Content Moderated" | Adjust prompt or lower safety_tolerance |

## 🔄 Updates

To update the node:

```bash
cd ComfyUI/custom_nodes/FluxKontextCreator
git pull origin main
```

Or use ComfyUI Manager's update feature.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Black Forest Labs](https://blackforestlabs.ai/) for the amazing Flux Kontext API
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) community for the excellent framework
- All contributors and users of this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ShmuelRonen/FluxKontextCreator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ShmuelRonen/FluxKontextCreator/discussions)
- **BFL API Support**: [BFL Documentation](https://docs.bfl.ai)

## ⭐ Show Your Support

If this project helps you, please consider giving it a star on GitHub!

---

**Made with ❤️ for the ComfyUI community**
