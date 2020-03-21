#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import argparse
import sys
from importlib import import_module

import colorful as cf

from thumbor import __release_date__, __version__
from thumbor.ext import BUILTIN_EXTENSIONS
from thumbor.filters import BUILTIN_FILTERS


def get_options():
    parser = argparse.ArgumentParser(description="thumbor doctor")

    parser.add_argument(
        "-n",
        "--nocolor",
        action="store_true",
        help="Disables coloring of thumbor doctor",
    )

    options = parser.parse_args()

    return {
        "nocolor": options.nocolor,
    }


def header(msg, color=cf.yellow):
    print(color(msg))


def subheader(msg, color=cf.bold_coral):
    print(color(msg))
    newline()


def newline():
    print()


def check_filters():
    newline()
    subheader('Verifying thumbor filters...')
    errors = []

    for filter_name in BUILTIN_FILTERS:
        try:
            import_module(filter_name)
            print(cf.bold_green('✅ %s' % filter_name))
        except ImportError as error:
            print(cf.bold_red('❎ %s' % filter_name))
            errors.append(error)

    return errors


def check_extensions():
    newline()
    subheader('Verifying thumbor compiled extensions...')
    errors = []

    for extension in BUILTIN_EXTENSIONS:
        ext_name = extension.replace('thumbor.ext.filters.', '')
        try:
            import_module(extension)
            print(cf.bold_green('✅ %s' % ext_name))
        except ImportError as error:
            print(cf.bold_red('❎ %s' % ext_name))
            errors.append(error)

    return errors


def check_modules():
    newline()
    subheader('Verifying pycurl support...')
    errors = []

    modules = (
        ('pycurl', 'Thumbor works much better with PyCurl. For more information visit http://pycurl.io/.'),
        ('cv2', 'Thumbor requires OpenCV for smart cropping. For more information check https://opencv.org/.'),
    )

    for module, error_message in modules:
        try:
            import_module(module)  # NOQA
            print(cf.bold_green('✅ %s is installed correctly.' % module))
        except ImportError as error:
            print(cf.bold_red('❎ %s is not installed.' % module))
            print(error_message)
            newline()
            errors.append('%s - %s' % (str(error), error_message))

    return errors


def main():
    """Converts a given url with the specified arguments."""

    options = get_options()

    cf.use_style('solarized')
    if (options["nocolor"]):
        cf.disable()

    newline()
    header('Thumbor v%s (of %s)' % (__version__, __release_date__))

    newline()
    print('Thumbor doctor will analyze your install and verify if everything is working as expected.')

    errors = check_modules()
    errors += check_filters()
    errors += check_extensions()

    newline()

    if errors:
        print(cf.bold_red('😞 Oh no! We found some things that could improve... 😞'))
        newline()
        print('\n'.join(['* %s' % str(err) for err in errors]))
        newline()
        newline()
        print(cf.cyan("If you don't know how to fix them, please open an issue with thumbor."))
        print(cf.cyan("Don't forget to copy this log and add it to the description of your issue."))
        print("Open an issue at https://github.com/thumbor/thumbor/issues/new")
        sys.exit(1)
        return

    print(cf.bold_green('🎉 Congratulations! No errors found! 🎉'))


if __name__ == "__main__":
    main()
