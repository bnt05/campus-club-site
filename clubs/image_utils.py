import os

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def center_crop_and_resize_imagefield(image_field, target_width, target_height):
    """以中心点为基准裁剪并调整 ImageField 到目标尺寸。"""
    if not image_field:
        return

    try:
        image_path = image_field.path
    except Exception:
        return

    if not os.path.exists(image_path):
        return

    try:
        with Image.open(image_path) as img:
            original_format = img.format or 'JPEG'
            if original_format.upper() == 'PNG':
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGBA', img.size, (255, 255, 255, 0))
                    background.paste(img, mask=img.split()[-1])
                    img = background
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            width, height = img.size
            target_ratio = target_width / target_height
            current_ratio = width / height

            if current_ratio > target_ratio:
                new_width = int(target_ratio * height)
                left = (width - new_width) // 2
                right = left + new_width
                top, bottom = 0, height
            else:
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                bottom = top + new_height
                left, right = 0, width

            img = img.crop((left, top, right, bottom))
            img = img.resize((target_width, target_height), Image.LANCZOS)

            save_kwargs = {}
            if original_format.upper() in ('JPEG', 'JPG'):
                save_kwargs['quality'] = 90
                save_kwargs['optimize'] = True
                img = img.convert('RGB')
            elif original_format.upper() == 'PNG':
                save_kwargs['optimize'] = True

            img.save(image_path, format=original_format, **save_kwargs)
    except ImportError:
        return
    except Exception:
        return
