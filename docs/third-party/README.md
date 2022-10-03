# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://github.com/sthagen/pilli/blob/default/sbom.json) with SHA256 checksum ([80de1204 ...](https://raw.githubusercontent.com/sthagen/pilli/default/sbom.json.sha256 "sha256:80de1204cdcb81af2c291efbaa6b0a0e2199021f867c83ff78ef3bf46965564b")).
<!--[[[end]]] (checksum: 0d8ef07b6ae5041736f7d2b410c78ca4)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                             | License     | Author            | Description (from packaging data)                                  |
|:-------------------------------------------------|:----------------------------------------------------|:------------|:------------------|:-------------------------------------------------------------------|
| [pydantic](https://github.com/pydantic/pydantic) | [1.10.2](https://pypi.org/project/pydantic/1.10.2/) | MIT License | Samuel Colvin     | Data validation and settings management using python type hints    |
| [typer](https://github.com/tiangolo/typer)       | [0.6.1](https://pypi.org/project/typer/0.6.1/)      | MIT License | Sebastián Ramírez | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: ba7d82529443076bc022241162453539)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                              | Version                                          | License                              | Author             | Description (from packaging data)                                                   |
|:--------------------------------------------------|:-------------------------------------------------|:-------------------------------------|:-------------------|:------------------------------------------------------------------------------------|
| [sniffio](https://github.com/python-trio/sniffio) | [1.3.0](https://pypi.org/project/sniffio/1.3.0/) | Apache Software License; MIT License | Nathaniel J. Smith | Sniff out which async library your code is running under                            |
| anyio                                             | [3.6.1](https://pypi.org/project/anyio/3.6.1/)   | MIT License                          | Alex Grönholm      | High level compatibility layer for multiple asynchronous event loop implementations |
| idna                                              | [3.4](https://pypi.org/project/idna/3.4/)        | BSD License                          | UNKNOWN            | Internationalized Domain Names in Applications (IDNA)                               |
<!--[[[end]]] (checksum: 4706609630e88423504d8a2dfdf58cb1)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
pydantic==1.10.2
  - typing-extensions [required: >=4.1.0, installed: 4.3.0]
typer==0.6.1
  - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
````
<!--[[[end]]] (checksum: 4b5e787b58b17cf043812336b863be30)-->
