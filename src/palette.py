import extcolors


def img_to_palette(colored_img_path):
    colors, pixel_count = extcolors.extract_from_path(colored_img_path)
    colors_cummul = []
    prob_sum = 0
    for color, occurrence in colors:
        probability = occurrence/pixel_count
        prob_sum += probability
        colors_cummul.append((color, prob_sum))
    # print(colors)
    # print(colors_cummul)
    # print(f"Number of colors: {len(colors)}")
    # print(f"Number of pixels: {pixel_count}")
    # print(f"Summed pixels: {sum}")
    return colors_cummul
