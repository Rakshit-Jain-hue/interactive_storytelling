from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import os

# openai.api_key = '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'  # Replace with your actual API key

app = Flask(__name__)
CORS(app)

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

def generate_story(text):
    try:
        messages = [
            {"role": "system", "content": "You are a creative storyteller"},
            {"role": "user", "content": f"Create a story from the following input: {text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500  # Increased token limit for longer descriptions
        )
        story = response.choices[0].message.content
        return story
    except Exception as e:
        print(f"Error generating story: {e}")
        return "Error generating story."

def description_text(text):
    try:
        prompt = f"Describe the following text in about 30 words.\n{text}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful descriptor for image generation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error describing text: {e}")
        return "Error describing text."

def generate_image(summary, style):
    try:
        prompt = f"{summary} in {style} style"
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return "Error generating image."

@app.route('/generate-story', methods=['POST'])
def generate_story_endpoint():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        story = generate_story(prompt)  # Use default style for story
        return jsonify({'story': story})
    except Exception as e:
        print(f"Error in generate-story endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-image', methods=['POST'])
def generate_image_endpoint():
    try:
        data = request.get_json()
        story = data.get('story')
        style = data.get('style', 'realistic')  # Default to 'realistic' if no style is provided
        description = description_text(story)
        image_url = generate_image(description, style)
        return jsonify({'image_url': image_url})
    except Exception as e:
        print(f"Error in generate-image endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
