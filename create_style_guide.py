#!/usr/bin/env python3
"""
Create a style guide for consistent image generation using an LLM.
Usage: 
    python create_style_guide.py --artist "J. M. W. Turner"
    python create_style_guide.py --style "Art Nouveau"
    
Set your LLM API key as an environment variable:
    export OPENAI_API_KEY="your-key"  # or ANTHROPIC_API_KEY, etc.
"""

import argparse
import os
from pathlib import Path
from litellm import completion

# Example style guide to use as a template
EXAMPLE_STYLE_GUIDE = """# J. M. W. Turner Style Guide

## Core Characteristics
- Dramatic use of light and atmospheric effects
- Luminous, almost ethereal quality to scenes
- Bold, expressive brushwork with visible texture
- Emphasis on the sublime and romantic
- Rich golden yellows, deep blues, and warm oranges

## Color Palette
- Dominant warm golds and yellows (especially in skies)
- Deep blues and turquoise for water and atmosphere
- Burnt sienna, ochre, and raw umber for earth tones
- Dramatic contrasts between light and shadow
- Haziness and atmospheric perspective

## Composition
- Often dramatic diagonal compositions
- Swirling, dynamic movement
- Light as the central focus
- Blurred boundaries between elements
- Sense of vast space and atmosphere

## Technique
- Loose, expressive brushwork
- Layered glazes creating luminosity
- Impasto in highlights
- Deliberately indistinct forms dissolving into light
- Painterly and atmospheric rather than detailed

## Mood
- Sublime and awe-inspiring
- Romantic and emotional
- Sense of nature's power
- Contemplative and atmospheric
- Often melancholic or nostalgic

## Application Note
Apply these characteristics while maintaining the core subject matter of the prompt.
The Turner style should enhance, not overwhelm, the specific content requested.
"""

def generate_style_guide_with_llm(name, is_artist=True, model="openai/gpt-5-mini"):
    """Use an LLM to generate a detailed style guide."""
    
    type_str = "artist" if is_artist else "artistic style or movement"
    
    prompt = f"""You are an expert art historian and visual style analyst. Create a detailed style guide for image generation that captures the distinctive characteristics of {name} ({type_str}).

Your style guide should follow this exact format and level of detail:

{EXAMPLE_STYLE_GUIDE}

Create a comprehensive style guide for {name} that includes:
1. Core Characteristics - the most distinctive visual elements
2. Color Palette - specific colors and color relationships
3. Composition - how space and elements are arranged
4. Technique - brushwork, mark-making, or technical approach
5. Mood - the emotional and atmospheric qualities
6. Application Note - guidance on how to apply the style while keeping subject matter clear

Be specific and detailed. Focus on visual characteristics that an image generation AI can understand and reproduce. The guide will be used to create multiple images that should all share these consistent stylistic elements.

Return ONLY the markdown-formatted style guide, starting with the title.
"""

    print(f"🤖 Asking LLM to generate style guide for {name}...")
    
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        guide_content = response.choices[0].message.content
        return guide_content
        
    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        print("\nMake sure you have:")
        print("1. Installed litellm: pip install litellm")
        print("2. Set your API key (e.g., export OPENAI_API_KEY='your-key')")
        print("3. Have access to the specified model")
        return None

def create_style_guide(name, is_artist=True, model="gpt-4o-mini"):
    """Generate a detailed style guide based on artist or style."""
    
    # Create style-guides directory if it doesn't exist
    Path("style-guides").mkdir(exist_ok=True)
    
    # Create filename-safe name
    filename = name.lower().replace(" ", "_").replace(".", "").replace("-", "_")
    filepath = f"style-guides/{filename}.md"
    
    # Generate the style guide content using LLM
    guide = generate_style_guide_with_llm(name, is_artist, model)
    
    if guide is None:
        return None
    
    # Write to file
    with open(filepath, 'w') as f:
        f.write(guide)
    
    print(f"✓ Style guide created: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(
        description='Create a style guide using an LLM',
        epilog='Set your API key as environment variable (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--artist', help='Artist name (e.g., "J. M. W. Turner")')
    group.add_argument('--style', help='Style or movement (e.g., "Art Nouveau")')
    
    parser.add_argument(
        '--model',
        default='gpt-4o-mini',
        help='LLM model to use (default: gpt-4o-mini). Examples: gpt-4o, claude-3-5-sonnet-20241022, gemini-pro'
    )
    
    args = parser.parse_args()
    
    if args.artist:
        create_style_guide(args.artist, is_artist=True, model=args.model)
    else:
        create_style_guide(args.style, is_artist=False, model=args.model)

if __name__ == "__main__":
    main()
