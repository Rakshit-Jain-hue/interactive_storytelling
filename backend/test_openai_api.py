import openai

# Replace with your actual API key
openai.api_key = "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"

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ]
        )
        print("API Key is valid.")
        print("Response:", response['choices'][0]['message']['content'])
    except openai.error.InvalidRequestError as e:
        print("Invalid request error:", e)
    except openai.error.AuthenticationError as e:
        print("Invalid API Key. Please check your API key and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_openai_api()
