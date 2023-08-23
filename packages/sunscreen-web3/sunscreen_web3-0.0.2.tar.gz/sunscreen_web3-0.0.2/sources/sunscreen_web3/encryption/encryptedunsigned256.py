from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encrypted import Encrypted


class EncryptedUnsigned256(Encrypted):
    standard_noise_for_fresh_cipher = None

    def __init__(self, pointer, context, is_fresh, noise_budget, key_set_override):
        Encrypted.__init__(
            self, pointer, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def create_from_plain(_cls, hex, context, key_set_override=None):
        hex_buffer = SunscreenInteropBuffer.create_from_string(
            hex, context.get_rust_library()
        )
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_unsigned256(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                hex_buffer.get(),
            )
        )

        if EncryptedUnsigned256.standard_noise_for_fresh_cipher is None:
            EncryptedUnsigned256.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, cipher, key_set_override
                )
            )

        result = EncryptedUnsigned256(
            cipher,
            context,
            True,
            EncryptedUnsigned256.standard_noise_for_fresh_cipher,
            key_set_override,
        )
        return result

    @classmethod
    def create_from_encrypted_cipher_string(
        _cls,
        cipher_string,
        context,
        is_fresh=False,
        noise_budget=None,
        key_set_override=None,
    ):
        buffer = SunscreenInteropBuffer.create_from_string(
            cipher_string, context.get_rust_library()
        )
        cipher = context.get_rust_library().get().get_cipher_from_string(buffer.get())
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedUnsigned256(
            cipher, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def create_from_encrypted_cipher_pointer(
        _cls, cipher, context, is_fresh=False, noise_budget=None, key_set_override=None
    ):
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedUnsigned256(
            cipher, context, is_fresh, noise_budget, key_set_override
        )

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedUnsigned256.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.noise_budget = reencrypted.noise_budget
        self.is_fresh = True

    def decrypt(self):
        decrypt_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )
        self.rust_library.get().decrypt_unsigned256(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
            decrypt_buffer.get(),
        )

        return decrypt_buffer.get_string()


class EncryptedUnsigned256Zero(EncryptedUnsigned256):
    def __init__(self, context, key_set_override):
        EncryptedUnsigned256.__init__(
            self,
            None,
            context,
            True,
            EncryptedUnsigned256.standard_noise_for_fresh_cipher,
            key_set_override,
        )
        if EncryptedUnsigned256.standard_noise_for_fresh_cipher is None:
            hex_buffer = SunscreenInteropBuffer.create_from_string(
                "0x0", context.get_rust_library()
            )
            self.pointer = self.rust_library.get().encrypt_unsigned256(
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                hex_buffer.get(),
            )
            EncryptedUnsigned256.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, self.pointer, key_set_override
                )
            )
            self.noise_budget = EncryptedUnsigned256.standard_noise_for_fresh_cipher

    def get(self):
        with self.lock:
            if not self.pointer:
                hex_buffer = SunscreenInteropBuffer.create_from_string(
                    "0x0", self.context.get_rust_library()
                )
                self.pointer = self.rust_library.get().encrypt_unsigned256(
                    self.context.get_inner_context(),
                    self.context.get_public_key(self.key_set_override),
                    hex_buffer.get(),
                )

            return self.pointer
