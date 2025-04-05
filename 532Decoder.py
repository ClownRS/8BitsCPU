import os

### 用于给532译码器编码。

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '532Decoder.bin')

with open(filename, 'wb') as file:
    for val in range(32):
        result = 1 << val
        binary = result.to_bytes(4, byteorder='little')
        file.write(binary)
        print(binary)
print("Compile Complete!")