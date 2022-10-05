# [[[fill git_describe()]]]
__version__ = '2022.10.5+parent.930d1a72'
# [[[end]]] (checksum: 4e1fa2fb7844ab7f0a3ffe11740134f9)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []
