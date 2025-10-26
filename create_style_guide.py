#!/usr/bin/env python3
"""
Create a style guide for consistent image generation using an LLM.
Usage:
    python create_style_guide.py --artist "J. M. W. Turner"
    python create_style_guide.py --style "Art Nouveau"
    python create_style_guide.py --images "image1.jpg,image2.png,image3.jpg"

Set your LLM API key as an environment variable:
    export OPENAI_API_KEY="your-key"  # or ANTHROPIC_API_KEY, etc.
"""

import argparse
import base64
import os
from datetime import datetime
from pathlib import Path
from litellm import completion

def encode_image(image_path):
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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

def generate_style_guide_with_llm(name, is_artist=True, model="gpt-4o-mini"):
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

def analyze_image_with_llm(image_path, model="gpt-4o-mini"):
    """Analyze a single image to extract visual style characteristics."""

    print(f"🔍 Analyzing image: {image_path}")

    try:
        # Encode the image
        base64_image = encode_image(image_path)

        # Determine image format from file extension
        image_format = Path(image_path).suffix.lstrip('.').lower()
        if image_format == 'jpg':
            image_format = 'jpeg'

        prompt = """Analyze this image and describe its visual style characteristics in detail.
Focus on the following categories:

1. **Core Characteristics**: The most distinctive visual elements
2. **Color Palette**: Specific colors, color relationships, and overall color mood
3. **Composition**: How space and elements are arranged, perspective, balance
4. **Technique**: Brushwork, mark-making, texture, or technical approach visible
5. **Mood**: The emotional and atmospheric qualities
6. **Subject Matter**: What is depicted in the image

Be specific and detailed. Focus on visual characteristics that could be used to recreate a similar style.
Format your response with clear headings for each category."""

        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            temperature=0.7
        )

        analysis = response.choices[0].message.content
        print(f"✓ Analysis complete for {image_path}")
        return analysis

    except Exception as e:
        print(f"❌ Error analyzing image {image_path}: {e}")
        return None

def synthesize_style_guide_from_images(analyses, model="gpt-4o-mini"):
    """Synthesize multiple image analyses into a unified style guide."""

    print(f"🎨 Synthesizing style guide from {len(analyses)} image analyses...")

    # Combine all analyses
    combined_analyses = "\n\n---\n\n".join([f"## Image {i+1} Analysis\n{analysis}"
                                             for i, analysis in enumerate(analyses)])

    prompt = f"""You are an expert art historian and visual style analyst. You have been provided with detailed analyses of {len(analyses)} images. Your task is to identify the common visual patterns and characteristics across all these images and create a unified style guide.

Here are the individual image analyses:

{combined_analyses}

---

Based on these analyses, create a comprehensive style guide that captures the CONSISTENT elements across all images. Follow this exact format:

{EXAMPLE_STYLE_GUIDE}

Your style guide should:
1. Identify patterns that appear across MULTIPLE images (not just one)
2. Focus on visual characteristics that can be reproduced
3. Note any variations or range within the style
4. Be specific about colors, composition, technique, and mood
5. Include an "Application Note" section explaining how to apply the style while maintaining subject matter

Return ONLY the markdown-formatted style guide, starting with a descriptive title based on the common characteristics you've identified."""

    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        guide_content = response.choices[0].message.content
        print("✓ Style guide synthesis complete")
        return guide_content

    except Exception as e:
        print(f"❌ Error synthesizing style guide: {e}")
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
    group.add_argument('--images', help='Comma-separated list of image paths to analyze (e.g., "img1.png,img2.jpg")')
    
    parser.add_argument(
        '--model',
        default='gpt-4o-mini',
        help='LLM model to use (default: gpt-4o-mini). Examples: gpt-4o, claude-3-5-sonnet-20241022, gemini-pro'
    )
    
    args = parser.parse_args()

    if args.images:
        # Handle image-based style guide generation
        image_paths = [path.strip() for path in args.images.split(',')]

        print(f"📸 Processing {len(image_paths)} images...")

        # Analyze each image
        analyses = []
        for image_path in image_paths:
            # Check if file exists
            if not Path(image_path).exists():
                print(f"❌ Error: Image file not found: {image_path}")
                return

            analysis = analyze_image_with_llm(image_path, model=args.model)
            if analysis is None:
                print(f"❌ Failed to analyze {image_path}. Aborting.")
                return
            analyses.append(analysis)

        # Synthesize the style guide
        guide = synthesize_style_guide_from_images(analyses, model=args.model)
        if guide is None:
            print("❌ Failed to synthesize style guide. Aborting.")
            return

        # Create style-guides directory if it doesn't exist
        Path("style-guides").mkdir(exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"style-guides/images-{timestamp}.md"

        # Write to file
        with open(filepath, 'w') as f:
            f.write(guide)

        print(f"✓ Style guide created: {filepath}")

    elif args.artist:
        create_style_guide(args.artist, is_artist=True, model=args.model)
    else:
        create_style_guide(args.style, is_artist=False, model=args.model)

if __name__ == "__main__":
    main()
