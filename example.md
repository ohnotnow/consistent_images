   import openai
    import base64
    client = openai.OpenAI( api_key=os.getenv("OPENAI_API_KEY"))
    THIS_MODEL = "gpt-4o-mini"
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    # Getting the base64 string
    base64_image = encode_image(image_path)
    
    # Send the request to the API
    response = client.chat.completions.create(
            model=THIS_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": [
                        {"type": "text",
                        "text": "You are a cool image analyst.  Your goal is to describe what is in the image provided as a file."
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type":"text",
                            "text": "What is in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                                {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
    print(f"response: {response}")
    # Extract the description
    description = response.choices[0].message.content
    print(f"Desription: {description}")

