# PCT - Point Cloud Tiling

This repository contains a Python toolkit for tiling large-scale point cloud data efficiently. It is designed to handle large LAS files by segmenting them into smaller, manageable tiles which can be processed or analyzed independently. This is particularly useful for working with massive datasets in applications like geographical information systems (GIS), 3D modeling, and large-scale environmental analysis.

### Features

* **Efficient Handling of Large Files:** Breaks down large LAS files into smaller tiles.
* **Customizable Tiling Options:** Allows users to define the size of tiles and the subsampling precision per tile.

## Folder Structure

* [`notebooks`](./notebooks): _Folder containing Jupyter notebooks to process step-by-step_
* [`scripts`](./scripts): _Folder with Python scripts (could serve as usage documentation)_
* [`src/pct`](./src/pct): _Folder for all source files specific to this project_
   * [`utils`](./src/boa/utils) _Utility functions_


## Installation 

This code has been tested with `Python >= 3.9` on `MacOS`. To use this code in development mode simply clone the repository and install the dependencies.

1. Clone this repository:
    ```bash
    git clone https://github.com/FallBosk/PointCloud_Tiling.git
    cd PointCloud_Tiling
    ```

2. Create the environment `my_env` and install the dependencies (can also use conda):
    ```bash
    python -m venv my_env
    source my_env/bin/activate
    python -m pip install -r requirements.txt
    ```

3. **Finally** (if you would like to use the subsampling feature), install `cccorelib` and `pycc` into the `my_env` environment by following the [instructions on their GitHub page](https://github.com/tmontaigu/CloudCompare-PythonPlugin/blob/master/docs/building.rst#building-as-independent-wheels). Please note, these two packages are not available on the Python Package Index (PyPi).

    **Note:** installing these packages is known to cause issues. For help and questions please consult the [issue list](https://github.com/tmontaigu/CloudCompare-PythonPlugin/issues) on the original repository. Building these packages requires Qt

## Usage
There are two ways for using this repository. Option 1 is simply running the complete pipeline using the provided bash script in [scripts](scripts). Option 2 is using the provide tutorial [notebooks](notebooks) that demonstrate how the code and tools can be used.

**Option 1: using command line**

```bash
cd scripts
python pipeline.py --in_folder <input_directory> --out_folder <output_directory>
```

**Option 2: using Jupyter notebooks**

Check out the [notebooks](notebooks) that demonstrate how the tools can be used.
 

## Contributing

Contributions to enhance the functionality or efficiency of this tool are welcome. Please fork the repository and submit a pull request with your changes.


## Acknowledgements

We extend our gratitude to the Amsterdam AI Team for their influential work on the [Urban_PointCloud_Processing](https://github.com/Amsterdam-AI-Team/Urban_PointCloud_Processing) repository (check it out!). Their innovative approaches to handling urban point cloud data have significantly inspired the methodologies implemented in our project. This acknowledgment serves to recognize their pivotal contributions to the field of point cloud processing, which have guided and enriched our own developments.

## License

This project is licensed under the terms of the GPL-3.0 liscense - see the [LICENSE](./LICENSE) file for details.
