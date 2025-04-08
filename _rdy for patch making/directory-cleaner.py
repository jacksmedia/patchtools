from pathlib import Path # for dir reference
import shutil

def clean(script_dir):
    ## Delete all sfc and zip files
    for ext in ('*.sfc', '*.zip'):
        for file_path in script_dir.glob(ext):
            try:
                file_path.unlink()
                print(f"Deleted {file_path.name}")
            except Exception as e:
                print(f"Failed to delete {file_path.name}: {e}")

    ## Delete all subfolders & contents
    for item in script_dir.iterdir():
        if item.is_dir():
            try:
                shutil.rmtree(item)
                print(f"Deleted dir: {item.name}")
            except Exception as e:
                print(f"Failed to delete dir {item.name}: {e}")

# Example usage
script_dir = Path(__file__).parent # this dir

# Process invocation
clean(script_dir)