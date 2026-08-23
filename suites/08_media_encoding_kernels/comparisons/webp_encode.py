def predict_spatial_residual(pixels, width, height, quality):
    total_residual = 0
    for y in range(1, height):
        for x in range(1, width):
            curr = pixels[y * width + x]
            top = pixels[(y - 1) * width + x]
            left = pixels[y * width + (x - 1)]
            top_left = pixels[(y - 1) * width + (x - 1)]

            p = left + top - top_left
            pa = abs(p - left)
            pb = abs(p - top)
            pc = abs(p - top_left)

            if pa <= pb and pa <= pc:
                pred = left
            elif pb <= pc:
                pred = top
            else:
                pred = top_left

            residual = (curr - pred) * quality // 100
            total_residual += abs(residual)
    return total_residual

def main():
    width = 256
    height = 256
    pixels = []
    for i in range(width * height):
        val = ((i * 1103515245 + 12345) // 65536) % 256
        pixels.append(val)

    res = predict_spatial_residual(pixels, width, height, 100)
    print(res)

if __name__ == "__main__":
    main()
