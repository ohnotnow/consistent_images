# Image Style Guide System

Simple Python scripts to generate stylistically consistent images. Uses an LLM to create custom style guides on demand, then combines them with your prompts.

## Setup

```bash
# Install litellm
pip install litellm

# Set your API key (choose one based on your provider)
export OPENAI_API_KEY="your-key"
# or
export ANTHROPIC_API_KEY="your-key"
# or
export GEMINI_API_KEY="your-key"

# Set your replicate API key
export REPLICATE_API_KEY="your-key"
```

## Quick Start

### 1. Create a Style Guide (LLM generates it for you!)

```bash
# For a specific artist
python create_style_guide.py --artist "J. M. W. Turner"

# For an artistic style/movement
python create_style_guide.py --style "Art Nouveau"

# From reference images (analyzes your images to extract the style!)
python create_style_guide.py --images "image1.jpg,image2.png,image3.jpg"

# Use a different model
python create_style_guide.py --artist "Hokusai" --model anthropic/claude-4-5-sonnet
```

The LLM analyzes the artist/style/images and creates a detailed guide covering:
- Core visual characteristics
- Color palettes
- Composition techniques
- Technical approaches
- Mood and atmosphere

**Image-based style guides**: When using `--images`, the script analyzes each image individually using a vision model, then synthesizes a unified style guide from the common patterns across all images. Perfect for when you have reference images but don't know the exact artist or style name!

### 2. Generate Images

```bash
# Use the style guide with your prompt
python generate_image.py --style-guide style-guides/jmw_turner.md futuristic nanobot assembly process

python generate_image.py --style-guide style-guides/art_nouveau.md a high octane car chase

# Generate multiple variations at once
python generate_image.py --style-guide style-guides/jmw_turner.md --number 4 futuristic nanobot assembly process
```

The script combines your prompt with the style guide and outputs an enhanced prompt.


## Requirements

```bash
uv sync
```

## License

MIT
