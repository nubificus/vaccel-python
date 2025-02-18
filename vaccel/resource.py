from abc import abstractmethod
from vaccel._vaccel import lib, ffi
from vaccel.error import VaccelError
import os


class Resource:
    """A vAccel resource

    vAccel resources are not exposed as concrete data structures
    from the vAccel runtime for the end-programmer to use. Instead,
    they are embedded in concrete resources, e.g. a TensorFlow model,
    hence this is an abstract class with common methods for all
    exposed methods of vAccel resources
    """
    @abstractmethod
    def id(self):
        """The id of a vAccel resource"""
        pass

    @abstractmethod
    def is_registered(self, session):
        """Checks if the resource is registered with the session

        Args:
            session: A vaccel.Session instance

        Returns:
            True if the resource is registered with the session"""
        pass

    @abstractmethod
    def _get_inner_resource(self):
        pass

    def __init__(self, session, obj, rtype):
        self.path = obj
        # self.filename_len = len(obj)
        # self.file = self.__create_vaccel_file__()
        # self.vaccel_files = self.__create_vaccel_file_table__(1)
        self.session = session
        self._inner = self.create_resource(rtype)
        self.register = self.register_resource()

    def __del__(self):
        self.unregister = self.unregister_resource()
        self.destroy = self.destroy_resource()

    def __parse_object__(self,obj) -> bytes:
            """Parses a shared object file and returns its content and size

            Args:
                obj: The path to the shared object file

            Returns:
                A tuple containing the content of the shared object file as bytes
                and its size as an integer

            Raises:
                TypeError: If object is not a string
            """
            filename = self.filename
            obj = self.filename
            if not isinstance(obj, str):
                raise TypeError(
                    f"Invalid image type. Expected str or bytes, got {type(obj)}.")

            if isinstance(obj, str):
                with open(obj, "rb") as objfile:
                    obj = objfile.read()

            size = os.stat(filename).st_size
            return obj, size

    def __create_vaccel_files__(self):
        file = ffi.new("struct vaccel_file *")
        filename = bytes(self.filename, encoding="utf-8")
        path = ffi.new("char[%d]" % self.filename_len, filename)
        lib.vaccel_file_new(file, path)
        lib.vaccel_file_read(file)

        return file

    def __create_vaccel_file_table__(self, nr_files):
        table = ffi.new("struct vaccel_file *[%d]" % nr_files, list(self.file))
        return table

    def create_resource(self, rtype):
            """Creates a resource from a file and returns a pointer to it

            Args:
                rtype: The resource type

            Returns:
                A pointer to the resource
            """
            sharedobj = bytes(self.path, encoding="utf-8")
            resource = ffi.new("struct vaccel_resource *")
            lib.vaccel_resource_init(resource, sharedobj, rtype)
            return resource

    def register_resource(self):
        ret = lib.vaccel_resource_register(self._inner, self.session._to_inner())
        return ret

    def destroy_resource(self):
        ret= lib.vaccel_resource_release(self._inner)
        return ret

    def unregister_resource(self):
        ret = lib.vaccel_resource_unregister(self._inner, self.session._to_inner())
        return ret

    def _to_inner(self):
        return self._inner
