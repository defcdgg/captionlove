import struct
import os
import argparse

def extract(path):
    with open(path, "rb") as f:
        arc_data = f.read()

    if not arc_data.startswith(b"CAPT"):
        print("file error.")
        return
        
    file_count = struct.unpack("<I", arc_data[4:8])[0]

    file_name_pos = 8
    file_offset_pos = file_name_pos + file_count * 12
    file_size_pos = file_offset_pos + file_count * 4

    print(f'file offset start = {file_offset_pos:X}\nfile size start = {file_size_pos:X}')

    base = os.path.basename(path)
    out_dir = os.path.splitext(base)[0]
    os.makedirs(out_dir, exist_ok=True)

    file_names = []
    file_offsets = []
    file_sizes = []

    for i in range(file_count):
        raw_name = arc_data[file_name_pos:file_name_pos+12]
        file_name_pos += 12
        file_name = raw_name.split(b"\x00")[0].decode("ascii")
        if not file_name:
            file_name = f'file_{i}'
            print("get name error.")
        file_names.append(file_name)

        file_offset = struct.unpack("<I", arc_data[file_offset_pos:file_offset_pos+4])[0]
        file_offset_pos+=4
        file_offsets.append(file_offset)

        file_size = struct.unpack("<I", arc_data[file_size_pos:file_size_pos+4])[0]
        file_size_pos+=4
        file_sizes.append(file_size)

        with open(f'{out_dir}/{file_name}', "wb") as f:
            f.write(arc_data[file_offset:file_offset+file_size])




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input archive file")
    # parser.add_argument("-o", "--output", help="Output directory",required=True)
    args = parser.parse_args()

    # with open(args.input, "rb") as f:
    #     arc_data = f.read()

    extract(args.input)



if __name__ == "__main__":
    main()