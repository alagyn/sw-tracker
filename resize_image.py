from argparse import ArgumentParser
import os
from PIL import Image

OUT_SIZE = 250


def main():
    parser = ArgumentParser()
    _ = parser.add_argument("in_dir")
    _ = parser.add_argument("out_dir")

    args = parser.parse_args()

    in_dir = str(args.in_dir)
    out_dir = str(args.out_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    for file in os.listdir(in_dir):
        in_file = os.path.join(in_dir, file)
        x = Image.open(in_file)
        if x.width > x.height:
            scaleFactor = 500 / x.width
        else:
            scaleFactor = 500 / x.height

        out = x.resize(
            (int(x.width * scaleFactor), int(x.height * scaleFactor)))

        out_name, _ = os.path.splitext(file)
        out_file = os.path.join(out_dir, f'{out_name}.jpg')
        out.save(out_file)


if __name__ == '__main__':
    main()
