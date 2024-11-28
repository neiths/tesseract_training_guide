import os

def find_invalid_files(directory):
    """
    Find invalid ground-truth file groups in a directory.

    Args:
        directory (str): Path to the directory containing the files.

    Returns:
        list: List of prefixes that are invalid with associated issues.
    """
    invalid_files = []

    # Extract unique prefixes from the file names
    prefixes = set()
    for file_name in os.listdir(directory):
        if file_name.endswith(('.tif', '.box', '.gt.txt')):
            prefixes.add(os.path.splitext(file_name)[0].rsplit('.', 1)[0])

    # Validate each prefix
    for prefix in prefixes:
        required_files = [f"{prefix}.tif", f"{prefix}.box", f"{prefix}.gt.txt"]
        issues = []

        # Check existence of files
        for file_name in required_files:
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_name}")

        # Check if .gt.txt is not blank
        gt_txt_path = os.path.join(directory, f"{prefix}.gt.txt")
        if os.path.exists(gt_txt_path):
            with open(gt_txt_path, 'r', encoding='utf-8') as f:
                if f.read().strip() == "":
                    issues.append(f"{prefix}.gt.txt is blank")

        # If any issues found, add to invalid list
        if issues:
            invalid_files.append({
                "prefix": prefix,
                "issues": issues
            })

    return invalid_files

def remove_invalid_files(directory):
    """
    Identify and remove invalid ground-truth file groups in a directory.

    Args:
        directory (str): Path to the directory containing the files.

    Returns:
        list: List of prefixes that were removed.
    """
    invalid_files = []

    # Extract unique prefixes from the file names
    prefixes = set()
    for file_name in os.listdir(directory):
        if file_name.endswith(('.tif', '.box', '.gt.txt')):
            prefixes.add(os.path.splitext(file_name)[0].rsplit('.', 1)[0])

    # Validate each prefix
    for prefix in prefixes:
        required_files = [f"{prefix}.tif", f"{prefix}.box", f"{prefix}.gt.txt"]
        issues = []

        # Check existence of files
        for file_name in required_files:
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(file_path):
                issues.append(f"Missing file: {file_name}")

        # Check if .gt.txt is not blank
        gt_txt_path = os.path.join(directory, f"{prefix}.gt.txt")
        if os.path.exists(gt_txt_path):
            with open(gt_txt_path, 'r', encoding='utf-8') as f:
                if f.read().strip() == "":
                    issues.append(f"{prefix}.gt.txt is blank")

        # If any issues found, add to invalid list
        if issues:
            invalid_files.append({
                "prefix": prefix,
                "issues": issues
            })

    # Remove invalid files
    removed_prefixes = []
    for invalid in invalid_files:
        prefix = invalid['prefix']
        print(f"Removing files for prefix: {prefix}")
        for ext in ['tif', 'box', 'gt.txt']:
            file_path = os.path.join(directory, f"{prefix}.{ext}")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        removed_prefixes.append(prefix)

    return removed_prefixes


# Example usage
directory = "tesstrain/data/vietnamese-ocr-model-ground-truth"
invalid_files = find_invalid_files(directory)

len_invalid_files = 0

if invalid_files:
    print("Invalid file groups found:")
    for file in invalid_files:
        print(f"Prefix: {file['prefix']}")
        len_invalid_files += 1
        for issue in file['issues']:
            print(f"  - {issue}")
    print(f"Total invalid file groups: {len_invalid_files}")
else:
    print("All file groups are valid.")
    
# Example usage
directory = "tesstrain/data/vietnamese-ocr-model-ground-truth"
removed_prefixes = remove_invalid_files(directory)

if removed_prefixes:
    print("Removed the following invalid file groups:")
    for prefix in removed_prefixes:
        print(f"  - {prefix}")
else:
    print("No invalid file groups found to remove.")


