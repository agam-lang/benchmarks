def valkey_pipeline_ops(num_ops):
    table_size = 1024
    table_keys = [0] * table_size
    table_vals = [0] * table_size

    checksum = 0
    for op in range(num_ops):
        key = (op * 2654435761 // 65536)
        slot = key % 1024

        mode = op % 3
        if mode == 0:
            table_keys[slot] = key
            table_vals[slot] = op
        elif mode == 1:
            if table_keys[slot] == key:
                checksum += table_vals[slot]
        else:
            table_vals[slot] += 1
            checksum += table_vals[slot]

    return checksum % 1000000007

def main():
    result = valkey_pipeline_ops(100000)
    print(result)

if __name__ == "__main__":
    main()
