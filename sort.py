import argparse
from pathlib import Path
from shutil import copyfile, rmtree
from threading import Thread
import logging


parser = argparse.ArgumentParser(description='App for sorting folder')
parser.add_argument('-s', '--source', required=True,
                    help='folder that we want to sort')
parser.add_argument('-o', '--output', default='dist',
                    help='output folder, by default="dist"')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')

folders = []


def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path):
    logging.debug(f' is starting')
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            ext = ext[1:]
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(threadName)s %(message)s')
    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    try:
        grabs_folder(base_folder)
        print(folders)
    except OSError as e:
        logging.error(e)
        exit()

    treads = []
    for folder in folders:
        th = Thread(
            name=f'Thread for folder {folder}', target=copy_file, args=(folder, ))
        th.start()
        treads.append(th)

    [th.join() for th in treads]
    print(f"Ready for delete folder {base_folder}")
    rmtree(base_folder)
    print(f"Folder {base_folder} has been delete")
