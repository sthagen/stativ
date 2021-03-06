# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://github.com/sthagen/pilli/blob/default/sbom.json) with SHA256 checksum ([f7ccd583 ...](https://raw.githubusercontent.com/sthagen/pilli/default/sbom.json.sha256 "sha256:f7ccd5834b5b552ce7c571f986c576ae3fd6670435517aed704a570824641889")).
<!--[[[end]]] (checksum: 90f9f42c818e3eeb04d4833d255c9261)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                         | License     | Author                             | Description (from packaging data)                                  |
|:-------------------------------------------------|:------------------------------------------------|:------------|:-----------------------------------|:-------------------------------------------------------------------|
| [scooby](https://github.com/banesullivan/scooby) | [0.6.0](https://pypi.org/project/scooby/0.6.0/) | MIT License | Dieter Werthmüller & Bane Sullivan | A Great Dane turned Python environment detective                   |
| [typer](https://github.com/tiangolo/typer)       | [0.4.2](https://pypi.org/project/typer/0.4.2/)  | MIT License | Sebastián Ramírez                  | Typer, build great CLIs. Easy to code. Based on Python type hints. |
<!--[[[end]]] (checksum: 0c65629131b0cda5fc4562beaa2cc72c)-->

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

<img src="https://raw.githubusercontent.com/sthagen/pilli/default/docs/third-party/package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
scooby==0.6.0
typer==0.4.2
  - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
````
<!--[[[end]]] (checksum: 080552ed1697f3c164b61b186558a345)-->
