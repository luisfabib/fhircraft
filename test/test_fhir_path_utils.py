from  fhircraft.fhir.path.utils import split_fhirpath, join_fhirpath

class Test_SplitFhirPath:

    def test_split_simple_paths(self):
        result = split_fhirpath("patient.name.family")
        assert result == ["patient", "name", "family"]

    def test_handle_multiple_segments(self):
        result = split_fhirpath("patient.name.family.given")
        assert result == ["patient", "name", "family", "given"]

    def test_return_list_of_segments(self):
        result = split_fhirpath("patient.name.family")
        assert isinstance(result, list)

    def test_handle_nested_functions(self):
        result = split_fhirpath("patient.name.family.where(family='Smith').given")
        assert result == ["patient", "name", "family", "where(family='Smith')", "given"]

    def test_split_paths_with_dots_in_quotes(self):
        result = split_fhirpath("patient.name.family.where(family='Smith.Jones').given")
        assert result == ["patient", "name", "family", "where(family='Smith.Jones')", "given"]

    def test_empty_input_returns_empty_list(self):
        result = split_fhirpath("")
        assert result == ['']
        

class Test_JoinFhirPath:

    def test_split_simple_paths(self):
        result = join_fhirpath("patient", "name", "family")
        assert result == "patient.name.family"

    def test_return_string(self):
        result = join_fhirpath("patient", "name", "family")
        assert isinstance(result, str)

    def test_handle_nested_functions(self):
        result = join_fhirpath("patient", "name", "family", "where(family='Smith')", "given")
        assert result == "patient.name.family.where(family='Smith').given"

    def test_handle_paths_with_empty_segments(self):
        result = join_fhirpath("patient", "name", "", "family",  "", "where(family='Smith.Jones')", "given")
        assert result == "patient.name.family.where(family='Smith.Jones').given"

    def test_handle_paths_with_dots_in_quotes(self):
        result = join_fhirpath("patient", "name", "family", "where(family='Smith.Jones')", "given")
        assert result == "patient.name.family.where(family='Smith.Jones').given"

    def test_handle_segments_with_spurious_dots(self):
        result = join_fhirpath("patient.", "...name", ".family", ".where(family='Smith').", ".given")
        assert result == "patient.name.family.where(family='Smith').given"
        
