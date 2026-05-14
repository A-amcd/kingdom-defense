import struct
import zlib

def crc32(data):
    crc = 0xffffffff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xedb88320 if crc & 1 else 0)
    return crc ^ 0xffffffff

def chunk(type_bytes, data):
    length = struct.pack('!I', len(data))
    crc_data = type_bytes + data
    crc_val = struct.pack('!I', crc32(crc_data))
    return length + type_bytes + data + crc_val

def create_png():
    width, height = 128, 128
    signature = b'\x89PNG\r\n\x1a\n'
    
    ihdr = struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0)
    
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'
        for x in range(width):
            cx, cy = width // 2, height // 2
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            
            if dist < width // 4:
                r, g, b = 100, 100, 100
            elif dist < width // 2:
                r, g, b = 60, 60, 80
            else:
                r, g, b = 30, 30, 50
            raw_data += bytes([r, g, b, 255])
    
    compressed = zlib.compress(raw_data)
    iend = b''
    
    png_data = signature + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', iend)
    
    with open('icon.png', 'wb') as f:
        f.write(png_data)
    print("图标已创建: icon.png")

if __name__ == "__main__":
    create_png()