fn intra_mode_decision(block: &[i32], block_size: usize) -> i32 {
    let mut best_cost = 10000000;
    for mode in 0..35 {
        let mut sad_cost = 0;
        for y in 0..block_size {
            for x in 0..block_size {
                let actual = block[y * block_size + x];
                let predicted = if mode == 0 {
                    (x as i32 + y as i32) * 8
                } else if mode == 1 {
                    128
                } else {
                    ((x as i32 * mode as i32) + (y as i32 * (35 - mode as i32))) % 256
                };

                let diff = actual - predicted;
                sad_cost += diff.abs();
            }
        }
        if sad_cost < best_cost {
            best_cost = sad_cost;
        }
    }
    best_cost
}

fn main() {
    let block_size = 16;
    let mut block = Vec::with_capacity(block_size * block_size);
    for i in 0..(block_size * block_size) {
        let val = ((i.wrapping_mul(1664525) + 1013904223) / 65536) % 256;
        block.push(val as i32);
    }

    let mut total_cost = 0;
    for _ in 0..1000 {
        total_cost += intra_mode_decision(&block, block_size);
    }
    println!("{}", total_cost);
}
