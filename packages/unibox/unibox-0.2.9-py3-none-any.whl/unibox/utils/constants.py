"commonly used constant variables"

__all_imgs_raw = (
    "jpg jpeg png bmp dds exif jp2 jpx pcx pnm ras gif tga tif tiff xbm xpm webp"
)
IMG_FILES = ["." + i.strip() for i in __all_imgs_raw.split(" ")]
