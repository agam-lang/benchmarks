def lpc_residual_encode(samples, num_samples, order):
    residual_energy = 0
    for i in range(order, num_samples):
        predicted = 0
        for k in range(order):
            predicted += samples[i - 1 - k] // (k + 2)
        diff = samples[i] - predicted
        residual_energy += abs(diff)
    return residual_energy

def main():
    num_samples = 32768
    samples = []
    for i in range(num_samples):
        val = ((i * 1103515245 + 12345) // 65536) % 32768
        samples.append(val - 16384)

    energy = lpc_residual_encode(samples, num_samples, 8)
    print(energy)

if __name__ == "__main__":
    main()
