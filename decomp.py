import os
import argparse

def decompress(data: bytes) -> bytes:
    """Simplified and clean LZSS decompressor matching FUN_8001e890 behavior."""

    window = bytearray(0x1000)   # 4KB sliding window
    win_pos = 0                  # write pointer
    out = bytearray()

    p = 0
    end = len(data)

    while p < end:
        flag = data[p]
        p += 1

        for bit in range(8):
            if p >= end:
                return bytes(out)

            # bit = 0 → literal
            if ((flag >> (7 - bit)) & 1) == 0:
                b = data[p]
                p += 1

                window[win_pos] = b
                win_pos = (win_pos + 1) & 0xFFF

                out.append(b)

            # bit = 1 → back-reference
            else:
                if p + 1 >= end:
                    return bytes(out)

                b1 = data[p]
                b2 = data[p + 1]
                p += 2

                combined = (b1 << 8) | b2
                offset = (combined >> 4) & 0xFFF
                length = (combined & 0xF) + 3

                for _ in range(length):
                    b = window[offset]
                    offset = (offset + 1) & 0xFFF

                    window[win_pos] = b
                    win_pos = (win_pos + 1) & 0xFFF

                    out.append(b)

    return bytes(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input archive file")
    parser.add_argument("-o", "--output", help="Output directory",required=True)
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        compress_data = f.read()

    decompress_data = decompress(compress_data[0x10:])

    filename = os.path.basename(args.input)

    with open(f"{args.output}/{filename}", "wb") as f:
        f.write(decompress_data)


if __name__ == "__main__":
    main()