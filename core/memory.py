"""
Conversation Memory Management
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class ConversationMemory:
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.messages = []
        self.context = {}
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add a message to conversation history"""
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.messages.append(message)
        
        # Keep only last N messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_context(self, num_messages: int = 5) -> str:
        """Get recent conversation as context"""
        recent = self.messages[-num_messages:] if self.messages else []
        
        context_parts = []
        for msg in recent:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def get_full_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.messages
    
    def clear(self):
        """Clear conversation history"""
        self.messages = []
        self.context = {}
    
    def save_to_file(self, filename: str):
        """Save conversation to file"""
        data = {
            'messages': self.messages,
            'context': self.context,
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """Load conversation from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = data.get('messages', [])
                self.context = data.get('context', {})
        except FileNotFoundError:
            print(f"File {filename} not found. Starting fresh conversation.")
