from .buffer import SunscreenInteropBuffer
from .encrypted import Encrypted


class EncryptedFloat64(Encrypted):
    standard_noise_for_fresh_cipher = None

    def __init__(self, pointer, context, is_fresh, noise_budget, key_set_override):
        Encrypted.__init__(
            self, pointer, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def create_from_plain(_cls, number, context, key_set_override=None):
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_float(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                number,
            )
        )

        if EncryptedFloat64.standard_noise_for_fresh_cipher is None:
            EncryptedFloat64.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, cipher, key_set_override
                )
            )

        result = EncryptedFloat64(
            cipher,
            context,
            True,
            EncryptedFloat64.standard_noise_for_fresh_cipher,
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
        return EncryptedFloat64(cipher, context, is_fresh, noise_budget, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        _cls, cipher, context, is_fresh=False, noise_budget=None, key_set_override=None
    ):
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedFloat64(cipher, context, is_fresh, noise_budget, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedFloat64.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.noise_budget = reencrypted.noise_budget
        self.is_fresh = True

    def decrypt(self):
        return self.rust_library.get().decrypt_float(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
        )


class EncryptedFloatZero(EncryptedFloat64):
    def __init__(self, context, key_set_override):
        EncryptedFloat64.__init__(
            self,
            None,
            context,
            True,
            EncryptedFloat64.standard_noise_for_fresh_cipher,
            key_set_override,
        )
        if EncryptedFloat64.standard_noise_for_fresh_cipher is None:
            self.pointer = self.rust_library.get().encrypt_float(
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                0,
            )
            EncryptedFloat64.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, self.pointer, key_set_override
                )
            )
            self.noise_budget = EncryptedFloat64.standard_noise_for_fresh_cipher

    def get(self):
        with self.lock:
            if not self.pointer:
                self.pointer = self.rust_library.get().encrypt_float(
                    self.context.get_inner_context(),
                    self.context.get_public_key(self.key_set_override),
                    0,
                )

            return self.pointer
