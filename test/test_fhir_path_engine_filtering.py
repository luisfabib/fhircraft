from fhircraft.fhir.path.engine.core import *
from fhircraft.fhir.path.engine.comparison import *
from fhircraft.fhir.path.engine.filtering import *
from collections import namedtuple


#-------------
# Where
#-------------

def test_where_returns_empty_for_empty_collection():
    collection = []
    result = Where(LessThan(This(), 3)).evaluate(collection)
    assert result == []

def test_where_returns_valid_items_in_collection_where_true():
    collection = [FHIRPathCollectionItem(value=4), FHIRPathCollectionItem(value=1)]
    result = Where(LessThan(This(), 3)).evaluate(collection)
    assert result == [collection[1]]



#-------------
# Select
#-------------

def test_select_returns_empty_for_empty_collection():
    collection = []
    result = Select(Invocation(This(), Element('field'))).evaluate(collection)
    assert result == []

def test_select_returns_collection_of_projected_elements():
    Resource = namedtuple('Resource', 'field')
    collection = [FHIRPathCollectionItem(value=Resource(field=123)), FHIRPathCollectionItem(value=Resource(field=456))]
    result = Select(Invocation(This(), Element('field'))).evaluate(collection)
    assert result[0].value == 123
    assert result[1].value == 456



#-------------
# Repeat
#-------------

def test_repeat_returns_empty_for_empty_collection():
    collection = []
    result = Repeat(Invocation(This(), Element('field'))).evaluate(collection)
    assert result == []

def test_repeat_returns_collection_of_nested_repeating_elements():
    Resource = namedtuple('Resource', ('label','items'))
    collection = [
        FHIRPathCollectionItem(value=Resource(label='1', items=[
            Resource(label='1.1', items=[]), 
            Resource(label='1.2', items=[
                Resource(label='1.2.1', items=[])
            ]), 
            Resource(label='1.3', items=[
                Resource(label='1.3.1', items=[])
            ]), 
        ]))
    ]
    result = Repeat(Invocation(This(), Element('items'))).evaluate(collection)
    assert [item.value.label for item in result] == ['1.1', '1.2', '1.3', '1.2.1', '1.3.1']

    

#-------------
# Repeat
#-------------

def test_ofType_returns_empty_for_empty_collection():
    collection = []
    result = OfType(str).evaluate(collection)
    assert result == []

def test_ofType_returns_filtered_collection_by_type():
    Resource1 = namedtuple('Resource1Type', 'value')
    Resource2 = namedtuple('Resource2Type', 'value')
    collection = [
        FHIRPathCollectionItem(value=Resource1(value=1)),
        FHIRPathCollectionItem(value=Resource2(value=2)),
        FHIRPathCollectionItem(value=Resource1(value=3)),
    ]
    result = OfType(Resource1).evaluate(collection)
    assert result == [collection[0], collection[2]]