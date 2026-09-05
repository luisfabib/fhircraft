import importlib.util
import os
import sys
import tempfile
import uuid

import pytest
from pydantic import BaseModel, Field

from fhircraft.fhir.resources.generator.core import CodeGenerator


@pytest.fixture
def generator():
    return CodeGenerator()


def _make_person_and_address_models():
    """A two-class hierarchy: Person has a field of a distinct custom model type."""

    class Address(BaseModel):
        """A postal address."""

        city: str = Field(description="City name")

    class Person(BaseModel):
        """A person with a home address."""

        name: str = Field(description="Full name")
        address: Address = Field(description="Home address")

    return Person, Address


def _load_package(directory: str):
    """Import the package at `directory` (its `__init__.py`) under a unique name."""

    pkg_name = f"_generated_test_pkg_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(
        pkg_name,
        os.path.join(directory, "__init__.py"),
        submodule_search_locations=[directory],
    )
    assert spec, "Failed to create module spec"
    assert spec.loader, "Failed to create module spec loader"
    module = importlib.util.module_from_spec(spec)
    sys.modules[pkg_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        del sys.modules[pkg_name]


# ----------------------------------------
# CodeGenerator.generate_source()
# ----------------------------------------


def test_generate_source__single_model_returns_source_string(generator):
    Person, _ = _make_person_and_address_models()

    source = generator.generate_source(Person)

    assert "class Person(BaseModel):" in source
    assert "name: str = Field(" in source


def test_generate_source__includes_transitively_referenced_models(generator):
    Person, Address = _make_person_and_address_models()

    source = generator.generate_source(Person)

    assert "class Address(BaseModel):" in source
    assert "class Person(BaseModel):" in source


def test_generate_source__accepts_list_of_resources(generator):
    Person, Address = _make_person_and_address_models()

    source = generator.generate_source([Person, Address])

    assert "class Person(BaseModel):" in source
    assert "class Address(BaseModel):" in source


def test_generate_source__is_stateless_across_calls(generator):
    Person, Address = _make_person_and_address_models()

    generator.generate_source(Person)
    second_source = generator.generate_source(Address)

    # A second, independent call should not carry over models from the first call.
    assert "class Person" not in second_source
    assert "class Address(BaseModel):" in second_source


# ----------------------------------------
# CodeGenerator.generate_files()
# ----------------------------------------


def test_generate_files__split_false_returns_single_module_and_init(generator):
    Person, Address = _make_person_and_address_models()

    files = generator.generate_files(Person, split=False)

    assert set(files.keys()) == {"models.py", "__init__.py"}
    assert "class Person(BaseModel):" in files["models.py"]
    assert "class Address(BaseModel):" in files["models.py"]
    assert "from .models import Person" in files["__init__.py"]
    assert "from .models import Address" in files["__init__.py"]


def test_generate_files__split_true_creates_one_file_per_model(generator):
    Person, Address = _make_person_and_address_models()

    files = generator.generate_files(Person, split=True)

    assert set(files.keys()) == {"person.py", "address.py", "__init__.py"}
    assert "class Person(BaseModel):" in files["person.py"]
    assert "class Address(BaseModel):" not in files["person.py"]
    assert "class Address(BaseModel):" in files["address.py"]


def test_generate_files__split_true_adds_cross_file_import(generator):
    Person, _ = _make_person_and_address_models()

    files = generator.generate_files(Person, split=True)

    assert "from .address import Address" in files["person.py"]


def test_generate_files__split_true_init_exports_all_models(generator):
    Person, _ = _make_person_and_address_models()

    files = generator.generate_files(Person, split=True)

    assert "from .person import Person" in files["__init__.py"]
    assert "from .address import Address" in files["__init__.py"]
    assert '"Person"' in files["__init__.py"]
    assert '"Address"' in files["__init__.py"]


def test_generate_files__split_true_raises_on_filename_collision(generator):
    # "ABTest" and "AbTest" both collapse to the same snake_case module name.
    class ABTest(BaseModel):
        value: int = 0

    class AbTest(BaseModel):
        value: str = ""

    with pytest.raises(ValueError, match="collision"):
        generator.generate_files([ABTest, AbTest], split=True)


# ----------------------------------------
# CodeGenerator.generate()
# ----------------------------------------


def test_generate__split_true_writes_importable_package_to_disk(generator):
    Person, Address = _make_person_and_address_models()

    with tempfile.TemporaryDirectory() as output_dir:
        written_paths = generator.generate(Person, output_dir, split=True)

        assert set(os.path.basename(p) for p in written_paths) == {
            "person.py",
            "address.py",
            "__init__.py",
        }
        assert all(os.path.isabs(p) and os.path.isfile(p) for p in written_paths)

        package = _load_package(output_dir)
        assert package.Person.model_fields["name"].description == "Full name"
        instance = package.Person(name="Ada", address=package.Address(city="Paris"))
        assert instance.address.city == "Paris"


def test_generate__split_false_writes_importable_package_to_disk(generator):
    Person, Address = _make_person_and_address_models()

    with tempfile.TemporaryDirectory() as output_dir:
        written_paths = generator.generate(Person, output_dir, split=False)

        assert set(os.path.basename(p) for p in written_paths) == {
            "models.py",
            "__init__.py",
        }

        package = _load_package(output_dir)
        instance = package.Person(name="Ada", address=package.Address(city="Paris"))
        assert instance.address.city == "Paris"


def test_generate__creates_output_dir_if_missing(generator):
    Person, _ = _make_person_and_address_models()

    with tempfile.TemporaryDirectory() as base_dir:
        output_dir = os.path.join(base_dir, "nested", "package")

        generator.generate(Person, output_dir, split=False)

        assert os.path.isdir(output_dir)
        assert os.path.isfile(os.path.join(output_dir, "models.py"))


def test_generate__exist_ok_false_raises_if_directory_exists(generator):
    Person, _ = _make_person_and_address_models()

    with tempfile.TemporaryDirectory() as output_dir:
        with pytest.raises(FileExistsError):
            generator.generate(Person, output_dir, split=False, exist_ok=False)
