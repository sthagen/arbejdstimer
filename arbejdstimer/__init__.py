# [[[fill git_describe()]]]
__version__ = '2022.10.3+parent.55129dee'
# [[[end]]] (checksum: fd5e9dcecc8bc84eebd1b6fa199042c5)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []
