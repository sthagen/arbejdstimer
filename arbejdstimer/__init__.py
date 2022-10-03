# [[[fill git_describe()]]]
__version__ = '2022.10.2+parent.03bda739'
# [[[end]]] (checksum: 56721c6ad953105cc6c64a09dc952a5a)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []
