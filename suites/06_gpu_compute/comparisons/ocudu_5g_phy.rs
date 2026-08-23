fn ldpc_decode_layer(llr_in: &[i32], length: usize, iterations: usize) -> i32 {
    let mut syndrome_sum: i32 = 0;
    for _ in 0..iterations {
        let mut i = 0;
        while i < length - 4 {
            let l0 = llr_in[i];
            let l1 = llr_in[i + 1];
            let l2 = llr_in[i + 2];
            let l3 = llr_in[i + 3];

            let min1 = l0.abs().min(l1.abs());
            let min2 = l2.abs().min(l3.abs());
            let check_val = min1.min(min2);
            let sign = if (l0 ^ l1 ^ l2 ^ l3) < 0 { -1 } else { 1 };
            syndrome_sum += check_val * sign;
            i += 4;
        }
    }
    syndrome_sum
}

fn main() {
    let num_symbols = 16384;
    let mut llr = Vec::with_capacity(num_symbols);
    for i in 0..num_symbols {
        let val = ((i.wrapping_mul(1664525) + 1013904223) / 65536) % 256;
        llr.push(val as i32 - 128);
    }

    let res = ldpc_decode_layer(&llr, num_symbols, 8);
    println!("{}", res);
}
