from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .rustlibrary import RustLibrary


class SunscreenFHEContext:
    def __init__(self, rust_library, context):
        self.rust_library = rust_library
        self.context = context
        self.key_set = None

    @classmethod
    def create_from_params(_cls, params):
        rust_library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_string(params, rust_library)
        context = rust_library.get().initialize_context_with_params_as_string(
            buffer.get()
        )
        return SunscreenFHEContext(rust_library, context)

    @classmethod
    def create_from_params_as_specified(_cls, lattice_dimension, plain_modulus):
        rust_library = RustLibrary()
        context = rust_library.get().initialize_context_from_params(
            lattice_dimension, plain_modulus
        )
        return SunscreenFHEContext(rust_library, context)

    def __del__(self):
        if self.context:
            self.rust_library.get().release_context(self.context)

    def get_rust_library(self):
        return self.rust_library

    def get_inner_context(self):
        return self.context

    def get_params(self):
        param_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )
        self.rust_library.get().get_params_as_string(self.context, param_buffer.get())

        return param_buffer.get_string()

    def get_public_key(self, key_set_override=None):
        if key_set_override:
            return key_set_override.get_public_key()

        return self.key_set.get_public_key()

    def get_private_key(self, key_set_override=None):
        if key_set_override:
            return key_set_override.get_private_key()

        if self.key_set:
            return self.key_set.get_private_key()

        return None

    def generate_keys(self):
        keys = self.rust_library.get().generate_keys(self.context)
        public_key = self.rust_library.get().get_public_key(keys)
        private_key = self.rust_library.get().get_private_key(keys)
        self.key_set = KeySet(public_key, private_key, self.rust_library)
        return self.key_set


class KeySet:
    def __init__(self, public_key, private_key, rust_library):
        self.public_key = public_key
        self.private_key = private_key
        self.rust_library = rust_library

    @classmethod
    def initialize_from_pointers(_cls, public_key, private_key=None):
        return KeySet(public_key, private_key, RustLibrary())

    @classmethod
    def initialize_from_string(_cls, public_key, private_key=None):
        library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_string(public_key, library)
        public_key = library.get().get_public_key_from_string(buffer.get())
        if private_key:
            pvt_buffer = SunscreenInteropBuffer.create_from_string(private_key, library)
            public_key = library.get().get_private_key_from_string(pvt_buffer.get())

        return KeySet(public_key, private_key, library)

    @classmethod
    def initialize_from_string_with_public_key(_cls, public_key):
        return KeySet.initialize_from_string(public_key, None)

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_public_key_string(self):
        param_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )

        self.rust_library.get().get_public_key_as_string(
            self.public_key, param_buffer.get()
        )
        return param_buffer.get_string()

    def __del__(self):
        if self.public_key:
            self.rust_library.get().release_public_key(self.public_key)
        if self.private_key:
            self.rust_library.get().release_private_key(self.private_key)
