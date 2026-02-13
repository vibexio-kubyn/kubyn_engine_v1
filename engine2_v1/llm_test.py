from google import genai

# Put your real key here temporarily for testing
GEMINI_API_KEY = "AIzaSyC4aBXsFVsNBJ-mGeX1ZSDlB0sZk28Q_e0"

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Explain how AI works in a few words."
)

print(response.text)
