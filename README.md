# About

This is a wrapper-type plugin, bases on amazing:
- [very fast 2D concave hull algorithm in JavaScript by Vladimir Agafonkin](https://github.com/mapbox/concaveman)
- [C++ port of mapbox's JS concaveman, with a Python wrapper](https://github.com/sadaszewski/concaveman-cpp)

Core functionality:
- choose Point layer
- generate concave hull for all points in that layer

# Dependencies

Plugin depends on the following Python libraries:
- shapely
- numpy
- scipy

Binary dependencies:
- concaveman-cpp complid library  
  `DLL` for Windows is inluded and should be placed in "C:\soft\extraDLLS"
	`SO` for Linux should be compiled from [source](https://github.com/sadaszewski/concaveman-cpp)

# License

GPLv3