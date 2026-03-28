"""
Test suite for AI Companion chatbot
Run with: python test_ai_companion.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health_check():
    """Test if the API is running"""
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API at", BASE_URL)
        print("Make sure to run: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_chat():
    """Test sending a message"""
    print_section("TEST 2: Simple Chat")
    try:
        payload = {
            "user_input": "Hello, how are you?"
        }
        response = requests.post(f"{BASE_URL}/chat/", params=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working!")
            print(f"User Input: {data.get('user_input')}")
            print(f"Bot Response: {data.get('bot_response')}")
            print(f"Conversation ID: {data.get('conversation_id')}")
            return data.get('conversation_id')
        else:
            print(f"❌ Chat endpoint returned: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_multiple_messages():
    """Test multiple messages"""
    print_section("TEST 3: Multiple Messages")
    messages = [
        "What is Python?",
        "Tell me a joke",
        "How do I learn programming?"
    ]
    
    try:
        for msg in messages:
            payload = {"user_input": msg}
            response = requests.post(f"{BASE_URL}/chat/", params=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"📤 Sent: {msg}")
                print(f"📥 Received: {data.get('bot_response')}")
                print()
            else:
                print(f"❌ Failed to send: {msg}")
                return False
        
        print("✅ All messages sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_conversation_history():
    """Test retrieving conversation history"""
    print_section("TEST 4: Conversation History")
    try:
        payload = {"user_input": "Test message for history"}
        response = requests.post(f"{BASE_URL}/chat/", params=payload, timeout=10)
        
        if response.status_code == 200:
            conv_id = response.json().get('conversation_id')
            response = requests.get(f"{BASE_URL}/conversations/{conv_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Retrieved conversation!")
                print(f"ID: {data.get('id')}")
                print(f"User Input: {data.get('user_input')}")
                print(f"Bot Response: {data.get('bot_response')}")
                return True
            else:
                print(f"❌ Failed to retrieve: {response.status_code}")
                return False
        else:
            print(f"❌ Failed to create: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_database():
    """Test database storage"""
    print_section("TEST 5: Database Storage")
    try:
        payload = {"user_input": "Testing database storage"}
        response = requests.post(f"{BASE_URL}/chat/", params=payload, timeout=10)
        
        if response.status_code == 200:
            conv_id = response.json().get('conversation_id')
            
            for i in range(3):
                response = requests.get(f"{BASE_URL}/conversations/{conv_id}", timeout=10)
                if response.status_code != 200:
                    print(f"❌ Database retrieval failed on attempt {i+1}")
                    return False
            
            print("✅ Database storage working!")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + "  🤖 AI COMPANION TEST SUITE".center(60) + "║")
    print("╚" + "="*58 + "╝\n")
    
    results = {
        "Health Check": test_health_check(),
        "Simple Chat": test_simple_chat() is not None,
        "Multiple Messages": test_multiple_messages(),
        "Conversation History": test_conversation_history(),
        "Database Storage": test_database(),
    }
    
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed\n")
    
    if passed == total:
        print("🎉 All tests passed! Your AI Companion is ready!\n")
    elif passed == 0:
        print("⚠️  API is not running. Start it with: python main.py\n")
    else:
        print(f"⚠️  {total - passed} test(s) failed.\n")

if __name__ == "__main__":
    run_all_tests()
