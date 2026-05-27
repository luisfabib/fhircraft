
## Requirements

Fhircraft requires a recent version of [Python](https://www.python.org/) (3.11 or higher) and a Python package manager (e.g., [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)) to be installed on your system.

!!! note "Internet Connection (optional)"

    Fhircraft works completely offline. An internet connection is only needed if you want to dynamically download external FHIR resources and definitions at runtime.


!!! tip "Pydantic Knowledge"

    Fhircraft is built on [:simple-pydantic: Pydantic](https://docs.pydantic.dev/latest/), meaning all FHIR resource models are Pydantic models with full access to their API. This documentation assumes basic Pydantic familiarity, so we recommend reviewing the Pydantic documentation if you're new to it.  


## Installation

### Latest Release

Fhircraft is provided as a [Python package](https://pypi.org/project/fhircraft/) and can be installed with your preferred package manager of choice, ideally by using a [virtual environment](https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment). Open up a terminal and install the latest Fhircraft version with:

=== ":simple-pypi: pip"

    ```bash
    pip install fhircraft
    ```

=== ":simple-poetry: Poetry"

    ```bash
    poetry add fhircraft
    ```

=== ":material-lightning-bolt: uv"

    ```bash
    uv add fhircraft
    ```

=== ":octicons-package-16: pipenv"

    ```bash
    pipenv install fhircraft
    ```

### Development Version

Install the latest development version directly from the [GitHub repository](https://github.com/luisfabib/fhircraft):

=== ":simple-pypi: pip"

    ```bash
    pip install git+https://github.com/luisfabib/fhircraft.git
    ```

=== ":simple-poetry: Poetry"

    ```bash
    poetry add git+https://github.com/luisfabib/fhircraft.git
    ```

=== ":material-lightning-bolt: uv"

    ```bash
    uv add git+https://github.com/luisfabib/fhircraft.git
    ```

## Development installation


If you want to contribute to Fhircraft or work with a customized version:

1. Clone the Fhircraft repository
```bash
git clone https://github.com/luisfabib/fhircraft.git
cd fhircraft
```

2. Install in editable mode along with the development dependencies
```bash
pip install -e .[dev]
```

For detailed instructions on developing and contributing to Fhircraft, see the [:octicons-devices-16: Contributing Guide](../community/contributing.md).


------------