"""The utility module contains the object representations of the utility FHIRPath functions."""


from fhircraft.fhir.path.engine.core import FHIRPathCollectionItem, FHIRPathFunction, FHIRPath
from fhircraft.fhir.path.engine.filtering import Select
from fhircraft.fhir.path.engine.literals import Date, DateTime, Time
from fhircraft.utils import ensure_list
import datetime 
from typing import List, Optional

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FHIRPath')

class Trace(FHIRPathFunction):
    """
    A representation of the FHIRPath [`trace()`](http://hl7.org/fhirpath/N1/#tracename-string-projection-expression-collection) function.

    Attributes:
        name  (str): Subtring query.
    """
    def __init__(self, name: str, projection: Optional[FHIRPath] = None):
        self.name = name
        self.projection = projection

    def evaluate(self, collection: List[FHIRPathCollectionItem], *args, **kwargs) -> int:
        """
        Adds a `String` representation of the input collection to the diagnostic log, using the `name` argument
        as the name in the log. This log should be made available to the user in some appropriate fashion. Does not
        change the input, so returns the input collection as output.

        If the `projection` argument is used, the trace would log the result of evaluating the project expression on the input,
        but still return the input to the trace function unchanged.

        Args: 
            collection (List[FHIRPathCollectionItem])): The input collection.
        
        Returns:
            collection (List[FHIRPathCollectionItem])): The input collection.            
        """ 
        log_collection = collection
        if self.projection:
            log_collection = Select(self.projection).evaluate(collection, *args, **kwargs)
        logger.debug(f'{self.name} - {[str(item.value) if isinstance(item, FHIRPathCollectionItem) else str(item) for item in ensure_list(log_collection)]}')        
        return collection


class Now(FHIRPathFunction):
    """
    A representation of the FHIRPath [`now()`](http://hl7.org/fhirpath/N1/#now-datetime) function.
    """
    def evaluate(self, *args, **kwargs) -> int:
        """
        Returns the current date and time, including timezone offset.

        Returns:
            DateTime: The current date and time, including timezone offset.        
        """ 
        now = datetime.now()
        return DateTime(now.year, now.month, now.day, now.hour, now.minute)



class TimeOfDay(FHIRPathFunction):
    """
    A representation of the FHIRPath [`timeOfDay()`](http://hl7.org/fhirpath/N1/#timeOfDay-time) function.
    """
    def evaluate(self, *args, **kwargs) -> int:
        """
        Returns the current time.

        Returns:
            Time: The current time.        
        """ 
        now = datetime.now()
        return Time(now.hour, now.minute)


class Today(FHIRPathFunction):
    """
    A representation of the FHIRPath [`Today()`](http://hl7.org/fhirpath/N1/#today-date) function.
    """
    def evaluate(self, *args, **kwargs) -> int:
        """
        Returns the current date.

        Returns:
            Date: The current date.        
        """ 
        now = datetime.now()
        return DateTime(now.year, now.month, now.day)
