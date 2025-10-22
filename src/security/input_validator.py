import re

class InputValidator:
    def __init__(self, max_length=500):
        self.max_length = max_length
        self.blocked_patterns = [
            r'ignore\s+(previous|above|prior)\s+instructions',
            r'system:',
            r'<script>',
            r'DROP\s+TABLE',
            r'DELETE\s+FROM',
        ]
    
    def validate(self, text: str):
        if len(text) > self.max_length:
            return False, f"Query too long (max {self.max_length} chars)"
        
        if not text.strip():
            return False, "Query cannot be empty"
        
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "Suspicious pattern detected"
        
        return True, "Valid"
    
    def sanitize(self, text: str):
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        return text.strip()
