# PCT - Point Cloud Tiling

This repository provides code to cut large-scale pointclouds into smaller usable tiles.

## Folder Structure

* [`notebooks`](./notebooks): _Folder containing Jupyter notebooks to process step-by-step_
* [`scripts`](./scripts): _Folder with Python scripts (could serve as usage documentation)_
* [`src/pct`](./src/pct): _Folder for all source files specific to this project_
   * [`utils`](./src/boa/utils) _Utility functions_


## Installation 

This code has been tested with `Python >= 3.9` on `MacOS`. To use this code in development mode simply clone the repository and install the dependencies.

1. Clone this repository:

2. Create the environment `my_env` and install the dependencies (can also use conda):
    ```bash
    python -m venv my_env
    source my_env/bin/activate
    python -m pip install -r requirements.txt
    ```

3. **Finally**, install `cccorelib` and `pycc` into the `my_env` environment by following the [instructions on their GitHub page](https://github.com/tmontaigu/CloudCompare-PythonPlugin/blob/master/docs/building.rst#building-as-independent-wheels). Please note, these two packages are not available on the Python Package Index (PyPi).

    **Note:** installing these packages is known to cause issues. For help and questions please consult the [issue list](https://github.com/tmontaigu/CloudCompare-PythonPlugin/issues) on the original repository. Building these packages requires Qt

## Usage
There are two ways for using this repository. Option 1 is simply running the complete pipeline using the provided bash script in [scripts](scripts). Option 2 is using the provide tutorial [notebooks](notebooks) that demonstrate how the code and tools can be used.

**Option 1: using command line**

```bash
cd scripts
sh run.sh
```

**Option 2: using Jupyter notebooks**

Check out the [notebooks](notebooks) that demonstrate how the tools can be used. **Note:** To produce an output, only notebook 0 - 3 is required to run. Other notebooks are optional.
 

## Contributing

Feel free to help out!


## Acknowledgements


## License

This project is licensed under the terms of the European Union Public License 1.2 (EUPL-1.2).
