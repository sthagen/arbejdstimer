# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/etc/sbom/cdx.json) with SHA256 checksum ([401c573f ...](https://git.sr.ht/~sthagen/arbejdstimer/blob/default/etc/sbom/cdx.json.sha256 "sha256:401c573f3ceb3ae21a1c4c12be8d779dd2fee2d280915f36d3ee5301b4ba6f5c")).
<!--[[[end]]] (checksum: 7d1e1120fc5a768747e308d67dfe22cc)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                           | License     | Author                                                                                                                                                                                                                                                        | Description (from packaging data)                                  |
|:-------------------------------------------------|:--------------------------------------------------|:------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------|
| [pydantic](https://github.com/pydantic/pydantic) | [2.4.1](https://pypi.org/project/pydantic/2.4.1/) | MIT License | Samuel Colvin <s@muelcolvin.com>, Eric Jolibois <em.jolibois@gmail.com>, Hasan Ramezani <hasan.r67@gmail.com>, Adrian Garcia Badaracco <1755071+adriangb@users.noreply.github.com>, Terrence Dorsey <terry@pydantic.dev>, David Montague <david@pydantic.dev> | Data validation using Python type hints                            |
| [typer](https://github.com/tiangolo/typer)       | [0.9.0](https://pypi.org/project/typer/0.9.0/)    | MIT License | Sebastián Ramírez                                                                                                                                                                                                                                             | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 895758d466a249aebfdd48353bd9ffd3)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                                             | Version                                                    | License                            | Author                                                                                | Description (from packaging data)                      |
|:-----------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|:-------------------------------------------------------|
| [click](https://palletsprojects.com/p/click/)                    | [8.1.5](https://pypi.org/project/click/8.1.5/)             | BSD License                        | UNKNOWN                                                                               | Composable command line interface toolkit              |
| [typing_extensions](https://github.com/python/typing_extensions) | [4.7.1](https://pypi.org/project/typing_extensions/4.7.1/) | Python Software Foundation License | "Guido van Rossum, Jukka Lehtosalo, Łukasz Langa, Michael Lee" <levkivskyi@gmail.com> | Backported and Experimental Type Hints for Python 3.7+ |
<!--[[[end]]] (checksum: e4e0711b27c84b7d53d7caceeba18d27)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
pydantic==2.4.1
├── annotated-types [required: >=0.4.0, installed: 0.5.0]
├── pydantic-core [required: ==2.10.1, installed: 2.10.1]
│   └── typing-extensions [required: >=4.6.0,!=4.7.0, installed: 4.7.1]
└── typing-extensions [required: >=4.6.1, installed: 4.7.1]
typer==0.9.0
├── click [required: >=7.1.1,<9.0.0, installed: 8.1.5]
└── typing-extensions [required: >=3.7.4.3, installed: 4.7.1]
````
<!--[[[end]]] (checksum: bedfab7cbb379bb11a5b627c0f2a7222)-->
