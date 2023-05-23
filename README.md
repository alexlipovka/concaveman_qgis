# About

This is a wrapper-type plugin, bases on amazing:
- [very fast 2D concave hull algorithm in JavaScript by Vladimir Agafonkin](https://github.com/mapbox/concaveman)
- [C++ port of mapbox's JS concaveman, with a Python wrapper](https://github.com/sadaszewski/concaveman-cpp)

Core functionality:
- choose Point layer
- generate concave hull for all or selected points in that layer

# Installation

Open osgeo4w shell and run:

```bash
python -m ensurepip --upgrade
pip install cffi
```

Copy "lib" folder with supplied DLL to plugin dir
```bash
$APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\concaveman_qgis
```

# Dependencies

Plugin depends on the following Python libraries:
- shapely
- numpy
- scipy
- cffi

Binary dependencies:
- concaveman-cpp compiled library  
  `DLL` for Windows is inluded  
	`SO` for Linux should be compiled from [source](https://github.com/sadaszewski/concaveman-cpp)

# License

GPLv3
