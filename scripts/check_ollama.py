import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.ollama_service import ollama_service

def check_ollama():
    print("=" * 60)
    print(" OLLAMA & LLAMA 3.2 CONNECTIVITY DIAGNOSTIC")
    print("=" * 60)
    health = ollama_service.check_health()
    print(f"Status:            {health['status']}")
    print(f"Base URL:          {health['base_url']}")
    print(f"Configured Model:  {health['configured_model']}")
    print(f"Model Ready:       {health['model_ready']}")
    print(f"Available Models:  {health.get('available_models', [])}")
    print(f"Diagnostic Note:   {health['message']}")
    print("=" * 60)

    if health["model_ready"]:
        print("\nExecuting test inference...")
        try:
            resp = ollama_service.generate_chat([
                {"role": "user", "content": "Say 'Ollama Llama 3.2 is operational.'"}
            ])
            print(f"Response: {resp.strip()}")
        except Exception as e:
            print(f"Inference error: {e}")

if __name__ == "__main__":
    check_ollama()
