# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/sbom.json) with SHA256 checksum ([bcc5548d ...](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/sbom.json.sha256 "sha256:bcc5548dc1f7b8796d51a3cf7e5000af293853970b69736b65de006dff3dfc22")).
<!--[[[end]]] (checksum: ec141f3e04097be9fa4e4019027887ae)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                             | License     | Author            | Description (from packaging data)                                  |
|:-------------------------------------------------|:----------------------------------------------------|:------------|:------------------|:-------------------------------------------------------------------|
| [pydantic](https://github.com/pydantic/pydantic) | [1.10.4](https://pypi.org/project/pydantic/1.10.4/) | MIT License | Samuel Colvin     | Data validation and settings management using python type hints    |
| [typer](https://github.com/tiangolo/typer)       | [0.7.0](https://pypi.org/project/typer/0.7.0/)      | MIT License | Sebastián Ramírez | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 8f3c3a35e13b46fc7130c695b478d1e9)-->

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
pydantic==1.10.4
  - typing-extensions [required: >=4.2.0, installed: 4.4.0]
typer==0.7.0
  - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
````
<!--[[[end]]] (checksum: 2540c630a2fe8086b1f338c32c77541c)-->
