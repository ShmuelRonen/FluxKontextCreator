# 🎨 Flux Kontext Creator for ComfyUI

A powerful ComfyUI custom node collection for text-based image editing and **revolutionary multi image fusion** using Black Forest Labs' Flux Kontext API. Transform and fuse your images with simple text instructions while maintaining character consistency and quality.

![Flux Kontext Creator](https://img.shields.io/badge/ComfyUI-Custom%20Node-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Fusion](https://img.shields.io/badge/🔥-Image%20Fusion-red)

### Multi image fusion process:
![image](https://github.com/user-attachments/assets/3e5aecee-c9ae-47ef-beee-28e79d6fcbcc)

### single image regular process:
![image](https://github.com/user-attachments/assets/d8c819a5-322e-4782-8e74-0899f7e1b862)

## ✨ Features

### 🎨 **Standard Flux Kontext Creator**
- **🖼️ Text-Based Image Editing**: Modify images using simple text instructions
- **🎭 Character Consistency**: Maintain character identity across multiple edits
- **⚡ Fast Processing**: 3-5 second generation times
- **🎯 Local Editing**: Target specific parts without affecting the rest
- **🎨 Style Transfer**: Apply different artistic styles while preserving elements
- **📝 Text Editing**: Modify text within images directly
- **🔄 Iterative Editing**: Build upon previous edits step-by-step

### 🔥 **NEW: Experimental Fusion Creator**
- **👥 Character Fusion**: Merge multiple people into one unified character
- **🌟 Multi-Image Combination**: Combine up to 10 images with intelligent layouts
- **🎯 Force Fusion Mode**: Advanced prompting system for seamless blending
- **📐 Layout Modes**: Side-by-side, overlay, grid, and seamless blend options
- **🧠 Smart Preprocessing**: Automatic image flattening and resizing
- **⚡ Breakthrough Fusion**: Single-input fusion mode for impossible combinations

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
        ├── flux_kontext_creator_exp.py    ← NEW FUSION NODE
        ├── config.ini                     ← YOU CREATE THIS
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

### 🎨 Standard Flux Kontext Creator

#### Basic Workflow

1. **Load Image**: Use "Load Image" node to import your source image
2. **Add Flux Kontext Creator**: Add the "🎨 Flux Kontext Creator" node to your workflow
3. **Connect**: Connect your image to the `input_image` input
4. **Configure**: Set your editing instruction and parameters
5. **Execute**: Run the workflow and get your edited image

#### Standard Node Parameters

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

### 🔥 Experimental Fusion Creator

#### Revolutionary Fusion Workflow

1. **Load Multiple Images**: Use multiple "Load Image" nodes for your source images
2. **Add Experimental Creator**: Add the "🔥 Flux Kontext Creator Experimental" node
3. **Connect Images**: Connect images to `image_1`, `image_2`, etc.
4. **Set Fusion Parameters**: Configure combination mode and fusion settings
5. **Write Fusion Prompt**: Use fusion-specific language (see guide below)
6. **Execute**: Get impossible fusions that look completely natural

#### Experimental Node Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `prompt` | Fusion instruction text | "Merge these two people..." | Multiline text |
| `number_of_images` | How many images to process | 2 | 1-10 |
| `combination_mode` | How to layout images | side_by_side | side_by_side, overlay, grid_2x2, all_in_one, no_combine |
| `force_fusion` | Enable advanced fusion mode | True | True/False |
| `flatten_images` | Handle RGBA→RGB conversion | True | True/False |
| `resize_mode` | Image resizing strategy | fit_largest | fit_largest, fit_smallest, no_resize |
| `gap_pixels` | Space between combined images | 10 | 0-100 |
| `model` | Kontext model to use | flux-kontext-pro | pro/max |
| `aspect_ratio` | Output image ratio | 1:1 | Various ratios |
| `seed` | Random seed | -1 | -1 to 2147483647 |

## 🧠 Fusion Mastery Guide

### 🎯 **FUNDAMENTAL PRINCIPLE**
**Your prompt determines HOW the AI interprets and fuses your images.** The combination_mode creates the reference layout, but your **prompt language** controls the fusion strategy.

### 🔥 **COMBINATION MODE STRATEGIES**

#### **side_by_side (BEST FOR CHARACTER FUSION)**
**When to use:** Merging people, faces, or distinct subjects
**Prompt approach:** Direct fusion language
```
✅ "merge the two people into one person"
✅ "combine their best features into a single character"
✅ "the woman and child as one unified person"
```

#### **overlay (BEST FOR STYLE/ATMOSPHERE)**
**When to use:** Style transfer, mood blending, artistic effects
**Prompt approach:** Atmospheric and stylistic language
```
✅ "apply the vintage mood to the modern portrait"
✅ "blend the lighting and atmosphere from both images"
✅ "combine the artistic style with the main subject"
```

#### **grid_2x2 (BEST FOR MULTI-ELEMENT SCENES)**
**When to use:** Complex scenes with multiple objects/elements
**Prompt approach:** Spatial and compositional language
```
✅ "arrange all elements in a cohesive interior scene"
✅ "create a unified composition from all four elements"
✅ "blend the room elements with the people naturally"
```

#### **all_in_one (BATCH PROCESSING)**
**When to use:** Processing multiple variations simultaneously
**Prompt approach:** Consistent transformation language
```
✅ "apply the same artistic style to all subjects"
✅ "transform each person with the same lighting effect"
✅ "create consistent character variations"
```

### 📝 **PROMPT FRAMEWORKS**

#### **LEVEL 1: BASIC FUSION PROMPTS**
```
Subject Fusion: "[Person A] combined with [Person B] as [desired outcome]"
Object Integration: "merge [object] with [object] into [result]"
Style Transfer: "[subject] in the style of [reference style]"
```

**Examples:**
- ✅ "the blonde woman holding the small dog in a restaurant"
- ✅ "combine the child's innocence with the woman's elegance"
- ✅ "merge the two hairstyles into one unique look"

#### **LEVEL 2: ADVANCED FUSION PROMPTS**
```
Characteristic Fusion: "blend [specific features] from both subjects"
Environmental Integration: "[subject] naturally placed in [environment] with [lighting/mood]"
Temporal Fusion: "[age/time reference] version of [combined subjects]"
```

**Examples:**
- ✅ "blend the woman's facial features with the child's eye color and smile"
- ✅ "the combined person sitting naturally in the restaurant with warm lighting"
- ✅ "teenage version combining both their facial structures"

#### **LEVEL 3: EXPERT FUSION PROMPTS**
```
Multi-Attribute Control: "[feature 1] + [feature 2] + [environment] + [mood] + [style]"
Narrative Fusion: "[story context] showing [relationship] between [fused elements]"
Technical Specifications: "[specific technical requirements] for [fusion result]"
```

**Examples:**
- ✅ "blonde curly hair + bright eyes + cozy restaurant + happy expression + professional portrait style"
- ✅ "mother-daughter bond visualized as one person showing both generations"
- ✅ "photorealistic fusion maintaining facial symmetry and natural lighting"

### 🚫 **COMMON MISTAKES & FIXES**

#### **❌ MISTAKE: Scene Description Instead of Fusion**
```
Wrong: "two people sitting in a restaurant"
✅ Right: "the combined person sitting in the restaurant"
```

#### **❌ MISTAKE: Vague Fusion Instructions**
```
Wrong: "mix them together"
✅ Right: "blend the woman's features with the child's smile and eye color"
```

#### **❌ MISTAKE: Conflicting Requirements**
```
Wrong: "keep both people separate but combine them"
✅ Right: "merge both people into one unified character"
```

#### **❌ MISTAKE: Over-Complex Prompts**
```
Wrong: "create a fusion of the woman and child while maintaining their individual characteristics but also blending them into one person with specific features..."
✅ Right: "blend the woman and child into one person with combined features"
```

## 📖 Example Workflows

### Standard Text Editing

```
Input: Photo of person wearing blue shirt
Prompt: "Change the shirt color to red"
Result: Same person now wearing red shirt
```

### Character Fusion (Experimental)

```
Input 1: Photo of blonde woman
Input 2: Photo of child with dog
Mode: side_by_side + force_fusion=True
Prompt: "the blonde woman holding the dog in a restaurant"
Result: Single person (fusion of both) holding dog in restaurant setting
```

### Style Transfer (Experimental)

```
Input 1: Modern portrait
Input 2: Vintage photo
Mode: overlay + force_fusion=False
Prompt: "apply the vintage aesthetic to the modern portrait"
Result: Modern person with vintage styling and atmosphere
```

### Multi-Element Scene (Experimental)

```
Input: 4 different room elements
Mode: grid_2x2 + force_fusion=True
Prompt: "create a cohesive living room with all these elements"
Result: Unified interior design combining all elements
```

### Standard Example Prompts

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

### Safety Tolerance Guide

- **0-2**: Very strict content filtering
- **3-4**: Balanced filtering (recommended)
- **5-6**: More permissive for creative work

## 🔬 Advanced Techniques

### **🔄 force_fusion Parameter**

#### **force_fusion = True (RECOMMENDED FOR FUSION)**
- **Use for:** All character/object fusion tasks
- **Effect:** Activates advanced fusion prompting system
- **Prompt style:** Direct fusion language
- **Result:** True blending and merging of elements

#### **force_fusion = False**
- **Use for:** Scene enhancement, style application
- **Effect:** Standard Kontext processing
- **Prompt style:** Traditional editing language
- **Result:** Scene modification and enhancement

### **📏 Optimal Image Counts**
- **2 images:** Perfect for character fusion
- **3-4 images:** Good for complex scenes
- **5+ images:** Use with grid or all_in_one modes

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

## 🛠 **PARAMETER OPTIMIZATION GUIDE**

### **🎨 Model Selection**
- **flux-kontext-pro:** Balanced speed and quality, ideal for most fusion tasks
- **flux-kontext-max:** Maximum quality and prompt adherence for critical fusions

### **📐 Combination Mode Selection**
```
Character Fusion: side_by_side + force_fusion=True + direct prompts
Style Transfer: overlay + force_fusion=False + atmospheric prompts
Complex Scenes: grid_2x2 + force_fusion=True + spatial prompts
Batch Processing: all_in_one + force_fusion=False + consistent prompts
```

### **🎯 Resize Mode Selection**
- **fit_largest:** Best for maintaining detail in high-res images
- **fit_smallest:** Good for consistent sizing across all images
- **no_resize:** Use when all images are already properly sized

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

**Fusion not working properly:**
- Ensure `force_fusion=True` for character merging
- Use fusion-specific prompt language (see guide above)
- Try `side_by_side` mode for best character fusion results
- Check that you're using singular language ("the person" not "two people")

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
| "Failed to combine images" | Check image formats and try different resize_mode |
| "No valid images provided" | Ensure images are properly connected to inputs |

## 🎉 **SUCCESS EXAMPLES**

### **Real User Success:**
**Input:** Dog photo + Woman with child photo
**Settings:** `side_by_side` + `force_fusion=True`
**Prompt:** *"the blond girl alone hold the dog in restaurant"*
**Result:** ✅ Perfect fusion - single person holding dog in restaurant

**Why it worked:**
1. **Singular language** ("the blond girl") implies fusion
2. **Clear action** ("hold the dog") provides specific interaction
3. **Environmental context** ("in restaurant") sets the scene
4. **Simple structure** without over-complication

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
- All contributors and users who helped develop the fusion techniques
- Special thanks to the community for breakthrough fusion discoveries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ShmuelRonen/FluxKontextCreator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ShmuelRonen/FluxKontextCreator/discussions)
- **BFL API Support**: [BFL Documentation](https://docs.bfl.ai)

## 🏆 **MASTERY CHECKLIST**

- [ ] Understand combination_mode effects on reference layout
- [ ] Know when to use force_fusion=True vs False
- [ ] Can write fusion vs enhancement prompts
- [ ] Use specific targeting for precise control
- [ ] Apply iterative refinement workflow
- [ ] Test parameter combinations systematically
- [ ] Build personal prompt template library
- [ ] Achieve consistent, high-quality fusion results

## ⭐ Show Your Support

If this project helps you create impossible fusions and amazing edits, please consider giving it a star on GitHub!

---

**Made with ❤️ and 🔥 for the ComfyUI community**

**🚀 Ready to create the impossible? Start with simple character fusion and work your way up to master-level techniques!**
