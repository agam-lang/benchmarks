fn predict_spatial_residual(pixels: &[i32], width: usize, height: usize, quality: i32) -> i32 {
    let mut total_residual: i32 = 0;
    for y in 1..height {
        for x in 1..width {
            let curr = pixels[y * width + x];
            let top = pixels[(y - 1) * width + x];
            let left = pixels[y * width + (x - 1)];
            let top_left = pixels[(y - 1) * width + (x - 1)];

            let p = left + top - top_left;
            let pa = (p - left).abs();
            let pb = (p - top).abs();
            let pc = (p - top_left).abs();

            let pred = if pa <= pb && pa <= pc {
                left
            } else if pb <= pc {
                top
            } else {
                top_left
            };

            let residual = (curr - pred) * quality / 100;
            total_residual += residual.abs();
        }
    }
    total_residual
}

fn main() {
    let width = 256;
    let height = 256;
    let mut pixels = Vec::with_capacity(width * height);
    for i in 0..(width * height) {
        let val = ((i.wrapping_mul(1103515245) + 12345) / 65536) % 256;
        pixels.push(val as i32);
    }

    let res = predict_spatial_residual(&pixels, width, height, 100);
    println!("{}", res);
}
