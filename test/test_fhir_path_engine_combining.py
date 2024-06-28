from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem
from fhircraft.fhir.path.engine.combining import *
        



#-------------
# Union
#-------------

def test_union_returns_combined_collection_without_duplicates():
    collection = [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1")]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Union(other_collection).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item2")]

    
#-------------
# Combine
#-------------

def test_combine_returns_combined_collection_with_duplicates():
    collection = [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1")]
    other_collection = [FHIRPathCollectionItem(value="item2")]
    result = Combine(other_collection).evaluate(collection)
    assert result == [FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item1"), FHIRPathCollectionItem(value="item2")]