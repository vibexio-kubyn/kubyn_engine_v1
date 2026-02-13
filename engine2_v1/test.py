from google import genai
 
GEMINI_API_KEY = "AIzaSyC4aBXsFVsNBJ-mGeX1ZSDlB0sZk28Q_e0"
 
client = genai.Client(api_key=GEMINI_API_KEY)
 
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain what is AI simply."
)
print(response.text)