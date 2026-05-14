#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

def create_png(width, height, pixels):
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
    
    signature = b'\x89PNG\r\n\x1a\n'
    
    ihdr = struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0)
    
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'
        for x in range(width):
            r, g, b, a = pixels[y][x]
            raw_data += bytes([r, g, b, a])
    
    import zlib
    compressed = zlib.compress(raw_data)
    
    iend = b''
    
    png_data = signature + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', iend)
    return png_data

def create_icon():
    size = 128
    pixels = []
    
    for y in range(size):
        row = []
        for x in range(size):
            cx, cy = size // 2, size // 2
            
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            
            if dist < size // 3:
                row.append((100, 100, 100, 255))
            elif dist < size // 2:
                row.append((60, 60, 80, 255))
            else:
                row.append((30, 30, 50, 255))
        
        pixels.append(row)
    
    png = create_png(size, size, pixels)
    
    with open('icon.png', 'wb') as f:
        f.write(png)
    
    print("图标已创建: icon.png")

if __name__ == "__main__":
    create_icon()