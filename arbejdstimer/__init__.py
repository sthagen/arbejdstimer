# [[[fill git_describe()]]]
__version__ = '2022.10.5+parent.099e9140'
# [[[end]]] (checksum: 4dbe1fa889441bf5859073290d84b181)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []
