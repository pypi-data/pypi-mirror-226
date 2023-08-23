from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from threading import RLock


class Encrypted:
    DEFAULT_ZERO_WORKAROUND = 0.000000000000001

    def __init__(self, buffer, context, is_fresh, noise_budget, key_set_override=None):
        self.rust_library = context.get_rust_library()
        self.pointer = buffer
        self.context = context
        self.is_fresh = is_fresh
        self.noise_budget = noise_budget
        self.key_set_override = key_set_override
        self.lock = RLock()

    def __del__(self):
        if self.pointer:
            self.rust_library.get().release_cipher(self.pointer)

    def get(self):
        with self.lock:
            return self.pointer

    def release(self):
        with self.lock:
            pointer = self.get()
            self.pointer = None
            return pointer

    def replace_pointer(self, pointer):
        with self.lock:
            if self.pointer:
                self.rust_library.get().release_cipher(self.pointer)
            self.pointer = pointer

    def get_string(self):
        pointer = self.get()
        if pointer:
            buffer = SunscreenInteropBuffer.create_for_length(
                DEFAULT_BUFFER_LENGTH, self.rust_library
            )
            self.rust_library.get().get_cipher_as_string(pointer, buffer.get())
            return buffer.get_string()
        return ""
    
    @classmethod
    def fix_zero_in_plain(_cls, value):
        if value == 0:
            return Encrypted.DEFAULT_ZERO_WORKAROUND

        return value
