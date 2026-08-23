def ldpc_decode_layer(llr_in, length, iterations):
    syndrome_sum = 0
    for _ in range(iterations):
        i = 0
        while i < length - 4:
            l0 = llr_in[i]
            l1 = llr_in[i + 1]
            l2 = llr_in[i + 2]
            l3 = llr_in[i + 3]

            min1 = min(abs(l0), abs(l1))
            min2 = min(abs(l2), abs(l3))
            check_val = min(min1, min2)
            sign = -1 if (l0 ^ l1 ^ l2 ^ l3) < 0 else 1
            syndrome_sum += check_val * sign
            i += 4
    return syndrome_sum

def main():
    num_symbols = 16384
    llr = []
    for i in range(num_symbols):
        val = ((i * 1664525 + 1013904223) // 65536) % 256
        llr.append(val - 128)

    res = ldpc_decode_layer(llr, num_symbols, 8)
    print(res)

if __name__ == "__main__":
    main()
