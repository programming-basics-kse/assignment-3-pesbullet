def validate_and_convert_int(string: str) -> int | None:
    try:
        return int(string)
    except ValueError:
        return None


def display_error_and_exit(error_value):
    print("[ERROR]: " + error_value)
    exit()


def display_warning(warning_value):
    print("[WARNING]: " + warning_value)


def display_progress(progress_value):
    print("[PROGRESS]: " + progress_value)
