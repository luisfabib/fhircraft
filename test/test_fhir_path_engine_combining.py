from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, Element
from fhircraft.fhir.path.engine.combining import *
        
env = dict()

#-------------
# Union
#-------------

def test_union_returns_combined_collection_without_duplicates():
    collection = [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1")]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Union(other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item2")]

def test_union_string_representation():
    expression = Union(Element("other"))
    assert str(expression) == "union(other)"

    
#-------------
# Combine
#-------------

def test_combine_returns_combined_collection_with_duplicates():
    collection = [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1")]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Combine(other_collection).evaluate(collection, env)
    assert result == [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item2")]
    
def test_combine_string_representation():
    expression = Combine(Element("other"))
    assert str(expression) == "combine(other)"