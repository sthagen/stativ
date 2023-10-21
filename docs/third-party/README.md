# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://git.sr.ht/~sthagen/stativ/blob/default/etc/sbom/cdx.json) with SHA256 checksum ([c93fcb10 ...](https://git.sr.ht/~sthagen/stativ/blob/default/etc/sbom/cdx.json.sha256 "sha256:c93fcb1037feadd7cce8dd2504f77ca88c789787c4024e939213efc0feb6e68c")).
<!--[[[end]]] (checksum: 98a20663c4e37b3cb9d446b3dc945b8b)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                         | License     | Author                                                              | Description (from packaging data)                                  |
|:-------------------------------------------------|:------------------------------------------------|:------------|:--------------------------------------------------------------------|:-------------------------------------------------------------------|
| [scooby](https://github.com/banesullivan/scooby) | [0.9.2](https://pypi.org/project/scooby/0.9.2/) | MIT License | Dieter Werthmüller, Bane Sullivan, Alex Kaszynski, and contributors | A Great Dane turned Python environment detective                   |
| [typer](https://github.com/tiangolo/typer)       | [0.9.0](https://pypi.org/project/typer/0.9.0/)  | MIT License | Sebastián Ramírez                                                   | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 9daf881d3a72a1c5292c25171bae8bf6)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                          | Version                                        | License     | Author                                | Description (from packaging data)         |
|:----------------------------------------------|:-----------------------------------------------|:------------|:--------------------------------------|:------------------------------------------|
| [click](https://palletsprojects.com/p/click/) | [8.1.6](https://pypi.org/project/click/8.1.6/) | BSD License | Pallets <contact@palletsprojects.com> | Composable command line interface toolkit |
<!--[[[end]]] (checksum: 7b69d9be7fa227d2db394dcd865606d8)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
scooby==0.9.2
typer==0.9.0
├── click [required: >=7.1.1,<9.0.0, installed: 8.1.6]
└── typing-extensions [required: >=3.7.4.3, installed: 4.7.1]
````
<!--[[[end]]] (checksum: d448354db3c43fbf34f2bfa3219a5bea)-->
