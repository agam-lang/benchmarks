def fir_filter_block(input_arr, coeffs, buffer_len, filter_len, passes):
    energy_sum = 0.0
    for _ in range(passes):
        for i in range(filter_len, buffer_len):
            acc = 0.0
            for k in range(filter_len):
                acc += input_arr[i - k] * coeffs[k]
            energy_sum += acc * acc
    return energy_sum

def main():
    buffer_len = 256
    filter_len = 32

    input_arr = [(i % 17) * 0.1 for i in range(buffer_len)]
    coeffs = [(k % 7) * 0.05 for k in range(filter_len)]

    energy = fir_filter_block(input_arr, coeffs, buffer_len, filter_len, 2000)
    print(int(energy))

if __name__ == "__main__":
    main()
