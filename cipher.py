import argparse
import io
import multiprocessing
import string

def rotate(s, n):
    # Define the valid characters
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    # Create a mapping of each character to its corresponding rotated character
    rotated_chars = chars[n:] + chars[:n]
    # Create a dictionary mapping each character to its rotated character
    char_map = dict(zip(chars, rotated_chars))
    # Apply the rotation to each character in the string
    result = "".join(char_map.get(c.lower(), c) for c in s)
    # Apply uppercase to rotated uppercase characters
    # result = "".join(rotated_chars[chars.index(c.lower())].upper() if c.isupper() and char_map.get(c.lower(), c).isalpha() else char_map.get(c.lower(), c) for c in s)
    return result

def encrypt_chunk(chunk, key):
    return rotate(chunk, key)

def decrypt_chunk(chunk, key):
    return rotate(chunk, -key)

def process_chunk(chunk, key, encrypt_mode):
    if encrypt_mode:
        return encrypt_chunk(chunk, key)
    else:
        return decrypt_chunk(chunk, key)

def process_file(file_name, key, encrypt_mode):
    if encrypt_mode:
        output_file_name = file_name + "-enc-" + str(key) + ".txt"
    else:
        output_file_name = file_name + "-dec-" + str(key) + ".txt"
    chunk_size = 1024*1024*1
    with io.open(file_name, "r") as input_file, \
         io.open(output_file_name, "w") as output_file, \
         multiprocessing.Pool() as pool:
        while True:
            chunk = input_file.read(chunk_size)
            if not chunk:
                break
            output_chunk = pool.apply(process_chunk, (chunk, key, encrypt_mode))
            output_file.write(output_chunk)

def process_text(text, key, encrypt_mode):
    if encrypt_mode:
        output_text = encrypt_chunk(text, key)
    else:
        output_text = decrypt_chunk(text, key)
    print(output_text)

def main():
    parser = argparse.ArgumentParser(description='Rotate a string by a given key.', epilog='May you be blessed with the truth of the cosmos.')
    parser.add_argument('input', metavar='input', type=str, help='input file or text')
    parser.add_argument('-d', dest='decrypt', action='store_true', help='decrypt instead of encrypt')
    parser.add_argument('-key', metavar='key', type=int, default=13, help='the key to use for rotation')
    args = parser.parse_args()

    if args.input.endswith(".txt"):
        process_file(args.input, args.key, not args.decrypt)
    else:
        process_text(args.input, args.key, not args.decrypt)
  
if __name__ == '__main__':
    main()
