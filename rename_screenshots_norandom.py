import ctypes
import os
import sys
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif", ".jfif", ".heic", ".avif"}

SELF_NAME = os.path.basename(sys.argv[0]).lower()


def show_message(text):
    if getattr(sys, "frozen", False):
        ctypes.windll.user32.MessageBoxW(0, text, "自动重命名(无随机数)", 0x10)
    else:
        print(text)


def get_exif_time(path):
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            for tag_id, value in exif.items():
                if TAGS.get(tag_id) == "DateTimeOriginal" and value:
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None


def get_photo_time(path):
    exif_time = get_exif_time(path)
    if exif_time:
        return exif_time
    return datetime.fromtimestamp(os.path.getmtime(path))


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if not os.path.isdir(directory):
        show_message(f"目录不存在: {directory}")
        sys.exit(1)

    entries = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    targets = []
    for name in entries:
        if name.lower() == SELF_NAME:
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            targets.append(name)

    if not targets:
        return

    used = set(os.listdir(directory))
    renamed_count = 0

    for name in targets:
        old_path = os.path.join(directory, name)
        ext = os.path.splitext(name)[1].lower()

        photo_time = get_photo_time(old_path)
        stamp = photo_time.strftime("%Y-%m-%d_%H%M%S")
        new_name = f"Screenshot_{stamp}{ext}"

        if new_name in used:
            index = 2
            while f"Screenshot_{stamp}_{index}{ext}" in used:
                index += 1
            new_name = f"Screenshot_{stamp}_{index}{ext}"
        used.add(new_name)

        new_path = os.path.join(directory, new_name)
        try:
            os.rename(old_path, new_path)
        except OSError as e:
            show_message(f"重命名失败: {name}\n{e}")
            sys.exit(1)
        renamed_count += 1


if __name__ == "__main__":
    main()
