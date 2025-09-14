import pytest
from pydantic import BaseModel

from fhircraft.fhir.mapper.engine.core import MappingScope
from fhircraft.fhir.mapper.engine.exceptions import MappingError
from fhircraft.fhir.path.engine.core import Element


class MockBaseModel(BaseModel):
    """Mock BaseModel for testing"""

    name: str
    value: int = 0


class AnotherMockModel(BaseModel):
    """Another mock model for testing"""

    id: str
    active: bool = True


class TestMappingScope:
    """Test cases for MappingScope class"""

    def test_init_basic(self):
        """Test basic initialization of MappingScope"""
        scope = MappingScope(name="test_scope")

        assert scope.name == "test_scope"
        assert scope.types == {}
        assert scope.source_instances == {}
        assert scope.target_instances == {}
        assert scope.variables == {}
        assert scope.processing_rules == set()
        assert scope.parent is None

    def test_init_with_parent(self):
        """Test initialization with parent scope"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        assert child.parent == parent
        assert child.name == "child"

    def test_init_with_data(self):
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

    def test_define_variable(self):
        """Test defining variables in scope"""
        scope = MappingScope(name="test")
        fhir_path = Element("test_element")

        scope.define_variable("test_var", fhir_path)

        assert "test_var" in scope.variables
        assert scope.variables["test_var"] == fhir_path

    def test_lookup_local_variable(self):
        """Test looking up variables in local scope"""
        scope = MappingScope(name="test")
        fhir_path = Element("test_element")
        scope.define_variable("test_var", fhir_path)

        result = scope.resolve_symbol("test_var")

        assert result == fhir_path

    def test_lookup_local_type(self):
        """Test looking up types in local scope"""
        scope = MappingScope(name="test", types={"Patient": MockBaseModel})

        result = scope.resolve_symbol("Patient")

        assert result == MockBaseModel

    def test_lookup_parent_scope(self):
        """Test looking up variables in parent scope"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        fhir_path = Element("parent_element")
        parent.define_variable("parent_var", fhir_path)

        result = child.resolve_symbol("parent_var")

        assert result == fhir_path

    def test_lookup_not_found(self):
        """Test looking up non-existent variable"""
        scope = MappingScope(name="test")
        with pytest.raises(MappingError):
            scope.resolve_symbol("nonexistent")

    def test_lookup_child_overrides_parent(self):
        """Test that child scope variables override parent scope"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        parent_path = Element("parent_element")
        child_path = Element("child_element")

        parent.define_variable("same_var", parent_path)
        child.define_variable("same_var", child_path)

        result = child.resolve_symbol("same_var")

        assert result == child_path
        assert result != parent_path

    def test_exists_local(self):
        """Test checking if identifier exists in current scope"""
        scope = MappingScope(name="test")
        scope.define_variable("test_var", Element("test"))
        scope.types["TestType"] = MockBaseModel

        assert scope.has_symbol("test_var")
        assert scope.has_symbol("TestType")
        assert not scope.has_symbol("nonexistent")

    def test_exists_with_parent(self):
        """Test checking existence across scope hierarchy"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        parent.define_variable("parent_var", Element("test"))
        child.define_variable("child_var", Element("test"))

        assert child.has_symbol("parent_var")
        assert child.has_symbol("child_var")
        assert not parent.has_symbol("child_var")

    def test_exists_local_only(self):
        """Test checking existence only in current scope"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        parent.define_variable("parent_var", Element("test"))
        child.define_variable("child_var", Element("test"))
        child.types["ChildType"] = MockBaseModel

        assert child.has_local_symbol("child_var")
        assert child.has_local_symbol("ChildType")
        assert not child.has_local_symbol("parent_var")

    def test_get_all_symbols(self):
        """Test getting all visible symbols including inherited ones"""
        parent = MappingScope(name="parent")
        child = MappingScope(name="child", parent=parent)

        parent_var = Element("parent_element")
        child_var = Element("child_element")
        override_var = Element("override_element")

        parent.define_variable("parent_var", parent_var)
        parent.define_variable("shared_var", Element("parent_shared"))
        child.define_variable("child_var", child_var)
        child.define_variable("shared_var", override_var)  # Override parent

        all_symbols = child.get_all_visible_symbols()

        assert "parent_var" in all_symbols
        assert "child_var" in all_symbols
        assert "shared_var" in all_symbols
        assert all_symbols["parent_var"] == parent_var
        assert all_symbols["child_var"] == child_var
        assert all_symbols["shared_var"] == override_var  # Child overrides parent

    def test_get_all_symbols_no_parent(self):
        """Test getting all symbols when no parent exists"""
        scope = MappingScope(name="test")
        var = Element("test_element")
        scope.define_variable("test_var", var)

        all_symbols = scope.get_all_visible_symbols()

        assert all_symbols == {"test_var": var}

    def test_get_path_single_scope(self):
        """Test getting path for single scope"""
        scope = MappingScope(name="root")

        path = scope.get_scope_path()

        assert path == ["root"]

    def test_get_path_nested_scopes(self):
        """Test getting path for nested scopes"""
        root = MappingScope(name="root")
        middle = MappingScope(name="middle", parent=root)
        leaf = MappingScope(name="leaf", parent=middle)

        path = leaf.get_scope_path()

        assert path == ["root", "middle", "leaf"]

    def test_rule_processing_tracking(self):
        """Test rule processing tracking functionality"""
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

    def test_finish_processing_nonexistent_rule(self):
        """Test finishing processing of a rule that wasn't being processed"""
        scope = MappingScope(name="test")

        # This should not raise an error
        scope.finish_processing_rule("nonexistent_rule")
        assert scope.processing_rules == set()

    def test_cycle_detection_scenario(self):
        """Test a typical cycle detection scenario"""
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

    def test_str_representation(self):
        """Test string representation of scope"""
        scope = MappingScope(name="test_scope")
        scope.define_variable("var1", Element("test"))
        scope.types["Type1"] = MockBaseModel

        str_repr = str(scope)

        assert "test_scope" in str_repr
        assert "var1" in str_repr
        assert "Type1" in str_repr

    def test_repr_representation(self):
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

    def test_repr_no_parent(self):
        """Test repr representation without parent"""
        scope = MappingScope(name="root")

        repr_str = repr(scope)

        assert "parent=None" in repr_str

    def test_complex_hierarchy(self):
        """Test complex scope hierarchy"""
        global_scope = MappingScope(name="global")
        global_scope.types["GlobalType"] = MockBaseModel
        global_scope.define_variable("global_var", Element("global"))

        group_scope = MappingScope(name="group", parent=global_scope)
        group_scope.types["GroupType"] = AnotherMockModel
        group_scope.define_variable("group_var", Element("group"))

        rule_scope = MappingScope(name="rule", parent=group_scope)
        rule_scope.define_variable("rule_var", Element("rule"))

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

    def test_multiple_variable_definitions(self):
        """Test defining multiple variables"""
        scope = MappingScope(name="test")

        variables = {
            "var1": Element("elem1"),
            "var2": Element("elem2"),
            "var3": Element("elem3"),
        }

        for name, value in variables.items():
            scope.define_variable(name, value)

        for name, expected_value in variables.items():
            assert scope.resolve_symbol(name) == expected_value

    def test_scope_isolation(self):
        """Test that sibling scopes are isolated from each other"""
        parent = MappingScope(name="parent")
        parent.define_variable("shared", Element("parent_shared"))

        child1 = MappingScope(name="child1", parent=parent)
        child2 = MappingScope(name="child2", parent=parent)

        child1.define_variable("child1_var", Element("child1"))
        child2.define_variable("child2_var", Element("child2"))

        # Each child can see parent but not sibling
        assert child1.resolve_symbol("shared")
        assert child1.resolve_symbol("child1_var")
        with pytest.raises(MappingError):
            child1.resolve_symbol("child2_var")

        assert child2.resolve_symbol("shared")
        assert child2.resolve_symbol("child2_var")
        with pytest.raises(MappingError):
            child2.resolve_symbol("child1_var")

    @pytest.fixture
    def sample_scope_hierarchy(self):
        """Fixture providing a sample scope hierarchy for testing"""
        root = MappingScope(name="root")
        root.types["RootType"] = MockBaseModel
        root.define_variable("root_var", Element("root"))

        middle = MappingScope(name="middle", parent=root)
        middle.types["MiddleType"] = AnotherMockModel
        middle.define_variable("middle_var", Element("middle"))

        leaf = MappingScope(name="leaf", parent=middle)
        leaf.define_variable("leaf_var", Element("leaf"))

        return root, middle, leaf

    def test_hierarchy_fixture(self, sample_scope_hierarchy):
        """Test using the sample hierarchy fixture"""
        root, middle, leaf = sample_scope_hierarchy

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
