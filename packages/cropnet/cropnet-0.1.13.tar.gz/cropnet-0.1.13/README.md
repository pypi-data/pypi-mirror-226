# CropNet

CropNet is an open, large-scale, and deep learning-ready dataset, specifically targeting climate change-aware crop yield predictions for the contiguous United States (U.S.) continent at the county level. It is composed of three modalities of data, i.e., Sentinel-2 Imagery, WRF-HRRR Computed Dataset, and USDA Crop Dataset, aligned in both the spatial and temporal domains, for over 2200 U.S. counties spanning 6 years (2017-2022). It is expected to facilitate researchers in developing deep learning models for timely and precisely predicting crop yields at the county level, by accounting for the effects of both short-term growing season weather variations and long-term climate change on crop yields.



## Overview

The CropNet dataset is composed of three modalities of data, i.e., Sentinel-2 Imagery, WRF-HRRR Computed Dataset, and USDA Crop Dataset, spanning from 2017 to 2022 (i.e., 6 years) across 2291 U.S. counties. 

- The dataset is available at [Google Drive](https://drive.google.com/drive/folders/1Js98GAxf1LeAUTxP1JMZZIrKvyJStDgz)

- The tutorials for each modality of data are availbale at [Github](https://anonymous.4open.science/r/CropNet)

  

#### Sentinel-2 Imagery

The Sentinel-2 Imagery, obtained from the [Sentinel-2 mission](https://sentinel.esa.int/web/sentinel/missions/sentinel-2), provides high-resolution satellite images for monitoring crop growth on the ground. It contains 224x224 RGB satellite images, with a spatial resolution of 9x9 km, and a revisit frequency of 14 days. 

#### WRF-HRRR Computed Dataset

The WRF-HRRR Computed Dataset, sourced from the [WRF-HRRR model](https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html), contains daily and monthly meteorological parameters, with the former and the latter designed for capturing the direct effects of short-term growing season weather variations on crop growth, and for learning the indirect impacts of long-term climate change on crop yields, respectively. It contains 9 meteorological parameters gridded at 9 km in a one-day (and one-month) interval.

#### USDA Crop Dataset

The USDA Crop Dataset, collected from the [USDA Quick Statistic website](https://quickstats.nass.usda.gov/), offers valuable crop information, such as production, yield, etc., for crops grown at each available county. It offers crop information for four types of crops, i.e., corn, cotton, soybeans, and winter wheat, at a county-level basis, with a temporal resolution of one year.



Although our initial goal of crafting the CropNet dataset is for precise crop yield prediction, we believe its future applicability is broad and can benefit the deep learning, agriculture, and meteorology communities, for exploring more interesting and critical climate change-related applications, by using one or more modalities of data.



## Pipeline

The code in this reposity:

1. combines all three modalities of data to create $(\mathbf{x}, \mathbf{y_{s}}, \mathbf{y_{l}}, \mathbf{z})$ tuples, with $\mathbf{x}$, $\mathbf{y_{s}}$, $\mathbf{y_{l}}$, and $\mathbf{z}$ representing satellite images, short-term daily whether parameters, long-term monthly meteorological parameters, and ground-truth crop yield (or production) information, respectively and
2. exposes those tuples via a `Dataset` object.

Notably, one or more modalities of data can be used for specific deep learning tasks. For example,

1. satellite images can be solely utilized for pre-training deep neural networks in a self-supervised learning manner (e.g., [SimCLR](https://arxiv.org/pdf/2002.05709.pdf), [MAE](https://arxiv.org/pdf/2111.06377.pdf), etc.), or
2. a pair of $(\mathbf{x}, \mathbf{y_{s}})$ under the same 9x9 km grid can be used for exploring the local weather effect on crop growth.



## Installation

MacOS and Linux users can install the latest version of CropNet with the following command:

```python
pip install cropnet
```



Note that if your Python version is older than 3.10.0, you may need to run the following commend before installation to make sure `cartopy` is successfully installed:

```shell
sudo apt install python3-dev libproj-dev proj-data proj-bin libgeos-dev
# If using Python 3.x, consider installing python3.x-dev
sudo apt install python3.10-dev

# install required package for Heribe
pip install ecmwflibs
```





## License

CropNet has a [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) license.