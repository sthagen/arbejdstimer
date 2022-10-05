# [[[fill git_describe()]]]
__version__ = '2022.10.5+parent.8cca9741'
# [[[end]]] (checksum: ca4e367ea359c14e908b987b3136e11c)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []
