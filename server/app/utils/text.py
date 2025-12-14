import re
import unicodedata


def slugify(value: str) -> str:
    """Convert text to a clean slug (lowercase, hyphen-separated)."""
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
