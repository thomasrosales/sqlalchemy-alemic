import asyncio
from functools import wraps


def insert_api_module_attribute(underscore_attribute_name, APIModuleClass):

    def decorated_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = asyncio.run(func(*args, **kwargs))
            if isinstance(result, list):
                if len(result) > 0:
                    for instance in result:
                        setattr(
                            instance,
                            underscore_attribute_name,
                            APIModuleClass(related_instance_id=instance.id),
                        )
            elif result:
                setattr(
                    result,
                    underscore_attribute_name,
                    APIModuleClass(related_instance_id=result.id),
                )
            return result

        return wrapper

    return decorated_function
