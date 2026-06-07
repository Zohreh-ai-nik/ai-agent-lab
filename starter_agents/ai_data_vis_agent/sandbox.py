# sandbox.py
# PURPOSE: All E2B sandbox interactions in one place
import base64
from typing import Optional, List, Any
from PIL import Image
from io import BytesIO
from e2b_code_interpreter import Sandbox


def create_sandbox(e2b_api_key: str) -> Sandbox:
    """Creates and returns an E2B sandbox instance."""
    return Sandbox(api_key=e2b_api_key)


def upload_dataset(sandbox: Sandbox, uploaded_file) -> str:
    """
    Uploads a CSV file into the E2B sandbox.
    Returns the path where the file lives inside the sandbox.
    """
    dataset_path = f"./{uploaded_file.name}"
    try:
        sandbox.files.write(dataset_path, uploaded_file)
        print(f"✅ Dataset uploaded to sandbox at: {dataset_path}")
        return dataset_path
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise e


def run_code(sandbox: Sandbox, code: str) -> Optional[List[Any]]:
    """
    Runs Python code inside the E2B sandbox.
    Returns list of results or None if error.
    """
    execution = sandbox.run_code(code)

    if execution.error:
        print(f"❌ Sandbox error: {execution.error}")
        return None

    print(f"✅ Code executed successfully")
    return execution.results


def extract_image(result) -> Optional[Image.Image]:
    """
    Converts a sandbox result into a PIL Image if it contains PNG data.
    Returns None if result is not an image.
    """
    if hasattr(result, 'png') and result.png:
        png_data = base64.b64decode(result.png)
        return Image.open(BytesIO(png_data))
    return None