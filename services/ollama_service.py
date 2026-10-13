"""
Ollama Service for local LLM inference, health diagnostics, and structured JSON generation.
"""

import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from config import settings
from utils.logging_config import logger
from utils.error_handlers import OllamaConnectionError

class OllamaService:
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.timeout = settings.ollama_timeout_seconds

    def check_health(self) -> Dict[str, Any]:
        """
        Verify Ollama server connectivity and model availability.
        Does not automatically download missing models.
        """
        endpoint = f"{self.base_url}/api/tags"
        try:
            req = urllib.request.Request(endpoint, headers={"User-Agent": "GenAI-Studio/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    models = [m.get("name") for m in data.get("models", [])]
                    # Check if requested model or model:latest matches
                    model_found = any(
                        self.model == m or self.model.split(":")[0] == m.split(":")[0]
                        for m in models
                    )
                    return {
                        "is_connected": True,
                        "status": "Connected",
                        "base_url": self.base_url,
                        "configured_model": self.model,
                        "available_models": models,
                        "model_ready": model_found,
                        "message": (
                            f"Ollama running. Model '{self.model}' is available."
                            if model_found
                            else f"Ollama running, but '{self.model}' is missing. Installed: {models}. Run: `ollama run {self.model}`"
                        )
                    }
        except urllib.error.URLError as e:
            logger.warning(f"Ollama health check failed: {e}")
            return {
                "is_connected": False,
                "status": "Disconnected",
                "base_url": self.base_url,
                "configured_model": self.model,
                "available_models": [],
                "model_ready": False,
                "message": f"Cannot connect to Ollama at {self.base_url}. Ensure Ollama is running (`ollama serve`). Details: {e}"
            }
        except Exception as e:
            return {
                "is_connected": False,
                "status": "Error",
                "base_url": self.base_url,
                "configured_model": self.model,
                "available_models": [],
                "model_ready": False,
                "message": f"Unexpected error connecting to Ollama: {e}"
            }

    def generate_chat(
        self,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        temperature: float = 0.2
    ) -> str:
        """
        Send a chat completion request to Ollama /api/chat.
        """
        endpoint = f"{self.base_url}/api/chat"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        if json_mode:
            payload["format"] = "json"

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json", "User-Agent": "GenAI-Studio/1.0"}
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                content = res_data.get("message", {}).get("content", "")
                return content
        except urllib.error.URLError as e:
            raise OllamaConnectionError(
                f"Failed to communicate with Ollama ({self.base_url})",
                details=str(e)
            )
        except TimeoutError:
            raise OllamaConnectionError(
                f"Ollama request timed out after {self.timeout}s",
                details="Model inference exceeded timeout. Try reducing input length or extending timeout."
            )

    def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        retries: int = 2
    ) -> Dict[str, Any]:
        """
        Generate and validate structured JSON output with bounded repair.
        """
        messages = [
            {"role": "system", "content": f"{system_prompt}\nIMPORTANT: You must respond ONLY with a single valid JSON object. No explanation, no markdown backticks, no comments."},
            {"role": "user", "content": user_prompt}
        ]

        last_error = ""
        for attempt in range(retries + 1):
            try:
                raw_response = self.generate_chat(messages, json_mode=True, temperature=0.1)
                parsed = self._repair_and_parse_json(raw_response)
                if parsed is not None:
                    return parsed
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Ollama JSON attempt {attempt + 1} failed: {e}")

        # If LLM failed, return structured error fallback
        return {
            "error": "Failed to parse structured JSON from model",
            "details": last_error,
            "fallback": True
        }

    def _repair_and_parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Clean markdown markers, extract outermost JSON object or array, and parse."""
        cleaned = text.strip()
        # Remove ```json and ``` if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        # Try direct parse
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Search for first { and last }
        match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Search for first [ and last ]
        match_arr = re.search(r"(\[.*\])", cleaned, re.DOTALL)
        if match_arr:
            try:
                return {"items": json.loads(match_arr.group(1))}
            except json.JSONDecodeError:
                pass

        return None

ollama_service = OllamaService()
