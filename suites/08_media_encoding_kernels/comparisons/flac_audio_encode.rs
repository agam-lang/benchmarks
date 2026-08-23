fn lpc_residual_encode(samples: &[i32], num_samples: usize, order: usize) -> i64 {
    let mut residual_energy: i64 = 0;
    for i in order..num_samples {
        let mut predicted = 0;
        for k in 0..order {
            predicted += samples[i - 1 - k] / (k as i32 + 2);
        }
        let diff = samples[i] - predicted;
        residual_energy += diff.abs() as i64;
    }
    residual_energy
}

fn main() {
    let num_samples = 32768;
    let mut samples = Vec::with_capacity(num_samples);
    for i in 0..num_samples {
        let val = ((i.wrapping_mul(1103515245) + 12345) / 65536) % 32768;
        samples.push(val as i32 - 16384);
    }

    let energy = lpc_residual_encode(&samples, num_samples, 8);
    println!("{}", energy);
}
