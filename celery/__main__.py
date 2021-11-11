"""Entry-point for the :program:`celery` umbrella command."""
from __future__ import absolute_import, print_function, unicode_literals

import sys

from . import maybe_patch_concurrency

__all__ = ['main']


def main():
    """Entrypoint to the ``celery`` umbrella command."""
    patch_pickle()
    if 'multi' not in sys.argv:
        maybe_patch_concurrency()
    from celery.bin.celery import main as _main
    _main()


def patch_pickle():
    """Patch pickle to support protocol 5

    Celery uses pickle.HIGHEST_PROTOCOL in several places, which makes
    it difficult to upgrade to a Python (3.8+) that supports protocol 5.
    The upgrade itself is not the problem, but issues arise if an older
    version of Python needs to read pickles created on Python 3.8+.

    Remove after dropping support for Python 3.7.x
    """
    import pickle
    if pickle.HIGHEST_PROTOCOL < 5:
        try:
            import pickle5
            sys.modules["pickle"] = pickle5
        except ImportError:
            pass


if __name__ == '__main__':  # pragma: no cover
    main()
