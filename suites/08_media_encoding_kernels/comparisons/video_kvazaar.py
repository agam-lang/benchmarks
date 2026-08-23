def intra_mode_decision(block, block_size):
    best_cost = 10000000
    for mode in range(35):
        sad_cost = 0
        for y in range(block_size):
            for x in range(block_size):
                actual = block[y * block_size + x]
                if mode == 0:
                    predicted = (x + y) * 8
                elif mode == 1:
                    predicted = 128
                else:
                    predicted = ((x * mode) + (y * (35 - mode))) % 256

                diff = actual - predicted
                sad_cost += abs(diff)
        if sad_cost < best_cost:
            best_cost = sad_cost
    return best_cost

def main():
    block_size = 16
    block = []
    for i in range(block_size * block_size):
        val = ((i * 1664525 + 1013904223) // 65536) % 256
        block.append(val)

    total_cost = 0
    for _ in range(1000):
        total_cost += intra_mode_decision(block, block_size)
    print(total_cost)

if __name__ == "__main__":
    main()
