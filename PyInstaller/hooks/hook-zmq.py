#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
Hook for PyZMQ. Cython based Python bindings for messaging library ZeroMQ.
http://www.zeromq.org/
"""


import glob
import os
from PyInstaller.hooks.hookutils import collect_submodules

hiddenimports = ['zmq.utils.garbage',
                 'zmq.core.pysocket',
                 'zmq.utils.jsonapi',
                 'zmq.utils.strtypes',
                 ]
hiddenimports.extend(collect_submodules('zmq.backend'))


def hook(mod):
    # If PyZMQ provides its own copy of libzmq, add it to the
    # extension-modules TOC so zmq/__init__.py can load it at runtime.
    # For predictable behavior, the libzmq search here must be identical
    # to the search in zmq/__init__.py.
    zmq_directory = os.path.dirname(mod.__file__)
    for libname in ('libzmq', 'libsodium'):
        libname_re = re.compile(libname + r"\.(?:so|pyd|dll|dylib).*")
        bundled = [os.path.join(zmq_directory, fname)
                   for fname in os.listdir(zmq_directory)
                   if libname_re.match(fname)]

        if bundled:
            # zmq/__init__.py will look in os.join(sys._MEIPASS, 'zmq'),
            # so libzmq has to land there.
            name = os.path.join('zmq', os.path.basename(bundled[0]))
            mod.binaries.append((name, bundled[0], 'BINARY'))
            break

    return mod
