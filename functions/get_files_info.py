import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        is_valid = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
            
        results = []
        for filename in os.listdir(target_dir):
            full_path = os.path.join(target_dir, filename)
            file_size = os.path.getsize(full_path)
            dir_status = os.path.isdir(full_path)
            results.append(f"- {filename}: file_size={file_size} bytes, is_dir={dir_status}")
        return "\n".join(results)

    except Exception as e:
        return f'Error: {e}'