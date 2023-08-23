# edge-intelligence

This repository contains the data science work for edge-intelligence.

## Repository structure

The repository structure is based on the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/).
*Please read template documentation to understand the rationale behind the repository structure and how to use it*.

```
alcoplast-ml-models-codebase/
    ├── .gitignore
    ├── Makefile                        # Makefile with commands to automatize operations and pipelines 
    ├── README.md                       # This file.
    ├── requirements.txt                # Dependencies to be installed with pip install -r requirements.txt
    ├── setup.py                        # Python setup.py file to install alcoplast package.
    ├── data/
    │   ├── processed/                  # The final data sets for modeling.
    │   └── raw/                        # The raw data dump.
    ├── models/                         # Serialised models
    ├── notebooks/                      # Jupyter notebook used for data/model exploration and reports.
    ├── reports/                        # Exported HTML reports.
    ├── alcoplast/                      # Main source code package.
    │   ├── __init__.py
    │   └── ...
    └── scripts/                        # Stand-alone executable scripts.
        ├── test_environment.py
        ├── prepare_directories.sh
        └── ...
```

## How to use the repository

The repository operations are managed through a Makefile for automation (this is the original choice of cookiecutter).
Therefore, it requires `make` to run (otherwise, one can run single python scripts as defined in the Makefile).

### Set up the environment

In order to set up the environment, use
```bash
make create_environment
```
The command will create a virtual environment based on `python3`.
The environment will be either a `conda env` or a standard Python `venv` depending on whether conda is available.
Conda is use preferentially.
The code requires a Python version `>=3.8` to work.

After activating the environment as suggested, use
```bash
make requirements
```
to create any missing directory implied by the repository structure and to install dependencies.

### Get the data

### Preprocess data
Data preprocessing build the *model-ready* dataset with timestamp, sensors data, process state, and target for both classification and regression tasks.\\
To obtain data run the **process_data.py** script:
```bash
python3 ./scripts/process_data.py -i <path/to/input/data.csv> -o <path/to/output/processed.csv>
```
or simply run `make process_data` (**Recommended**)

This script uses *../data/raw/streaming_dataset_target.csv* as default data source and save results in *../data/processed/pivoted_data.csv* so it is recommended to use the same csv names (**-i ./data/raw/streaming_dataset_target.csv**, **-o ./data/processed/pivoted_data.csv** for output) for notebooks compatibility (run `python3 scripts/process_data.py --help` for more information).

| **Script flags**     | **Type** | **Default value**                        | **Description**                                                                  |
|----------------------|----------|------------------------------------------|----------------------------------------------------------------------------------|
| -h, --help           |          |                                          | show help message and exit                                                       |
| -i , --input-dir     | string   | ../data/raw/streaming_dataset_target.csv | path (including filename) containing data to be processed                                                     |
| -o , --out-dir       | string   | ../data/processed/pivoted_data.csv       | path (including filename) where to save preprocessed data                                            |
| -s , --seed          | int      | 1234                                     | seed for reproducibility                                                         |
| -v , --verbose       | bool     | True                                     | print status                                                                     |
| -a , --save-all      | bool     | False                                    | save all processed dataset                                                       |
| -an , --anomaly-data | string   | ""                                       | data with anomaly path (including filename), if provided uses this dataset to build pivoted data |

Now you can also split dataset into $n$ sub-dataset with the `create_splitted_dataset.py` script. Run `python3 ./scripts/create_splitted_dataset.py --help` for more informations.
Naming conventions for generated data: *i.csv* $\forall i \in [0,n) \subset \N$
Example usage
```bash
python scripts/create_splitted_datasets.py -i data/processed/data_with_anomalies.csv -o data/processed/splitted -n 6
```
or simply run `make splitted`(*Note: it splits into 6 sub-dataset*)


### Model creation

### Export models
Models are served using mlflow api. To export models in mlflow format use the script **export_models.py** in the **scripts** folder.
To export a model use the following syntax (run `python3 scripts/export_models.py --help` for more information):
```bash
python3 ./scripts/export_models.py -m <choiced_model> -p <path/to/output/folder/> -j <path/to/optional/json/model/parameters.json>
```

| **Script flags**   | **Type** | **Default** | **Choices**                                          | **Description**                               | **Required** |
|--------------------|----------|-------------|------------------------------------------------------|-----------------------------------------------|--------------|
| -h, --help         |          |             |                                                      | show help message and exit                    |              |
| -m , --model       | string   |             | axgboost_bin, adaptive_random_forest, hoeffding_tree | model to be exported                          | False        |
| -p , --path        | string   |             |                                                      | dir path prefix where to export mlflow folder | True         |
| -j , --json-params | string   |             |                                                      | path to model json parameters                 | False        |
| -a, --build-all    | bool     | True        |                                                      | If used build all possible models             | False        |
| -c, --use-conda    | bool     | False       |                                                      | if used use conda env on model exporting      | False        |

*Example usage:*
**Build all models**
```bash
python3 ./scripts/export_models.py -p ./models/<mlflow_models_folder_name> -j ./models/json_params/params.json --build-all
```
This will output in a folder inside the ./models/ folder named using the following convention: **<mlflow_models_folder_name>_YYYYMMDD-HHSSmm**. Inside this last folder 3 folders will be created containing all necessary files to serve it as an MLFlow model (*MLFlow verision* = **1.26.1**).

**Build axgboost model**
```bash
python3 ./scripts/export_models.py -p ./models/<mlflow_models_folder_name> -j ./models/json_params/axgboost.json -m axgboost_bin
```
Same as before but the output folder contains only axgboost mlflow model.

**JSON Example**:
```json
{
    "axgboost_bin": {
        "n_models": 5,
        "max_window_size": 100,
        "min_window_size": 1,
        "detect_drift": false,
        "update_strategy": "replace"
    },
    "adaptive_random_forest": {
        "n_models": 10,
        "max_depth": 7
    },
    "hoeffding_tree": {
        "max_depth": 8
    }
}
```
This json can be used to build all models

You can also export all models with default values running `make export_default_models`.

### Testing exported models
Run the exported model using mlflow **1.26.1**:
```bash
mlflow models serve -m ./models/<mlflow_models_folder_name>_YYYYDDMM-HHmmss/<choiced_model> -p 5000 --env-manager=local
```
Open a new terminal and curl the app:
```bash
curl http://127.0.0.1:5000/invocations -H 'Content-Type: application/json; format=pandas-records' -d '[{"quantity": "0", "value":209, "state": 1, "label": 1}]'
```
You can also use the **test_mlflow_models.sh** script to test if it is working:
```bash
chmod +x scripts/test_mlflow_models.sh
sh scripts/test_mlflow_models.sh -p 5000
```
*Note:* -p flag is **not optional**, you must specify the port you want to ping **in localhost (127.0.0.1)**

### Using Docker: version 20.10.20, build 9fdeb9c
In *scripts* folder is provided the **build_docker_images.sh** file. Once you have exported MlFlow models it is possible to build docker images using this script.

| **Flag** | **Default**       | **Description**                                                                           | **Required** |
|----------|-------------------|-------------------------------------------------------------------------------------------|--------------|
| -m       |                   | directory path containint ONLY MlFlow generated models directories to build docker images | True         |
| -d       |                   | directory path containing Dockerfile                                                      | True         |
| -s       | ./                | Optional directory path containing setup.py.                                              | False        |
| -e       | ./                | Optional directory path containing edgeintelligence package                               | False        |
| -f       | Dockerfile.python | Optional Dockerfile name (opts: "Dockerfile.python", "Dockerfile.conda")                  | False        |

To display help message just run `sh scripts/build_docker_images.sh`
*Note*: -m flag shoul contain the output folder of the previously described **export_models.py** program.

**Example usage**
```bash
chmod +x scripts/build_docker_images.sh
sh scripts/build_docker_images.sh -m models/<output-of-export-models.py> -d docker -s ./ -e ./
docker run --rm -it -p 5000:5000 axgboost_bin:river
sh scripts/test_mlflow_models.sh -p 5000
```

*Using conda*
To use Docker image with base *continuumio/miniconda3 just add -f flag to the script with Dockerfile.conda as parameter:
```bash
sh scripts/build_docker_images.sh -m models/<output-of-export-models.py> -d docker -s ./ -e ./ -f Dockerfile.conda
```
*Note*: you must export mlflow models using **--use-conda** flag to build docker images like this.

If models are exported using the **make command**, you can build docker images also running `make conda_image` or `make python_image`

### Using monitor
In **scripts** folder is provided the **monitoring_stack** folder. Inside there are 2 main scripts: *generator.py* and *monitor.py*.
Use *generator.py* to make call the *invocations* api of mlflow models (127.0.0.1:5000/invocations) and save results on a csv file that can be accessed from *monitor.py* script. Once the *generator.py* is started it require a user input to start calling the api and save the result. Before this you must open the monitor.

**The *monitor.py* scripts takes the following input arguments:**

| **Flag**               | **Type**  | **Default** | **Description**                    | **Required** |
|------------------------|-----------|-------------|------------------------------------|--------------|
| None (positional)      | str       |             | csv path to monitor                | True         |
| -dc, --data-columns    | List[str] |             | list of data columns to monitor    | True         |
| -mc, --metrics-columns | List[str] |             | list of metrics columns to monitor | True         |
| -d, --dim              | int       | 1000        | buffer dimension                   | False        |
| -u, --update-time      | int       | 1000        | plot update time in milliseconds   | False        |

**The *generator.py* scripts takes the following input arguments:**

| **Flag**               | **Type**  | **Default** | **Description**                            | **Required** |
|------------------------|-----------|-------------|--------------------------------------------|--------------|
| -ho, --host            | str       | 127.0.0.1   | mlflow host                                | False        |
| -p, --port             | int       | 5000        | mlflow port                                | False        |
| -o, --output-file      | str       | results     | output file name prefix (csv will be added)| False        |

**Example usage:**
```bash
# bash 1
python3 scripts/monitoring_stack/generator.py --output-file prova

# bash 2
python3 scripts/monitoring_stack/monitor.py <path/to/file.csv> -dc 3 5 -mc f1s pre rec acc

# bash 1 -> hit enter
```

<img src="./imgs/monitor-generator-usage.gif" alt="Monitor Usage" width="600"/>

*Note*: the csv file must have the header row and it must contain -dc and -mc columns.