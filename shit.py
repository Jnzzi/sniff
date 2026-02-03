import os
from PIL import Image, ImageSequence

TARGET_KB = 500
MIN_QUALITY = 70
START_QUALITY = 90
METHOD = 6
RESIZE_STEP = 0.9
MIN_SCALE = 0.6

def gif_to_webp_smart(path):
    original_kb = os.path.getsize(path) / 1024
    webp_path = path[:-4] + ".webp"

    with Image.open(path) as img:
        frames = [f.convert("RGBA") for f in ImageSequence.Iterator(img)]
        w, h = frames[0].size
        scale = 1.0
        quality = START_QUALITY

        while True:
            resized_frames = [
                f.resize(
                    (int(w * scale), int(h * scale)),
                    Image.LANCZOS
                )
                for f in frames
            ]

            resized_frames[0].save(
                webp_path,
                format="WEBP",
                save_all=True,
                append_images=resized_frames[1:],
                quality=quality,
                method=METHOD,
                duration=img.info.get("duration", 40),
                loop=img.info.get("loop", 0)
            )

            size_kb = os.path.getsize(webp_path) / 1024
            print(f"{path}: {size_kb:.1f} KB (q={quality}, scale={scale:.2f})")

            if size_kb <= TARGET_KB:
                break

            if quality > MIN_QUALITY:
                quality -= 5
            elif scale > MIN_SCALE:
                scale *= RESIZE_STEP
                quality = START_QUALITY
            else:
                break

    if os.path.exists(webp_path) and os.path.getsize(webp_path) < os.path.getsize(path):
        os.remove(path)
        print(f"✔ Replaced {path}")
    else:
        os.remove(webp_path)
        print(f"✖ Kept original GIF (smaller)")

def main():
    for file in os.listdir("."):
        if file.lower().endswith(".gif"):
            gif_to_webp_smart(file)

if __name__ == "__main__":
    main()
