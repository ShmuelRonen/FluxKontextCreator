# Flux Kontext Creator - ComfyUI Node

A powerful ComfyUI node for text-based image editing using Black Forest Labs' Flux Kontext API.

## Features

🎨 **Text-Based Editing** - Edit images with simple text instructions  
⚡ **Fast Processing** - 3-5 seconds generation time  
🎯 **Local Edits** - Change specific parts without affecting the rest  
🔄 **Character Consistency** - Maintain character identity across edits  
🏆 **Premium Quality** - Pro and Max model options  

## Installation

### 1. Create Node Directory
```bash
# Navigate to your ComfyUI custom_nodes directory
cd ComfyUI/custom_nodes/

# Create new directory for the node
mkdir flux-kontext-creator
cd flux-kontext-creator
```

### 2. Add Node Files
Place these files in the `flux-kontext-creator` directory:
- `__init__.py` (the init file)
- `flux_kontext_creator.py` (the main node file)
- `config.ini` (configuration file)

### 3. Setup Configuration
Edit `config.ini` and add your BFL API key:
```ini
[API]
X_KEY=your-bfl-api-key-here
```

**Get your API key from:** https://api.bfl.ai

### 4. Install Dependencies
```bash
# Navigate to ComfyUI root
cd ../../

# Install required packages
pip install requests pillow numpy torch configparser
```

### 5. Restart ComfyUI
Completely restart ComfyUI to load the new node.

## Usage

### Basic Workflow
1. Load an image in ComfyUI
2. Add the **"🎨 Flux Kontext Creator"** node
3. Connect your image to the `input_image` input
4. Write your edit instruction in `edit_instruction`
5. Run the workflow

### Example Instructions

#### Color Changes
```
Change the car color to bright red
Make the person's shirt blue
Turn the sky into sunset colors
```

#### Adding Elements
```
Add sunglasses to the person
Place a cat on the table
Add a modern sofa in the room
```

#### Text Editing
```
Change the text on the sign to "WELCOME"
Replace "STORE" with "CAFE" on the building
Update the license plate to "HELLO"
```

#### Background Changes
```
Move the person to a beach setting while keeping the same pose
Change the background to a modern office
Transform the location to a forest scene
```

### Node Parameters

| Parameter | Description | Options |
|-----------|-------------|---------|
| `input_image` | Source image to edit | ComfyUI IMAGE |
| `edit_instruction` | Text describing the edit | Free text |
| `model` | Kontext model to use | pro, max |
| `aspect_ratio` | Output aspect ratio | 1:1, 16:9, etc. |
| `output_format` | Image format | png, jpeg |
| `safety_tolerance` | Content safety level | 0-6 |
| `seed` | Random seed | -1 (random) or number |
| `keep_original_on_fail` | Return original if edit fails | true/false |

### Model Comparison

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| **flux-kontext-pro** | ⚡⚡⚡ | 🌟🌟🌟🌟 | General editing |
| **flux-kontext-max** | ⚡⚡ | 🌟🌟🌟🌟🌟 | Typography, premium quality |

## Tips for Best Results

### 🎯 Be Specific
- ❌ "Make it look better"
- ✅ "Change the wall color to light gray"

### 🔒 Preserve Elements
- ✅ "Add a hat while keeping the same facial expression"
- ✅ "Change background to forest while maintaining the person's position"

### 🔄 Multiple Edits
- Make one edit at a time
- Use the result as input for the next edit
- This maintains quality and consistency

### 👥 Character References
- ❌ "Change her hair"
- ✅ "Change the woman with black hair to blonde hair"

## Troubleshooting

### ❌ "X_KEY not found"
**Solution:** Check that `config.ini` exists and contains your API key

### ❌ "Invalid API key"
**Solution:** Verify your API key at https://api.bfl.ai

### ❌ "Insufficient credits"
**Solution:** Add credits to your BFL account

### ❌ "Node not appearing"
**Solution:** 
1. Check all files are in the correct directory
2. Restart ComfyUI completely
3. Check console for error messages

### ❌ "Edit didn't work"
**Solution:**
- Make instruction more specific
- Try different safety_tolerance setting
- Use flux-kontext-max for better quality

## API Costs

- **flux-kontext-pro**: ~$0.04 per image
- **flux-kontext-max**: ~$0.06 per image

*Prices may vary, check BFL pricing for current rates*

## Support

- **BFL Documentation**: https://docs.bfl.ai
- **API Dashboard**: https://api.bfl.ai
- **Model Info**: https://bfl.ai/announcements/flux-1-kontext

## License

This node is for use with Black Forest Labs' Flux Kontext API. Please comply with BFL's terms of service and usage policies.

---

**Happy editing with Flux Kontext Creator!** 🎨✨
