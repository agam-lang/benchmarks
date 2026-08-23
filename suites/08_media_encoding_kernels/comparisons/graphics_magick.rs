fn graphics_magick_pipeline(pixels: &[i32], width: usize, height: usize) -> i32 {
    let mut accumulator: i32 = 0;
    for y in 1..(height - 1) {
        for x in 1..(width - 1) {
            let center = pixels[y * width + x];
            let top = pixels[(y - 1) * width + x];
            let bottom = pixels[(y + 1) * width + x];
            let left = pixels[y * width + (x - 1)];
            let right = pixels[y * width + (x + 1)];

            let sharpened = center * 5 - top - bottom - left - right;
            let noise = ((x * 13 + y * 37) % 31) as i32 - 15;
            let filtered = (sharpened + noise) % 256;

            accumulator += filtered.abs();
        }
    }
    accumulator
}

fn main() {
    let width = 256;
    let height = 256;
    let mut pixels = Vec::with_capacity(width * height);
    for i in 0..(width * height) {
        let val = ((i.wrapping_mul(1103515245) + 12345) / 65536) % 256;
        pixels.push(val as i32);
    }

    let result = graphics_magick_pipeline(&pixels, width, height);
    println!("{}", result);
}
