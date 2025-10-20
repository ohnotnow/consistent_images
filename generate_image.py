#!/usr/bin/env python3
"""
Generate images using a style guide combined with your prompt.
Usage: 
    python generate_image.py --style-guide style-guides/jmw_turner.md generate a futuristic nanobot
    python generate_image.py --style-guide style-guides/art_nouveau.md microscopic view of cells
"""

import argparse
import sys
from pathlib import Path
from litellm import completion
import replicate
import requests

def load_style_guide(filepath):
    """Load the style guide content from file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Style guide not found: {filepath}")
        print("Create one first using: python create_style_guide.py --artist 'Artist Name'")
        sys.exit(1)

def create_enhanced_prompt(style_guide, user_prompt, model="openai/gpt-5-mini"):
    """Combine style guide with user's specific prompt."""
    
    # Extract just the key points from the style guide for the prompt
    # (Most image models work better with focused prompts)
    
    llm_prompt = f"""You are an expert at writing concise prompts for image generation AI models.

Given this style guide:
{style_guide}

And this subject to depict:
{user_prompt}

Create a single, concise image generation prompt (2-4 sentences maximum) that:
1. Describes the subject clearly
2. Incorporates the key style characteristics (colors, composition, technique, mood)
3. Is optimized for image generation models (Stable Diffusion, DALL-E, Flux, etc.)

DO NOT write explanations, sections, or art direction documents.
DO NOT use headers, bullet points, or markdown formatting.
ONLY output the final prompt text that will be sent directly to the image model.

Example format:
"[Subject description] in the style of [artist/movement]. [Key visual characteristics: colors, technique]. [Composition and mood details]. [Technical quality specifications]."

Now write the prompt:"""


    response = completion(
        model=model,
        messages=[{"role": "user", "content": llm_prompt}],
    )
        
    enhanced_prompt = response.choices[0].message.content
    return enhanced_prompt

def make_safe_filename(prompt, max_length=50):
    """Convert a prompt into a filesystem-safe filename."""
    # Lowercase and strip whitespace
    safe = prompt.lower().strip()
    
    # Replace any non-alphanumeric characters with underscore
    safe = re.sub(r'[^a-z0-9]+', '_', safe)
    
    # Remove leading/trailing underscores
    safe = safe.strip('_')
    
    # Truncate to max length
    if len(safe) > max_length:
        safe = safe[:max_length].rstrip('_')
    
    return safe

def generate_image(style_guide_path, prompt):
    """Generate an image using the style guide and prompt."""
    
    # Load the style guide
    style_guide = load_style_guide(style_guide_path)
    
    # Create the enhanced prompt
    enhanced_prompt = create_enhanced_prompt(style_guide, prompt)
    
    # Display what we're sending
    print("=" * 70)
    print("ENHANCED PROMPT")
    print("=" * 70)
    print(enhanced_prompt)
    print("=" * 70)
    print()
    
    input = {
        "prompt": enhanced_prompt,
    }

    output = replicate.run(
        "google/nano-banana",
        input=input
    )

    if isinstance(output, list):
        image_url = output[0]
    else:
        image_url = output

    print(f"Image URL: {image_url}")
    image_content = requests.get(image_url).content
    filename = make_safe_filename(prompt)
    with open(filename, "wb") as f:
        f.write(image_content)
    return filename

def main():
    parser = argparse.ArgumentParser(
        description='Generate images with consistent style using style guides',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--style-guide',
        required=True,
        help='Path to style guide file (e.g., style-guides/jmw_turner.md)'
    )
    
    parser.add_argument(
        'prompt',
        nargs='+',
        help='Your image prompt (what you want to generate)'
    )
    
    args = parser.parse_args()
    
    # Join the prompt words
    user_prompt = ' '.join(args.prompt)
    
    # Generate the enhanced prompt
    filename = generate_image(args.style_guide, user_prompt)
    print(f"Image generated: {filename}")

if __name__ == "__main__":
    main()
