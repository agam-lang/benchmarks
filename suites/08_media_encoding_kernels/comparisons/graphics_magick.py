def graphics_magick_pipeline(pixels, width, height):
    accumulator = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            center = pixels[y * width + x]
            top = pixels[(y - 1) * width + x]
            bottom = pixels[(y + 1) * width + x]
            left = pixels[y * width + (x - 1)]
            right = pixels[y * width + (x + 1)]

            sharpened = center * 5 - top - bottom - left - right
            noise = ((x * 13 + y * 37) % 31) - 15
            filtered = (sharpened + noise) % 256

            accumulator += abs(filtered)
    return accumulator

def main():
    width = 256
    height = 256
    pixels = []
    for i in range(width * height):
        val = ((i * 1103515245 + 12345) // 65536) % 256
        pixels.append(val)

    result = graphics_magick_pipeline(pixels, width, height)
    print(result)

if __name__ == "__main__":
    main()
