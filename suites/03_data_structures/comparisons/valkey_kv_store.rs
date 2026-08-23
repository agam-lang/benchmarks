fn valkey_pipeline_ops(num_ops: usize) -> i32 {
    let table_size = 1024;
    let mut table_keys = vec![0i64; table_size];
    let mut table_vals = vec![0i64; table_size];

    let mut checksum: i64 = 0;
    for op in 0..num_ops {
        let key = ((op.wrapping_mul(2654435761)) / 65536) as i64;
        let slot = (key % 1024) as usize;

        match op % 3 {
            0 => {
                table_keys[slot] = key;
                table_vals[slot] = op as i64;
            }
            1 => {
                if table_keys[slot] == key {
                    checksum += table_vals[slot];
                }
            }
            _ => {
                table_vals[slot] += 1;
                checksum += table_vals[slot];
            }
        }
    }

    (checksum % 1000000007) as i32
}

fn main() {
    let result = valkey_pipeline_ops(100000);
    println!("{}", result);
}
