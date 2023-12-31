# PyLiDAR
![LiDAR Gif](https://github.com/yohanesnuwara/PyLiDAR/assets/51282928/20866586-1eea-4485-a4ee-8a2db9d6bd87)

We make it easier to perform analysis on LiDAR point cloud dataset in Python language, to be used mainly in forestry application. 

## Motivation

A very popular Python library for point cloud dataset called PDAL (Point Cloud Data Abstraction Library) mainly uses JSON pipelines. The parameters are controlled inside the JSON pipelines, which is quite complicated. So we build a library to run these pipelines in the language of Python. Using pipeline in PyLiDAR looks like using pipeline in [Scikit-Learn](https://scikit-learn.org/stable/).  

## Current Functionalities

Current functionalities of PyLiDAR are:

* Read and convert LAS to LAZ, vice versa
* Classification of point cloud
* Removing outlier from point cloud
* Creating Digital Surface Map (DSM), Digital Terrain Map (DTM), and Canopy Height Map (CHM)
