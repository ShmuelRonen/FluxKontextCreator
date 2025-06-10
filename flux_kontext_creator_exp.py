import torch
import numpy as np
from PIL import Image
import io
import base64
import requests
import time
import os
from enum import Enum

class Status(Enum):
    PENDING = "Pending"
    READY = "Ready"
    ERROR = "Error"

class FluxKontextCreatorExperimental:
    """
    Advanced Flux Kontext Creator with image combination, flattening, and fusion capabilities.
    Integrates CombineImages functionality and PS Flatten Image for comprehensive processing.
    Uses BFL (Black Forest Labs) Flux Kontext API for real image processing.
    
    SETUP INSTRUCTIONS:
    1. Make sure you have proper config.ini with X_KEY from https://api.bfl.ai
    2. Install required packages: pip install requests pillow
    """
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "combined_prompt")
    FUNCTION = "process_images"
    OUTPUT_NODE = True
    CATEGORY = "Flux Kontext/Advanced"

    def __init__(self):
        """Initialize with config loader"""
        try:
            # Use the same config loader from the main node
            from .flux_kontext_creator import ConfigLoader
            self.config_loader = ConfigLoader()
        except Exception as e:
            print(f"[FLUX KONTEXT EXPERIMENTAL] Initialization Error: {str(e)}")
            # Fallback initialization if main node not available
            pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "Merge these two people into one person combining their best features"}),
                "number_of_images": ("INT", {"default": 2, "min": 1, "max": 10, "step": 1}),
                "combination_mode": (["side_by_side", "overlay", "grid_2x2", "all_in_one", "no_combine"], {"default": "side_by_side"}),
                "force_fusion": ("BOOLEAN", {"default": True}),
                "flatten_images": ("BOOLEAN", {"default": True}),
                "image_1": ("IMAGE",),
            },
            "optional": {
                **{f"image_{i}": ("IMAGE",) for i in range(2, 11)},
                "resize_mode": (["fit_largest", "fit_smallest", "no_resize"], {"default": "fit_largest"}),
                "gap_pixels": ("INT", {"default": 10, "min": 0, "max": 100, "step": 1}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
                "aspect_ratio": (["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "9:21"], {"default": "1:1"}),
                "output_format": (["png", "jpeg"], {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 4, "min": 0, "max": 6}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647}),
            }
        }

    def process_images(self, prompt, number_of_images, combination_mode, force_fusion, flatten_images, **kwargs):
        """
        Main processing function that combines images, flattens them, and applies Flux Kontext with fusion strategies.
        """
        
        # Extract parameters
        resize_mode = kwargs.get("resize_mode", "fit_largest")
        gap_pixels = kwargs.get("gap_pixels", 10)
        model = kwargs.get("model", "flux-kontext-pro")
        aspect_ratio = kwargs.get("aspect_ratio", "1:1")
        output_format = kwargs.get("output_format", "png")
        safety_tolerance = kwargs.get("safety_tolerance", 4)
        seed = kwargs.get("seed", -1)
        
        # Collect input images
        images = []
        for i in range(1, number_of_images + 1):
            img = kwargs.get(f"image_{i}", None)
            if img is not None:
                images.append(img)
        
        if not images:
            return self._create_error_response("No valid images provided")
        
        print(f"[FLUX KONTEXT EXPERIMENTAL] Processing {len(images)} images with combination_mode: {combination_mode}")
        
        try:
            # Step 1: Flatten images if requested (handle RGBA -> RGB)
            if flatten_images:
                images = [self._flatten_image(img) for img in images]
            
            # Step 2: Combine images based on mode
            if len(images) > 1 and combination_mode != "no_combine":
                combined_image = self._combine_images(images, combination_mode, resize_mode, gap_pixels)
                final_image = combined_image
            else:
                final_image = images[0]
            
            # Step 3: Generate enhanced prompt for fusion
            enhanced_prompt = self._generate_fusion_prompt(prompt, len(images), force_fusion, combination_mode)
            
            # Step 4: Process through BFL Flux Kontext API
            result_image = self._flux_kontext_process(final_image, enhanced_prompt, model, aspect_ratio, output_format, safety_tolerance, seed)
            
            if result_image is not None:
                success_msg = f"✅ Flux Kontext fusion complete: {combination_mode} mode"
                return (result_image, success_msg)
            else:
                return self._create_error_response("Flux Kontext processing failed")
                
        except Exception as e:
            error_msg = f"Processing error: {str(e)}"
            print(f"[FLUX KONTEXT EXPERIMENTAL] {error_msg}")
            return self._create_error_response(error_msg)
    
    def _flatten_image(self, image_tensor):
        """
        Flatten RGBA images to RGB with white background, similar to Photoshop's flatten.
        """
        # Handle batch dimension
        if image_tensor.dim() == 4 and image_tensor.shape[0] == 1:
            image_tensor = image_tensor.squeeze(0)
        
        height, width = image_tensor.shape[0], image_tensor.shape[1]
        
        # Check if we have RGBA (4 channels) or just RGB (3 channels)
        if len(image_tensor.shape) == 3 and image_tensor.shape[2] == 4:
            # RGBA case - handle the alpha channel
            white_bg = torch.ones((height, width, 3), device=image_tensor.device)
            rgb = image_tensor[:, :, 0:3]
            alpha = image_tensor[:, :, 3:4]
            alpha_expanded = alpha.expand(-1, -1, 3)
            result = rgb * alpha_expanded + white_bg * (1.0 - alpha_expanded)
            return result.unsqueeze(0)  # Add batch dimension back
        else:
            # RGB case - no alpha channel to handle
            if image_tensor.dim() == 3:
                image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
            return image_tensor
    
    def _combine_images(self, images, combination_mode, resize_mode, gap_pixels):
        """
        Combine multiple images using various methods.
        """
        
        # Convert tensors to PIL Images for easier manipulation
        pil_images = []
        for img_tensor in images:
            # Handle batch dimension
            if img_tensor.dim() == 4:
                img_tensor = img_tensor.squeeze(0)
            
            # Ensure correct format [H, W, C] and range [0, 1]
            if img_tensor.shape[-1] in [3, 4]:  # [H, W, C]
                img_array = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            else:  # [C, H, W] - need to permute
                img_array = (img_tensor.permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
            
            pil_images.append(Image.fromarray(img_array))
        
        # Apply resizing if needed
        if resize_mode != "no_resize":
            pil_images = self._resize_images(pil_images, resize_mode)
        
        # Combine based on mode
        if combination_mode == "side_by_side":
            combined_pil = self._side_by_side_combine(pil_images, gap_pixels)
        elif combination_mode == "overlay":
            combined_pil = self._overlay_combine(pil_images)
        elif combination_mode == "grid_2x2":
            combined_pil = self._grid_combine(pil_images, gap_pixels)
        elif combination_mode == "all_in_one":
            # Stack images in batch dimension
            return self._all_in_one_combine(images)
        else:
            combined_pil = pil_images[0]  # Default to first image
        
        # Convert back to tensor
        combined_array = np.array(combined_pil).astype(np.float32) / 255.0
        combined_tensor = torch.from_numpy(combined_array).unsqueeze(0)  # Add batch dimension
        
        print(f"[FLUX KONTEXT EXPERIMENTAL] Combined image size: {combined_pil.size}")
        return combined_tensor
    
    def _resize_images(self, pil_images, resize_mode):
        """Resize PIL images according to mode."""
        if resize_mode == "fit_largest":
            max_width = max(img.width for img in pil_images)
            max_height = max(img.height for img in pil_images)
            target_size = (max_width, max_height)
        elif resize_mode == "fit_smallest":
            min_width = min(img.width for img in pil_images)
            min_height = min(img.height for img in pil_images)
            target_size = (min_width, min_height)
        else:
            return pil_images
        
        return [img.resize(target_size, Image.Resampling.LANCZOS) for img in pil_images]
    
    def _side_by_side_combine(self, pil_images, gap_pixels):
        """Combine images horizontally side by side."""
        total_width = sum(img.width for img in pil_images) + gap_pixels * (len(pil_images) - 1)
        max_height = max(img.height for img in pil_images)
        
        combined = Image.new('RGB', (total_width, max_height), (255, 255, 255))
        
        x_offset = 0
        for img in pil_images:
            y_offset = (max_height - img.height) // 2
            combined.paste(img, (x_offset, y_offset))
            x_offset += img.width + gap_pixels
        
        return combined
    
    def _overlay_combine(self, pil_images):
        """Combine images with transparency overlay."""
        if len(pil_images) < 2:
            return pil_images[0]
        
        base_img = pil_images[0].convert('RGBA')
        
        for i, img in enumerate(pil_images[1:], 1):
            overlay = img.convert('RGBA').resize(base_img.size, Image.Resampling.LANCZOS)
            alpha = int(255 * (0.7 ** i))
            overlay.putalpha(alpha)
            base_img = Image.alpha_composite(base_img, overlay)
        
        return base_img.convert('RGB')
    
    def _grid_combine(self, pil_images, gap_pixels):
        """Combine images in 2x2 grid."""
        while len(pil_images) < 4:
            white_img = Image.new('RGB', pil_images[0].size, (255, 255, 255))
            pil_images.append(white_img)
        
        pil_images = pil_images[:4]  # Take only first 4
        
        img_width, img_height = pil_images[0].size
        total_width = img_width * 2 + gap_pixels
        total_height = img_height * 2 + gap_pixels
        
        combined = Image.new('RGB', (total_width, total_height), (255, 255, 255))
        
        positions = [
            (0, 0), (img_width + gap_pixels, 0),
            (0, img_height + gap_pixels), (img_width + gap_pixels, img_height + gap_pixels)
        ]
        
        for img, pos in zip(pil_images, positions):
            combined.paste(img, pos)
        
        return combined
    
    def _all_in_one_combine(self, images):
        """Stack images in batch dimension."""
        shapes = [img.shape for img in images]
        if len(set(shapes)) > 1:
            raise ValueError(f"All images must have same resolution for all_in_one. Found: {shapes}")
        
        stacked = torch.cat(images, dim=0)
        return stacked
    
    def _generate_fusion_prompt(self, user_prompt, num_images, force_fusion, combination_mode):
        """
        Generate enhanced prompts based on our fusion strategies.
        """
        
        if force_fusion and num_images >= 2:
            if combination_mode in ["side_by_side", "grid_2x2", "overlay"]:
                # Single-input fusion mode - THE BREAKTHROUGH STRATEGY
                enhanced_prompt = (
                    f"SINGLE-INPUT FUSION MODE: You are viewing a reference image containing multiple subjects/elements. "
                    f"Task: {user_prompt}. "
                    f"FUSION APPROACH: When working with people - merge their characteristics, features, and styles to create ONE unified person. "
                    f"When working with objects and environments - seamlessly integrate elements with natural placement and lighting. "
                    f"EXTRACTION EXCELLENCE: Focus on the specific elements mentioned in the task and blend them masterfully. "
                    f"Treat this as a character/element extraction and fusion task, not a scene combination task. "
                    f"TECHNICAL STANDARDS: Ensure consistent lighting, proper scale relationships, seamless integration, and photo-realistic quality. "
                    f"The result should appear as a single, cohesive creation rather than separate combined elements."
                )
            else:
                # Multi-element synthesis
                enhanced_prompt = (
                    f"MULTI-ELEMENT SYNTHESIS: Process this reference containing {num_images} elements. Task: {user_prompt}. "
                    f"FUSION MASTERY: Extract and blend the specified elements with seamless integration, consistent lighting, "
                    f"harmonious color balance, and natural atmospheric effects. Focus on creating one unified result that "
                    f"incorporates all relevant elements with professional-grade visual quality and polished composition."
                )
        else:
            # Regular mode
            enhanced_prompt = (
                f"Process the reference image(s) according to this instruction: {user_prompt}. "
                f"Focus on high-quality execution with proper lighting, composition, and realistic details."
            )
        
        print(f"[FLUX KONTEXT EXPERIMENTAL] Enhanced prompt: {enhanced_prompt[:100]}...")
        return enhanced_prompt
    
    def _flux_kontext_process(self, image_tensor, enhanced_prompt, model, aspect_ratio, output_format, safety_tolerance, seed):
        """
        Process through BFL Flux Kontext API using the same pattern as the working implementation.
        """
        try:
            # Convert tensor to PIL Image for API upload
            if image_tensor.dim() == 4:
                image_tensor = image_tensor.squeeze(0)
            
            img_array = (image_tensor.cpu().numpy() * 255).astype(np.uint8)
            pil_image = Image.fromarray(img_array)
            
            # Convert to base64
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Build API request payload (matching working implementation)
            payload = {
                "prompt": enhanced_prompt,
                "input_image": img_base64,
                "aspect_ratio": aspect_ratio,
                "safety_tolerance": safety_tolerance,
                "output_format": output_format
            }
            
            # Add seed if specified
            if seed >= 0:
                payload["seed"] = seed

            # Get base URL and construct endpoint (matching working implementation)
            base_url = os.environ.get("BASE_URL", "https://api.bfl.ai")
            if model == "flux-kontext-max":
                url = f"{base_url}/v1/flux-kontext-max"
            else:
                url = f"{base_url}/v1/flux-kontext-pro"

            # Check API key (matching working implementation)
            x_key = os.environ.get("X_KEY")
            if not x_key:
                print("[FLUX KONTEXT EXPERIMENTAL] Error: X_KEY not found. Check your config.ini")
                return None

            headers = {"x-key": x_key}
            
            # Send API request
            print(f"[FLUX KONTEXT EXPERIMENTAL] Sending request to: {url}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"[FLUX KONTEXT EXPERIMENTAL] Response Status: {response.status_code}")
            
            # Handle API response (matching working implementation)
            if response.status_code == 200:
                response_data = response.json()
                task_id = response_data.get("id")
                
                if not task_id:
                    print("[FLUX KONTEXT EXPERIMENTAL] Error: No task ID received from server")
                    return None
                
                print(f"[FLUX KONTEXT EXPERIMENTAL] Task ID: {task_id}")
                
                # Wait for result using the same polling logic
                result_image = self._wait_for_result(task_id, base_url, x_key)
                return result_image
                        
            # Handle various HTTP error codes (matching working implementation)
            elif response.status_code == 400:
                print(f"[FLUX KONTEXT EXPERIMENTAL] Error 400: Invalid request parameters - {response.text}")
            elif response.status_code == 401:
                print(f"[FLUX KONTEXT EXPERIMENTAL] Error 401: Invalid API key - Check your X_KEY")
            elif response.status_code == 402:
                print(f"[FLUX KONTEXT EXPERIMENTAL] Error 402: Insufficient credits in BFL account - {response.text}")
            else:
                print(f"[FLUX KONTEXT EXPERIMENTAL] Error {response.status_code}: {response.text}")
                
            return None
                
        except Exception as e:
            print(f"[FLUX KONTEXT EXPERIMENTAL] API Exception: {str(e)}")
            return None
    
    def _wait_for_result(self, task_id, base_url, x_key, max_attempts=20):
        """Poll the API for editing result (matching working implementation)"""
        print(f"[FLUX KONTEXT EXPERIMENTAL] Waiting for result: {task_id}")
        
        for attempt in range(1, max_attempts + 1):
            try:
                wait_time = min(2 + attempt, 15)
                print(f"[FLUX KONTEXT EXPERIMENTAL] Attempt {attempt}/{max_attempts} - waiting {wait_time}s")
                time.sleep(wait_time)
                
                get_url = f"{base_url}/v1/get_result?id={task_id}"
                headers = {"x-key": x_key}
                
                response = requests.get(get_url, headers=headers, timeout=30)
                
                if response.status_code != 200:
                    continue
                
                result = response.json()
                status = result.get("status", "Unknown")
                print(f"[FLUX KONTEXT EXPERIMENTAL] Status: {status}")
                
                if status == Status.READY.value:
                    sample_url = result.get('result', {}).get('sample')
                    if not sample_url:
                        return None
                    
                    print(f"[FLUX KONTEXT EXPERIMENTAL] Downloading result...")
                    img_response = requests.get(sample_url, timeout=30)
                    
                    if img_response.status_code != 200:
                        return None
                    
                    img = Image.open(io.BytesIO(img_response.content))
                    img = img.convert('RGB')
                    
                    img_array = np.array(img).astype(np.float32) / 255.0
                    img_tensor = torch.from_numpy(img_array)[None,]
                    
                    print(f"[FLUX KONTEXT EXPERIMENTAL] Success! Result size: {img.size}")
                    return img_tensor
                    
                elif status == Status.PENDING.value:
                    continue
                elif status == Status.ERROR.value:
                    print(f"[FLUX KONTEXT EXPERIMENTAL] Task failed with error status")
                    return None
                else:
                    continue
                    
            except Exception as e:
                print(f"[FLUX KONTEXT EXPERIMENTAL] Polling error: {str(e)}")
                continue
        
        print(f"[FLUX KONTEXT EXPERIMENTAL] Timeout after {max_attempts} attempts")
        return None
    
    def _create_error_response(self, error_msg):
        """Create error response with blank image"""
        blank_img = Image.new('RGB', (512, 512), color='black')
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor, f"❌ {error_msg}")

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FluxKontextCreatorExperimental": FluxKontextCreatorExperimental
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxKontextCreatorExperimental": "🔥 Flux Kontext Creator Experimental"
}