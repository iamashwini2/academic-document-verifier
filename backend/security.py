ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}


def is_allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False

    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
