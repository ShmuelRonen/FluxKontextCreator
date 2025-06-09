import requests
from PIL import Image
import io
import numpy as np
import torch
import os
import configparser
import time
import base64
from enum import Enum

class Status(Enum):
    PENDING = "Pending"
    READY = "Ready"
    ERROR = "Error"

class ConfigLoader:
    """
    Configuration loader for BFL API credentials
    Reads X_KEY and BASE_URL from config.ini file
    Compatible with existing config format
    """
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "config.ini")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}. Please ensure config.ini exists in the same directory as the script.")
            
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.set_api_config()

    def set_api_config(self):
        """Set API configuration from config file"""
        try:
            if not self.config.has_section('API'):
                raise KeyError("Section 'API' not found in config file")
            
            # Set X_KEY
            if not self.config.has_option('API', 'X_KEY'):
                raise KeyError("X_KEY not found in API section")
            x_key = self.config['API']['X_KEY']
            if not x_key:
                raise KeyError("X_KEY cannot be empty")
            os.environ["X_KEY"] = x_key
            
            # Set BASE_URL (with fallback to correct API endpoint)
            if self.config.has_option('API', 'BASE_URL'):
                base_url = self.config['API']['BASE_URL']
                # Fix common URL issues
                if base_url == "https://api.bfl.ml":
                    print("[FLUX KONTEXT] Warning: api.bfl.ml is the docs site. Using api.bfl.ai for API calls")
                    base_url = "https://api.bfl.ai"
                elif not base_url.startswith('http'):
                    base_url = f"https://{base_url}"
            else:
                base_url = "https://api.bfl.ai"  # Default to main API
                
            os.environ["BASE_URL"] = base_url
            print(f"[FLUX KONTEXT] Using API endpoint: {base_url}")
            
        except KeyError as e:
            print(f"[FLUX KONTEXT] Error setting API config: {str(e)}")
            print("[FLUX KONTEXT] Please ensure your config.ini contains X_KEY under the [API] section")
            raise

class FluxKontextCreator:
    """
    Flux Kontext Image Editor Node for ComfyUI
    
    This node allows users to edit images using simple text instructions
    via Black Forest Labs' Flux Kontext API. It supports both Pro and Max models
    for high-quality, contextual image editing.
    
    Features:
    - Text-based image editing
    - Character consistency across edits
    - Local editing without affecting other parts
    - Fast processing (3-5 seconds)
    - Compatible with existing BFL config format
    """
    
    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "edit_image"
    CATEGORY = "BFL/Kontext"

    def __init__(self):
        """Initialize the Flux Kontext Creator with config loader"""
        try:
            self.config_loader = ConfigLoader()
        except Exception as e:
            print(f"[FLUX KONTEXT] Initialization Error: {str(e)}")
            print("[FLUX KONTEXT] Please ensure config.ini is properly set up with API credentials")
            raise

    @classmethod
    def INPUT_TYPES(cls):
        """Define input parameters for the ComfyUI node"""
        return {
            "required": {
                "input_image": ("IMAGE",),
                "edit_instruction": ("STRING", {
                    "default": "Change the car color to red", 
                    "multiline": True,
                    "placeholder": "Example: Change the person's shirt to blue"
                }),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
                "aspect_ratio": ([
                    "1:1", "4:3", "3:4", "16:9", "9:16", "21:9", "9:21"
                ], {"default": "1:1"}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 4, "min": 0, "max": 6}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
                "keep_original_on_fail": ("BOOLEAN", {"default": True}),
            }
        }

    def edit_image(self, input_image, edit_instruction, model, aspect_ratio, 
                   output_format, safety_tolerance, seed=-1, keep_original_on_fail=True):
        """
        Main function to edit image using Flux Kontext API
        
        Args:
            input_image: ComfyUI image tensor
            edit_instruction: Text instruction for editing
            model: flux-kontext-pro or flux-kontext-max
            aspect_ratio: Desired aspect ratio
            output_format: png or jpeg
            safety_tolerance: Safety level (0-6)
            seed: Random seed (-1 for random)
            keep_original_on_fail: Return original image if editing fails
            
        Returns:
            Tuple of (edited_image_tensor, status_message)
        """
        print(f"[FLUX KONTEXT] Starting image edit with {model}")
        print(f"[FLUX KONTEXT] Instruction: {edit_instruction}")
        
        # Validate edit instruction
        if not edit_instruction.strip():
            error_msg = "Edit instruction cannot be empty"
            print(f"[FLUX KONTEXT] Error: {error_msg}")
            if keep_original_on_fail:
                return (input_image, f"❌ {error_msg}")
            else:
                return (*self.create_blank_image(), f"❌ {error_msg}")

        try:
            # Convert input image to base64
            print("[FLUX KONTEXT] Converting image to base64...")
            input_pil = self.tensor_to_pil(input_image)
            if input_pil is None:
                error_msg = "Failed to convert input image"
                print(f"[FLUX KONTEXT] Error: {error_msg}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
            
            base64_image = self.pil_to_base64(input_pil)
            if base64_image is None:
                error_msg = "Failed to encode image to base64"
                print(f"[FLUX KONTEXT] Error: {error_msg}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
            
            # Build API request payload
            payload = {
                "prompt": edit_instruction,
                "input_image": base64_image,
                "aspect_ratio": aspect_ratio,
                "safety_tolerance": safety_tolerance,
                "output_format": output_format
            }
            
            # Add seed if specified
            if seed >= 0:
                payload["seed"] = seed

            # Get base URL and construct endpoint
            base_url = os.environ.get("BASE_URL", "https://api.bfl.ai")
            if model == "flux-kontext-max":
                url = f"{base_url}/v1/flux-kontext-max"
            else:
                url = f"{base_url}/v1/flux-kontext-pro"

            # Check API key
            x_key = os.environ.get("X_KEY")
            if not x_key:
                error_msg = "X_KEY not found. Check your config.ini"
                print(f"[FLUX KONTEXT] Error: {error_msg}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")

            headers = {"x-key": x_key}
            
            # Send API request
            print(f"[FLUX KONTEXT] Sending request to: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"[FLUX KONTEXT] Response Status: {response.status_code}")
            
            # Handle API response
            if response.status_code == 200:
                response_data = response.json()
                task_id = response_data.get("id")
                
                if not task_id:
                    error_msg = "No task ID received from server"
                    print(f"[FLUX KONTEXT] Error: {error_msg}")
                    print(f"[FLUX KONTEXT] Response: {response_data}")
                    if keep_original_on_fail:
                        return (input_image, f"❌ {error_msg}")
                    else:
                        return (*self.create_blank_image(), f"❌ {error_msg}")
                
                print(f"[FLUX KONTEXT] Task ID: {task_id}")
                
                # Wait for result
                result_image = self.wait_for_result(task_id, output_format)
                
                if result_image is not None:
                    success_msg = f"✅ {model} edit complete: {edit_instruction[:50]}..."
                    print(f"[FLUX KONTEXT] Success: {edit_instruction}")
                    return (result_image, success_msg)
                else:
                    error_msg = "Failed to generate edited image"
                    print(f"[FLUX KONTEXT] Error: {error_msg}")
                    if keep_original_on_fail:
                        return (input_image, f"❌ {error_msg}")
                    else:
                        return (*self.create_blank_image(), f"❌ {error_msg}")
                        
            # Handle various HTTP error codes
            elif response.status_code == 400:
                error_msg = "Invalid request parameters"
                print(f"[FLUX KONTEXT] Error 400: {response.text}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
                    
            elif response.status_code == 401:
                error_msg = "Invalid API key"
                print(f"[FLUX KONTEXT] Error 401: Check your X_KEY in config.ini")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
                    
            elif response.status_code == 402:
                error_msg = "Insufficient credits in BFL account"
                print(f"[FLUX KONTEXT] Error 402: {response.text}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
                    
            else:
                error_msg = f"Server error: {response.status_code}"
                print(f"[FLUX KONTEXT] Error: {error_msg}")
                print(f"[FLUX KONTEXT] Response: {response.text}")
                if keep_original_on_fail:
                    return (input_image, f"❌ {error_msg}")
                else:
                    return (*self.create_blank_image(), f"❌ {error_msg}")
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - try again"
            print(f"[FLUX KONTEXT] Error: {error_msg}")
            if keep_original_on_fail:
                return (input_image, f"❌ {error_msg}")
            else:
                return (*self.create_blank_image(), f"❌ {error_msg}")
                
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - check internet"
            print(f"[FLUX KONTEXT] Error: {error_msg}")
            if keep_original_on_fail:
                return (input_image, f"❌ {error_msg}")
            else:
                return (*self.create_blank_image(), f"❌ {error_msg}")
                
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"[FLUX KONTEXT] Error: {error_msg}")
            print(f"[FLUX KONTEXT] Error Type: {type(e).__name__}")
            if keep_original_on_fail:
                return (input_image, f"❌ {error_msg}")
            else:
                return (*self.create_blank_image(), f"❌ {error_msg}")

    def tensor_to_pil(self, tensor):
        """
        Convert ComfyUI image tensor to PIL Image
        
        Args:
            tensor: ComfyUI image tensor [batch, height, width, channels]
            
        Returns:
            PIL Image object or None if conversion fails
        """
        try:
            # Handle tensor dimensions
            if len(tensor.shape) == 4:
                img_array = tensor[0].cpu().numpy()  # Take first image from batch
            else:
                img_array = tensor.cpu().numpy()
            
            # Convert value range
            if img_array.max() <= 1.0:
                # Values in [0,1] range, convert to [0,255]
                img_array = (img_array * 255).astype(np.uint8)
            else:
                # Values already in [0,255] range
                img_array = img_array.astype(np.uint8)
            
            # Ensure RGB format
            if len(img_array.shape) == 2:
                # Grayscale, convert to RGB
                img_array = np.stack([img_array] * 3, axis=-1)
            elif img_array.shape[-1] == 4:
                # RGBA, remove alpha channel
                img_array = img_array[:, :, :3]
            
            pil_image = Image.fromarray(img_array, mode='RGB')
            print(f"[FLUX KONTEXT] Image converted: {pil_image.size}")
            return pil_image
            
        except Exception as e:
            print(f"[FLUX KONTEXT] Error converting tensor to PIL: {str(e)}")
            return None

    def pil_to_base64(self, pil_image):
        """
        Convert PIL Image to base64 string
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            Base64 encoded string or None if conversion fails
        """
        try:
            # Save to buffer
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            
            # Convert to base64
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            print(f"[FLUX KONTEXT] Image encoded to base64: {len(img_base64)} chars")
            return img_base64
            
        except Exception as e:
            print(f"[FLUX KONTEXT] Error converting PIL to base64: {str(e)}")
            return None

    def wait_for_result(self, task_id, output_format, max_attempts=20):
        """
        Poll the API for editing result
        
        Args:
            task_id: Task ID from initial API request
            output_format: Desired output format
            max_attempts: Maximum polling attempts
            
        Returns:
            ComfyUI image tensor or None if failed
        """
        print(f"[FLUX KONTEXT] Waiting for result: {task_id}")
        base_url = os.environ.get("BASE_URL", "https://api.bfl.ai")
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Progressive wait time
                wait_time = min(2 + attempt, 15)
                print(f"[FLUX KONTEXT] Attempt {attempt}/{max_attempts} - waiting {wait_time}s")
                time.sleep(wait_time)
                
                # Check task status
                get_url = f"{base_url}/v1/get_result?id={task_id}"
                headers = {"x-key": os.environ["X_KEY"]}
                
                response = requests.get(get_url, headers=headers, timeout=30)
                
                if response.status_code != 200:
                    print(f"[FLUX KONTEXT] Status check failed: {response.status_code}")
                    continue
                
                result = response.json()
                status = result.get("status", "Unknown")
                print(f"[FLUX KONTEXT] Status: {status}")
                
                if status == Status.READY.value:
                    # Image is ready
                    sample_url = result.get('result', {}).get('sample')
                    if not sample_url:
                        print("[FLUX KONTEXT] Error: No sample URL in response")
                        return None
                    
                    # Download the image
                    print(f"[FLUX KONTEXT] Downloading: {sample_url}")
                    img_response = requests.get(sample_url, timeout=30)
                    
                    if img_response.status_code != 200:
                        print(f"[FLUX KONTEXT] Download failed: {img_response.status_code}")
                        return None
                    
                    # Convert to tensor
                    img = Image.open(io.BytesIO(img_response.content))
                    img = img.convert('RGB')  # Ensure RGB format
                    
                    # Convert to numpy then tensor
                    img_array = np.array(img).astype(np.float32) / 255.0
                    img_tensor = torch.from_numpy(img_array)[None,]  # Add batch dimension
                    
                    print(f"[FLUX KONTEXT] Success! Image size: {img.size}")
                    return img_tensor
                    
                elif status == Status.PENDING.value:
                    # Still processing
                    continue
                    
                elif status == Status.ERROR.value:
                    print(f"[FLUX KONTEXT] Task failed with error: {result}")
                    return None
                    
                else:
                    print(f"[FLUX KONTEXT] Unknown status: {status}")
                    continue
                    
            except Exception as e:
                print(f"[FLUX KONTEXT] Error checking result: {str(e)}")
                continue
        
        print(f"[FLUX KONTEXT] Timeout: Max attempts ({max_attempts}) reached")
        return None

    def create_blank_image(self):
        """
        Create a blank black image for error cases
        
        Returns:
            Tuple containing blank image tensor
        """
        blank_img = Image.new('RGB', (512, 512), color='black')
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor,)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FluxKontextCreator": FluxKontextCreator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxKontextCreator": "🎨 Flux Kontext Creator"
}