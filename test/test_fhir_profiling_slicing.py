
from fhircraft.fhir.profiling import SlicingGroup, Slice, Discriminator, Constraint
from fhircraft.fhir.path import FHIRPathError
from unittest.mock import patch, MagicMock
from unittest import TestCase 
import pytest

class TestDiscriminator(TestCase):
    
    def test_discriminator_construction(self):
        obj = Discriminator(type='value', path='code')
        assert obj.type == 'value'
        assert obj.path == 'code'
    
    def test_discriminator_type_enum(self):
        with pytest.raises(ValueError):
            Discriminator(type='invalid', path='code')

    def test_discriminator_invalid_fhirpath(self):
        with pytest.raises(FHIRPathError):
            Discriminator(type='value', path='code.coding.5')

    def test_discriminator_restricted_functions(self):
        with pytest.raises(FHIRPathError):
            Discriminator(type='value', path="code.filter(coding.code='5')")
        
class TestSlicingGroup(TestCase):
    
    def test_slicing_group_construction(self):
        obj = SlicingGroup(
            id='Observation.component', 
            path='Observation.component',
            discriminators=[Discriminator(type='value', path='Observation.component.code')],
        )
        assert obj.id == 'Observation.component'
        assert obj.path == 'Observation.component'
        assert obj.rules == 'open'
        assert obj.ordered == False
        assert obj.discriminators[0].path == 'Observation.component.code'
    
    def test_slicing_group_rules_enum(self):
        with pytest.raises(ValueError):
            SlicingGroup(
                id='Observation.component', path='Observation.component',
                discriminators=[Discriminator(type='value', path='Observation.component.code')],
                rules='invalid',
            )

    def test_slicing_group_invalid_fhirpath(self):
        with pytest.raises(FHIRPathError):
            SlicingGroup(
                id='Observation.component', path='Observation.component.0',
                discriminators=[Discriminator(type='value', path='Observation.component.code')],
            )


class TestSlice(TestCase):
    
    def setUp(self):
        self.slicing = SlicingGroup(
            id='Observation.component', 
            path='Observation.component',
            discriminators=[Discriminator(type='value', path='code')],
        )
        self.slice = Slice(
            id='Observation.component:sliceName', 
            name='sliceName',
            type='BackboneElement'
        )
        self.slicing.add_slice(self.slice)
        self.constraint = Constraint(
            id='Observation.component:sliceName.code',
            path='Observation.component.code.coding.code',
            min=0,
            max=1,
        )
    
    def test_slice_construction(self):
        assert self.slice.id == 'Observation.component:sliceName'
        assert self.slice.name == 'sliceName'
        assert self.slice.type == 'BackboneElement'
    
    def test_get_constraints_on_slice(self):
        self.constraint.path = 'Observation.component'
        self.slice.add_constraint(self.constraint)
        assert self.slice.get_constraints_on_slice() == [self.constraint]
        
    def test_slice_min_cardinality(self):
        self.constraint.path = 'Observation.component'
        self.slice.add_constraint(self.constraint)
        assert self.slice.min_cardinality == 0
        
    def test_slice_discriminating_expression_pattern(self):
        pattern = MagicMock()
        self.constraint.path = 'Observation.component.code'
        pattern.dict.return_value = {'coding': [{
            'code': "123456", 
            "system": "http://system.org",
            }]
        }
        self.constraint.pattern = pattern
        self.slice.add_constraint(self.constraint)
        assert self.slice.discriminating_expression == \
            "where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"

        
    def __prepare_discriminator_pattern__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='code')]
        pattern = MagicMock()
        self.constraint.path = 'Observation.component.code'
        pattern.dict.return_value = {'coding': [{
            'code': "123456", 
            "system": "http://system.org",
            }]
        }
        self.constraint.pattern = pattern
        self.slice.add_constraint(self.constraint)

    def test_slice_discriminating_expression_pattern(self):
        self.__prepare_discriminator_pattern__()
        assert self.slice.discriminating_expression == \
            "where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"
        
    def test_slice_full_fhir_path_pattern(self):
        self.__prepare_discriminator_pattern__()
        assert self.slice.full_fhir_path == \
            "Observation.component.where(code.coding[0].code='123456').where(code.coding[0].system='http://system.org')"
        
        
        
    def __prepare_discriminator_fixed__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='valueString')]
        self.constraint.path = 'Observation.component.valueString'
        self.constraint.fixedValue = 'myString'
        self.slice.add_constraint(self.constraint)
        
    def test_slice_discriminating_expression_fixed_value(self):
        self.__prepare_discriminator_fixed__()
        assert self.slice.discriminating_expression == "where(valueString='myString')"
        
    def test_slice_full_fhir_path_fixed_value(self):
        self.__prepare_discriminator_fixed__()
        assert self.slice.full_fhir_path == "Observation.component.where(valueString='myString')"
        
        

    def __prepare_discriminator_extension__(self):
        self.slicing.discriminators = [Discriminator(type='value', path='url')]
        self.slice.type = 'Extension'
        self.slicing.path = 'Observation.extension'
        self.constraint.path = self.slicing.path
        profile = MagicMock()
        profile.__canonical_url__ = 'http://doman.org/extension'
        self.constraint.profile = profile
        self.slice.add_constraint(self.constraint)
                
    def test_slice_discriminating_expression_extension(self):
        self.__prepare_discriminator_extension__()
        assert self.slice.discriminating_expression == "extension('http://doman.org/extension')"
         
    def test_slice_full_fhir_path_extension(self):
        self.__prepare_discriminator_extension__()
        assert self.slice.full_fhir_path == "Observation.extension('http://doman.org/extension')"
        
        
    def test_slice_discriminating_expression_index(self):
        self.slicing.discriminators = [Discriminator(type='position', path='$this')]
        assert self.slice.discriminating_expression == "index(0)"
        
        
    def __prepare_discriminator_type__(self):
        self.slicing.discriminators = [Discriminator(type='type', path='value[x]')]
        self.constraint.path = 'Observation.component.value[x]'
        self.slice.type = 'Quantity'
        self.slice.add_constraint(self.constraint)
        
    def test_slice_discriminating_expression_type(self):
        self.__prepare_discriminator_type__()
        assert self.slice.discriminating_expression == "where(value[x] is Quantity)"

    def test_slice_full_fhir_path_type(self):
        self.__prepare_discriminator_type__()
        assert self.slice.full_fhir_path == "Observation.component.where(value[x] is Quantity)"