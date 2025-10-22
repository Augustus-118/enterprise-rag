import re

class PIIDetector:
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        }
    
    def detect(self, text: str):
        detected = {}
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[pii_type] = matches
        return detected
    
    def redact(self, text: str):
        for pii_type, pattern in self.patterns.items():
            if pii_type == 'email':
                text = re.sub(pattern, '[EMAIL]', text)
            elif pii_type == 'phone':
                text = re.sub(pattern, '[PHONE]', text)
            elif pii_type == 'ssn':
                text = re.sub(pattern, '[SSN]', text)
        return text
