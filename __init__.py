"""
Flux Kontext Creator Nodes for ComfyUI

Text-based image editing using Black Forest Labs' Flux Kontext API
Compatible with existing BFL config format

Includes:
- FluxKontextCreator: Single image editing
- FluxKontextCreator_Exp: Multi-image reference combination (Experimental)
"""

# Import all node classes and their mappings
try:
    from .flux_kontext_creator import NODE_CLASS_MAPPINGS as CREATOR_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CREATOR_DISPLAY_MAPPINGS
    creator_loaded = True
    print("[FLUX KONTEXT] 🎨 Flux Kontext Creator loaded successfully")
except Exception as e:
    print(f"[FLUX KONTEXT] Warning: Could not load Flux Kontext Creator: {e}")
    creator_loaded = False
    CREATOR_MAPPINGS = {}
    CREATOR_DISPLAY_MAPPINGS = {}

try:
    from .flux_kontext_creator_exp import NODE_CLASS_MAPPINGS as EXP_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as EXP_DISPLAY_MAPPINGS
    exp_loaded = True
    print("[FLUX KONTEXT] 🎨 Flux Kontext Creator Experimental loaded successfully")
except Exception as e:
    print(f"[FLUX KONTEXT] Warning: Could not load Flux Kontext Creator Experimental: {e}")
    exp_loaded = False
    EXP_MAPPINGS = {}
    EXP_DISPLAY_MAPPINGS = {}

# Combine all node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Add loaded nodes
NODE_CLASS_MAPPINGS.update(CREATOR_MAPPINGS)
NODE_CLASS_MAPPINGS.update(EXP_MAPPINGS)

NODE_DISPLAY_NAME_MAPPINGS.update(CREATOR_DISPLAY_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(EXP_DISPLAY_MAPPINGS)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Print loading summary
print("[FLUX KONTEXT] Ready for text-based image editing!")
print("[FLUX KONTEXT] Available nodes:")

if creator_loaded:
    print("[FLUX KONTEXT]   - 🎨 Flux Kontext Creator (single image)")
if exp_loaded:
    print("[FLUX KONTEXT]   - 🎨 Flux Kontext Creator Experimental (multi-reference)")

total_nodes = len(NODE_CLASS_MAPPINGS)
print(f"[FLUX KONTEXT] Total nodes loaded: {total_nodes}")

if total_nodes == 0:
    print("[FLUX KONTEXT] ⚠️ No nodes were loaded successfully!")
    print("[FLUX KONTEXT] Please check your config.ini and file structure.")