#!/usr/bin/env python3
"""Groq LLM Client for TaniBot"""

import requests
import json
from typing import Optional, List, Dict

class GroqClient:
    """Groq API client for LLM inference"""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: List[Dict], max_tokens: int = 500, 
             temperature: float = 0.7) -> Dict:
        """Send chat completion request"""
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=data, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "content": result['choices'][0]['message']['content'],
                    "usage": result['usage'],
                    "model": result['model']
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def ask(self, question: str, system_prompt: str = None) -> Dict:
        """Simple question-answer interface"""
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": question})
        
        return self.chat(messages)


# TaniBot-specific client
class TaniBotLLM(GroqClient):
    """TaniBot LLM with agricultural context"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, model="llama-3.1-8b-instant")
        self.system_prompt = """You are TaniBot, an AI agricultural assistant for Indonesia.

Your role:
- Help farmers with crop recommendations
- Provide weather-based insights
- Answer questions about Indonesian agriculture
- Give yield predictions and planting advice
- Speak in friendly, accessible Indonesian or English

Always be helpful, accurate, and culturally appropriate."""
    
    def ask_agriculture(self, question: str) -> Dict:
        """Ask agriculture-related question"""
        return self.ask(question, self.system_prompt)
    
    def get_crop_advice(self, crop: str, location: str) -> Dict:
        """Get crop-specific advice for a location"""
        question = f"What are the best practices for growing {crop} in {location}? Include planting season, water needs, and common pests."
        return self.ask_agriculture(question)
    
    def get_weather_recommendation(self, weather_data: Dict, location: str) -> Dict:
        """Get farming recommendations based on weather"""
        question = f"Based on this weather in {location}: {weather_data}, what farming activities do you recommend this week?"
        return self.ask_agriculture(question)


# Test
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/mnt/data/openclaw/workspace/.openclaw/workspace')
    
    # Load API key from environment or secrets
    import os
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    if not GROQ_API_KEY:
        print("⚠️ GROQ_API_KEY not set. Set environment variable or use secrets.")
        exit(1)
    
    print("=" * 60)
    print("🌾 TANI BOT - GROQ LLM TEST")
    print("=" * 60)
    
    bot = TaniBotLLM(GROQ_API_KEY)
    
    # Test 1: General agriculture question
    print("\n1. Testing general agriculture question...")
    result = bot.ask_agriculture("What crops grow well in Java during rainy season?")
    
    if result.get('success'):
        print(f"   ✅ Response received ({len(result['content'])} chars)")
        print(f"   Usage: {result['usage']['total_tokens']} tokens")
        print(f"\n   Preview: {result['content'][:200]}...")
    else:
        print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    
    # Test 2: Crop-specific advice
    print("\n2. Testing crop-specific advice...")
    result = bot.get_crop_advice("Rice (Padi)", "West Java")
    
    if result.get('success'):
        print(f"   ✅ Response received ({len(result['content'])} chars)")
        print(f"   Usage: {result['usage']['total_tokens']} tokens")
    else:
        print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Groq LLM integration test complete!")
