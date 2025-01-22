import asyncio
import websockets
import json
import ssl
from cryptography.fernet import Fernet  # Fix import

class SecureTransmission:
    def __init__(self, server_url, encryption_key):
        self.server_url = server_url
        self.fernet = Fernet(encryption_key)  # Fix initialization
