fn fir_filter_block(
    input: &[f64],
    coeffs: &[f64],
    buffer_len: usize,
    filter_len: usize,
    passes: usize,
) -> f64 {
    let mut energy_sum: f64 = 0.0;
    for _ in 0..passes {
        for i in filter_len..buffer_len {
            let mut acc: f64 = 0.0;
            for k in 0..filter_len {
                acc += input[i - k] * coeffs[k];
            }
            energy_sum += acc * acc;
        }
    }
    energy_sum
}

fn main() {
    let buffer_len = 256;
    let filter_len = 32;

    let mut input = Vec::with_capacity(buffer_len);
    for i in 0..buffer_len {
        input.push((i % 17) as f64 * 0.1);
    }

    let mut coeffs = Vec::with_capacity(filter_len);
    for k in 0..filter_len {
        coeffs.push((k % 7) as f64 * 0.05);
    }

    let energy = fir_filter_block(&input, &coeffs, buffer_len, filter_len, 2000);
    println!("{}", energy as i64);
}
