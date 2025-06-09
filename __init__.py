"""
Flux Kontext Creator Node for ComfyUI

Text-based image editing using Black Forest Labs' Flux Kontext API
Compatible with existing BFL config format
"""

from .flux_kontext_creator import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("[FLUX KONTEXT] 🎨 Flux Kontext Creator loaded successfully")
print("[FLUX KONTEXT] Ready for text-based image editing!")