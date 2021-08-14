import os
import xml.etree.ElementTree as et
from shutil import copy2


def copy_file(destination: str, filename: str, source: str) -> None:
    full_source = os.path.join(source, filename)
    full_destination = os.path.join(destination, filename)
    copy2(full_source, full_destination)


def copy_files(config_file: str) -> None:
    root = et.parse(config_file).getroot()
    for child in root:
        source, destination, filename = child.attrib.values()
        # checks if destination folder doesn't exists creates one
        if not os.path.exists(destination):
            os.mkdir(destination)
        copy_file(destination, filename, source)


if __name__ == '__main__':
    config_xml = input("Enter path of your xml config file: ")
    if not os.path.exists(config_xml):
        raise FileNotFoundError(f'There is not file {config_xml}')
    copy_files(config_xml)
