"""Quick test for Gemini API key."""
import asyncio
import os
from dotenv import load_dotenv

async def test_gemini():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return
    
    if not api_key.startswith("AIza"):
        print("❌ Invalid API key format. Should start with 'AIza'")
        print(f"   Your key starts with: {api_key[:10]}...")
        return
    
    print(f"✓ API key format looks correct")
    print(f"  Key: {api_key[:15]}...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            google_api_key=api_key
        )
        
        response = await llm.ainvoke("Say hello")
        print(f"✓ Gemini API working!")
        print(f"  Response: {response.content[:100]}...")
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        print("\n💡 Get a new API key from: https://aistudio.google.com/app/apikey")

if __name__ == "__main__":
    asyncio.run(test_gemini())

