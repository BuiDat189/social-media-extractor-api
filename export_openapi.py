import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

def export():
    openapi_schema = app.openapi()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    print(f"Exported OpenAPI specification successfully to: {output_path}")

if __name__ == "__main__":
    export()
