from PIL import Image, ImageOps, ImageGrab

MAX = 256
HUE_SHIFT_DEG = MAX // 2
BRIGHTNESS_INCR = 30


# Get image
png_image = ImageGrab.grabclipboard()
if png_image is None:
	input("No image in clipboard. Press enter to exit... ")
	exit(1)


# Ask whether the image should be hue-shifted
# ... to counteract the inverted colours
response = input("Also shift hue? (y/n) ").strip().lower()
hue_shift = response == "y"


# Preserve alpha, recombined later
r, g, b, a = png_image.split()
rgb_image = Image.merge("RGB", (r, g, b))

inverted_image = ImageOps.invert(rgb_image)
final_image = inverted_image

if hue_shift:
	# Do the hue shift, convert back to RGB
	image_hsv = final_image.convert("HSV")
	h, s, v = image_hsv.split()
	shifted_h = h.point(lambda p: (p + HUE_SHIFT_DEG) % MAX)
	shifted_hsv_image = Image.merge("HSV", (shifted_h, s, v))

	shifted_rgb_image = shifted_hsv_image.convert("RGB")
	final_image = shifted_rgb_image

# Increase brightness by +30
r2, g2, b2 = final_image.split()
add_brightness = lambda p: min(p + BRIGHTNESS_INCR, MAX - 1)
shifted_r2 = r2.point(add_brightness)
shifted_g2 = g2.point(add_brightness)
shifted_b2 = b2.point(add_brightness)

final_png_image = Image.merge("RGBA", \
  (shifted_r2, shifted_g2, shifted_b2, a))


# Display image
# Doesn't copy to clipboard
final_png_image.show()