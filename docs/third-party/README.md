# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/sbom.json) with SHA256 checksum ([989a0dd8 ...](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/sbom.json.sha256 "sha256:989a0dd891a0bcac4501ce25000acfed437d9fb9a8e2249923f415967201dfbe")).
<!--[[[end]]] (checksum: 3d35e422a5ca523e41fd64b26fea1b83)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                             | License     | Author            | Description (from packaging data)                                  |
|:-------------------------------------------------|:----------------------------------------------------|:------------|:------------------|:-------------------------------------------------------------------|
| [pydantic](https://github.com/pydantic/pydantic) | [1.10.3](https://pypi.org/project/pydantic/1.10.3/) | MIT License | Samuel Colvin     | Data validation and settings management using python type hints    |
| [typer](https://github.com/tiangolo/typer)       | [0.7.0](https://pypi.org/project/typer/0.7.0/)      | MIT License | Sebastián Ramírez | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 972b361286fd50133bbb76a606df1d75)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                          | Version                                        | License     | Author         | Description (from packaging data)         |
|:----------------------------------------------|:-----------------------------------------------|:------------|:---------------|:------------------------------------------|
| [click](https://palletsprojects.com/p/click/) | [8.1.3](https://pypi.org/project/click/8.1.3/) | BSD License | Armin Ronacher | Composable command line interface toolkit |
<!--[[[end]]] (checksum: dc3a866a7aa3332404bde3da87727cb9)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
pydantic==1.10.3
  - typing-extensions [required: >=4.1.0, installed: 4.4.0]
typer==0.7.0
  - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
````
<!--[[[end]]] (checksum: 08d53d195ca0946227b1329d968ba0dd)-->
