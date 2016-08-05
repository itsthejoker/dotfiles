#!/usr/bin/env python

import os
import sys
import logging
import argparse
import shutil

from subprocess import call


def backup_atom(base_path, home):
    logger.info("Attempting to back up Atom settings...")
    path = home+"/.atom"
    # do we even have an atom installation to back up?
    if os.path.isdir(path):
        # verify that the destination directory exists
        if not os.path.isdir(os.path.join(base_path+"/atom")):
            os.mkdir(os.path.join(base_path+"/atom"))

        files = []
        files_to_copy = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            files.extend(filenames)
            # just want the first level
            break

        filetype = [".json", ".cson", ".coffee", ".less"]
        for item in files:
            filename, file_extension = os.path.splitext(item)
            if file_extension in filetype:
                files_to_copy.append(item)

        for item in files_to_copy:
            logger.debug("Copying {}...".format(item))
            logger.debug(os.path.join(base_path, "atom"))
            shutil.copyfile(os.path.join(path+"/"+item),
                            os.path.join(base_path+"/atom/"+item))

        os.chdir(os.path.join(base_path+"/atom"))
        # call gets annoyed if we don't create the file first
        open(os.path.join(base_path+"/atom/packages.list"), 'w').close
        call("apm list --installed --bare > {}/atom/packages.list".
             format(base_path), shell=True)

        logger.info("Successfully backed up Atom settings!")

    else:
        logger.info("Unable to locate ~/.atom, skipping")


def backup_bashrc(base_path, home):
    logger.debug("Attempting to back up .bashrc...")
    shutil.copyfile(os.path.join(home+"/.bashrc"),
                    os.path.join(base_path+"/"+"bashrc"))
    logger.info("Successfully backed up .bashrc!")


def backup_gitconfig(base_path, home):
    logger.debug("Attempting to back up .gitconfig...")
    shutil.copyfile(os.path.join(home+"/.gitconfig"),
                    os.path.join(base_path+"/"+"gitconfig"))
    logger.info("Successfully backed up .gitconfig!")


def backup(base_path, home):
    backup_atom(base_path, home)
    backup_bashrc(base_path, home)
    backup_gitconfig(base_path, home)


def restore(base_path, home):
    # for atom
    # apm install --packages-file packages.list
    pass


def main(argv):
    base_path = os.path.dirname(os.path.realpath(__file__))
    home = os.path.expanduser("~")
    logger.debug("Currently running at: {}".format(base_path))

    parser = argparse.ArgumentParser(
        description='Backup and restore Linux dotfiles.')
    parser.add_argument('-b', '-backup',
                        help="Backup dotfiles from current system.",
                        action="store_true")
    parser.add_argument('-r', '-restore',
                        help="Restore dotfiles from the working directory.",
                        action="store_true")

    args = parser.parse_args()
    if args.b == args.r:
        logger.error("You need to select only one of the options.")
        sys.exit(1)

    if args.b is True:
        backup(base_path, home)
    elif args.r is True:
        restore(base_path, home)


if __name__ == '__main__':

    logger = logging.getLogger('dotfile_manager')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    main(sys.argv)
