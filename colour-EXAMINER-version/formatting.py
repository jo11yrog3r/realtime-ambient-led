def colour_block(rgb):
        r, g, b = rgb
        return f"\033[48;2;{r};{g};{b}m    \033[0m"

def rgb_to_hex(rgb):
        hex_color_code = '#' + ''.join(f'{value:02x}' for value in rgb)
        return hex_color_code