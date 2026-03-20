import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.core import MappingScope
from fhircraft.fhir.mapper.engine.exceptions import MappingError
from fhircraft.fhir.path.engine.core import Element


# ===========================================================================
# Helpers
# ===========================================================================


class MockBaseModel(BaseModel):
    """Mock BaseModel for testing"""

    name: str
    value: int = 0


class AnotherMockModel(BaseModel):
    """Another mock model for testing"""

    id: str
    active: bool = True


# ===========================================================================
# MappingScope.__init__
# ===========================================================================


def test_scope__init__basic():
    """Test basic initialization of MappingScope"""
    scope = MappingScope(name="test_scope")

    assert scope.name == "test_scope"
    assert scope.types == {}
    assert scope.source_instances == {}
    assert scope.target_instances == {}
    assert scope.variables == {}
    assert scope.processing_rules == set()
    assert scope.parent is None


def test_scope__init__with_parent():
    """Test initialization with parent scope"""
    parent = MappingScope(name="parent")
    child = MappingScope(name="child", parent=parent)

    assert child.parent == parent
    assert child.name == "child"


def test_scope__init__with_data():
    """Test initialization with initial data"""
    types = {"Patient": MockBaseModel}
    source_instances = {"src1": MockBaseModel(name="test", value=1)}
    target_instances = {"tgt1": MockBaseModel(name="target", value=2)}
    variables = {"var1": Element("test")}
    processing_rules = {"rule1", "rule2"}

    scope = MappingScope(
        name="test",
        types=types,  # type: ignore
        source_instances=source_instances,  # type: ignore
        target_instances=target_instances,  # type: ignore
        variables=variables,  # type: ignore
        processing_rules=processing_rules,
    )

    assert scope.types == types
    assert scope.source_instances == source_instances
    assert scope.target_instances == target_instances
    assert scope.variables == variables
    assert scope.processing_rules == processing_rules


def test_scope__tracking_rule_processing():
    scope = MappingScope(name="test")

    # Initially no rules are being processed
    assert not scope.is_processing_rule("rule1")
    assert scope.processing_rules == set()

    # Start processing a rule
    scope.start_processing_rule("rule1")
    assert scope.is_processing_rule("rule1")
    assert "rule1" in scope.processing_rules

    # Start processing another rule
    scope.start_processing_rule("rule2")
    assert scope.is_processing_rule("rule1")
    assert scope.is_processing_rule("rule2")
    assert scope.processing_rules == {"rule1", "rule2"}

    # Finish processing a rule
    scope.finish_processing_rule("rule1")
    assert not scope.is_processing_rule("rule1")
    assert scope.is_processing_rule("rule2")
    assert scope.processing_rules == {"rule2"}

    # Finish processing the last rule
    scope.finish_processing_rule("rule2")
    assert not scope.is_processing_rule("rule2")
    assert scope.processing_rules == set()


def test_scope__finish_processing_nonexistent_rule():
    scope = MappingScope(name="test")

    # This should not raise an error
    scope.finish_processing_rule("nonexistent_rule")
    assert scope.processing_rules == set()


def test_scope__circular_detection():
    scope = MappingScope(name="test")

    # Simulate processing rules with potential cycle
    scope.start_processing_rule("rule_a")
    scope.start_processing_rule("rule_b")

    # rule_b tries to call rule_a (cycle detected)
    assert scope.is_processing_rule("rule_a")

    # Finish processing in reverse order
    scope.finish_processing_rule("rule_b")
    scope.finish_processing_rule("rule_a")

    assert scope.processing_rules == set()


# ===========================================================================
# MappingScope.resolve_symbol
# ===========================================================================


def test_scope__resolve_symbol__local_variable():
    fhirpath = Element("test_element")
    scope = MappingScope(name="test", variables={"test_var": fhirpath})
    assert scope.resolve_symbol("test_var") == fhirpath


def test_scope__resolve_symbol__local_type():
    scope = MappingScope(name="test", types={"Patient": MockBaseModel})
    assert scope.resolve_symbol("Patient") == MockBaseModel


def test_scope__resolve_symbol__parent_scope():
    fhir_path = Element("parent_element")
    parent = MappingScope(name="parent", variables={"parent_var": fhir_path})
    child = MappingScope(name="child", parent=parent)
    assert child.resolve_symbol("parent_var") == fhir_path


def test_scope__resolve_symbol__raises_error_when_not_found():
    scope = MappingScope(name="test")
    with pytest.raises(MappingError):
        scope.resolve_symbol("nonexistent")


def test_scope__resolve_symbol__multiple_variables():
    scope = MappingScope(
        name="test",
        variables={
            "var1": Element("elem1"),
            "var2": Element("elem2"),
            "var3": Element("elem3"),
        },
    )
    assert scope.resolve_symbol("var1") == Element("elem1")
    assert scope.resolve_symbol("var2") == Element("elem2")
    assert scope.resolve_symbol("var3") == Element("elem3")


def test_scope__resolve_symbol__child_overrides_parent_variable():
    parent_path = Element("parent_element")
    child_path = Element("child_element")
    parent = MappingScope(name="parent", variables={"shared": parent_path})
    child = MappingScope(name="child", parent=parent, variables={"shared": child_path})

    assert child.resolve_symbol("shared") == child_path
    assert child.resolve_symbol("shared") != parent_path
    assert parent.resolve_symbol("shared") == parent_path


def test_scope__resolve_symbol__complex_hierarchy():
    global_scope = MappingScope(
        name="global",
        variables={"global_var": Element("global")},
        types={"GlobalType": MockBaseModel},
    )

    group_scope = MappingScope(
        name="group",
        parent=global_scope,
        variables={"group_var": Element("group")},
        types={"GroupType": AnotherMockModel},
    )

    rule_scope = MappingScope(
        name="rule", parent=group_scope, variables={"rule_var": Element("rule")}
    )

    # Test lookups from deepest scope
    assert rule_scope.resolve_symbol("global_var") == Element("global")
    assert rule_scope.resolve_symbol("group_var") == Element("group")
    assert rule_scope.resolve_symbol("rule_var") == Element("rule")
    assert rule_scope.resolve_symbol("GlobalType") == MockBaseModel
    assert rule_scope.resolve_symbol("GroupType") == AnotherMockModel

    # Test path
    assert rule_scope.get_scope_path() == ["global", "group", "rule"]

    # Test all symbols - should include variables from all scopes but only variables for backward compatibility
    all_symbols = rule_scope.get_all_visible_symbols()
    assert (
        len(all_symbols) >= 3
    )  # At least the 3 variables, may include types and groups
    assert "global_var" in all_symbols
    assert "group_var" in all_symbols
    assert "rule_var" in all_symbols


def test_scope__resolve_symbol__check_sibling_scopes_are_isolated():
    parent = MappingScope(
        name="parent", variables={"shared_var": Element("parent_shared")}
    )

    child1 = MappingScope(
        name="child1", parent=parent, variables={"child1_var": Element("child1_shared")}
    )
    child2 = MappingScope(
        name="child2", parent=parent, variables={"child2_var": Element("child2_shared")}
    )

    # Each child can see parent but not sibling
    assert child1.resolve_symbol("shared_var")
    assert child1.resolve_symbol("child1_var")
    with pytest.raises(MappingError):
        child1.resolve_symbol("child2_var")

    assert child2.resolve_symbol("shared_var")
    assert child2.resolve_symbol("child2_var")
    with pytest.raises(MappingError):
        child2.resolve_symbol("child1_var")


def test_scope__resolve_symbol__nested_symbol_resolution():
    root = MappingScope(
        name="root",
        variables={"root_var": Element("root")},
        types={"RootType": MockBaseModel},
    )

    middle = MappingScope(
        name="middle",
        parent=root,
        variables={"middle_var": Element("middle")},
        types={"MiddleType": AnotherMockModel},
    )

    leaf = MappingScope(
        name="leaf", parent=middle, variables={"leaf_var": Element("leaf")}
    )

    # Test that fixture is properly set up
    assert root.name == "root"
    assert middle.parent == root
    assert leaf.parent == middle

    # Test lookups work correctly
    assert leaf.resolve_symbol("root_var")
    assert leaf.resolve_symbol("middle_var")
    assert leaf.resolve_symbol("leaf_var")

    assert leaf.resolve_symbol("RootType") == MockBaseModel
    assert leaf.resolve_symbol("MiddleType") == AnotherMockModel


# ===========================================================================
# MappingScope.define_variable
# ===========================================================================


def test_scope__define_variable__basic():
    scope = MappingScope(name="test")
    fhir_path = Element("test_element")

    scope.define_variable("test_var", fhir_path)

    assert "test_var" in scope.variables
    assert scope.variables["test_var"] == fhir_path


def test_scope__define_variable__raises_error_for_non_fhirpath():
    scope = MappingScope(name="test")

    with pytest.raises(ValueError, match="FHIRPath"):
        scope.define_variable("test_var", "not_a_fhir_path")  # type: ignore


# ===========================================================================
# MappingScope.get_all_visible_symbols
# ===========================================================================


def test_scope__get_all_symbols__no_parent_scope():
    var = Element("test_element")
    scope = MappingScope(name="test", variables={"test_var": var})

    assert scope.get_all_visible_symbols() == {"test_var": var}


def test_scope__get_all_symbols__returns_all_including_inherited():
    parent_var = Element("parent_element")
    child_var = Element("child_element")
    override_var = Element("override_element")

    parent = MappingScope(
        name="parent",
        variables={"parent_var": parent_var, "shared_var": Element("parent_shared")},
    )
    child = MappingScope(
        name="child",
        parent=parent,
        variables={"child_var": child_var, "shared_var": override_var},
    )

    all_symbols = child.get_all_visible_symbols()

    assert "parent_var" in all_symbols
    assert "child_var" in all_symbols
    assert "shared_var" in all_symbols
    assert all_symbols["parent_var"] == parent_var
    assert all_symbols["child_var"] == child_var
    assert all_symbols["shared_var"] == override_var


# ===========================================================================
# MappingScope.has_symbol
# ===========================================================================


def test_scope__exists_local():
    """Test checking if identifier exists in current scope"""
    scope = MappingScope(name="test")
    scope.variables["test_var"] = Element("test")
    scope.types["TestType"] = MockBaseModel

    assert scope.has_symbol("test_var")
    assert scope.has_symbol("TestType")
    assert not scope.has_symbol("nonexistent")


def test_scope__exists_with_parent():
    """Test checking existence across scope hierarchy"""
    parent = MappingScope(name="parent")
    parent.variables["parent_var"] = Element("test")

    child = MappingScope(name="child", parent=parent)
    child.variables["child_var"] = Element("test")

    assert child.has_symbol("parent_var")
    assert child.has_symbol("child_var")
    assert not parent.has_symbol("child_var")


def test_scope__exists_local_only():
    """Test checking existence only in current scope"""
    parent = MappingScope(name="parent")
    parent.variables["parent_var"] = Element("test")

    child = MappingScope(name="child", parent=parent)
    child.variables["child_var"] = Element("test")
    child.types["ChildType"] = MockBaseModel

    assert child.has_local_symbol("child_var")
    assert child.has_local_symbol("ChildType")
    assert not child.has_local_symbol("parent_var")


# ===========================================================================
# MappingScope.get_scope_path
# ===========================================================================


def test_scope__get_scope_path__single_scope():
    """Test getting path for single scope"""
    scope = MappingScope(name="root")

    assert scope.get_scope_path() == ["root"]


def test_scope__get_scope_path__nested_scopes():
    """Test getting path for nested scopes"""
    root = MappingScope(name="root")
    middle = MappingScope(name="middle", parent=root)
    leaf = MappingScope(name="leaf", parent=middle)

    assert leaf.get_scope_path() == ["root", "middle", "leaf"]


# ===========================================================================
# MappingScope.resolve_group
# ===========================================================================


def _make_group_def(name: str):
    """Make a minimal StructureMapGroup definition."""
    from fhircraft.fhir.resources.datatypes.R5.core.structure_map import (
        StructureMapGroup,
        StructureMapGroupInput,
    )

    return StructureMapGroup(
        name=name,
        typeMode="none",
        input=[
            StructureMapGroupInput(name="src", mode="source"),
            StructureMapGroupInput(name="tgt", mode="target"),
        ],
    )


def _make_structure_map(url: str, group_names):
    """Make a minimal StructureMap with the given group names."""
    from fhircraft.fhir.resources.datatypes.R5.core.structure_map import StructureMap

    return StructureMap(
        url=url,
        name=url.split("/")[-1],
        status="active",
        group=[_make_group_def(n) for n in group_names],
    )


def test_resolve_group__finds_local_group():
    from fhircraft.fhir.mapper.engine.group import Group

    group = Group(_make_group_def("Local"))
    scope = MappingScope(name="test")
    scope.groups["Local"] = group
    assert scope.resolve_group("Local") is group


def test_resolve_group__finds_group_in_parent_scope():
    from fhircraft.fhir.mapper.engine.group import Group

    group = Group(_make_group_def("ParentGroup"))
    parent = MappingScope(name="parent")
    parent.groups["ParentGroup"] = group
    child = MappingScope(name="child", parent=parent)
    assert child.resolve_group("ParentGroup") is group


def test_resolve_group__finds_group_in_imported_map():
    from fhircraft.fhir.mapper.engine.group import Group

    sm = _make_structure_map("http://example.org/Map", ["ImportedGroup"])
    scope = MappingScope(name="test")
    scope.imported_maps = [sm]
    result = scope.resolve_group("ImportedGroup")
    assert isinstance(result, Group)
    assert str(result.name) == "ImportedGroup"


def test_resolve_group__prefers_local_over_imported():
    from fhircraft.fhir.mapper.engine.group import Group

    local = Group(_make_group_def("Shared"))
    sm = _make_structure_map("http://example.org/Map", ["Shared"])
    scope = MappingScope(name="test")
    scope.groups["Shared"] = local
    scope.imported_maps = [sm]
    assert scope.resolve_group("Shared") is local


def test_resolve_group__raises_when_not_found():
    scope = MappingScope(name="test")
    with pytest.raises(MappingError, match="NonExistent"):
        scope.resolve_group("NonExistent")


def test_resolve_group__raises_on_ambiguous_imported_group():
    sm1 = _make_structure_map("http://example.org/Map1", ["Shared"])
    sm2 = _make_structure_map("http://example.org/Map2", ["Shared"])
    scope = MappingScope(name="test")
    scope.imported_maps = [sm1, sm2]
    with pytest.raises(MappingError, match="Ambiguous"):
        scope.resolve_group("Shared")


def test_resolve_group__child_scope_searches_parent_imported_maps():
    """imported_maps on the parent scope are visible when resolving from a child."""
    from fhircraft.fhir.mapper.engine.group import Group

    sm = _make_structure_map("http://example.org/Map", ["ImportedGroup"])
    parent = MappingScope(name="parent")
    parent.imported_maps = [sm]
    child = MappingScope(name="child", parent=parent)
    result = child.resolve_group("ImportedGroup")
    assert isinstance(result, Group)


# ===========================================================================
# MappingScope.__str__ and __repr__
# ===========================================================================


def test_scope__str():
    """Test string representation of scope"""
    scope = MappingScope(name="test_scope")
    scope.define_variable("var1", Element("test"))
    scope.types["Type1"] = MockBaseModel

    str_repr = str(scope)

    assert "test_scope" in str_repr
    assert "var1" in str_repr
    assert "Type1" in str_repr


def test_scope__repr():
    """Test repr representation of scope"""
    parent = MappingScope(name="parent")
    child = MappingScope(name="child", parent=parent)
    child.define_variable("test_var", Element("test"))
    child.types["TestType"] = MockBaseModel

    repr_str = repr(child)

    assert "name='child'" in repr_str
    assert "parent=parent" in repr_str
    assert "test_var" in repr_str
    assert "TestType" in repr_str


def test_scope__repr_with_no_parent():
    scope = MappingScope(name="root")
    repr_str = repr(scope)
    assert "parent=None" in repr_str
