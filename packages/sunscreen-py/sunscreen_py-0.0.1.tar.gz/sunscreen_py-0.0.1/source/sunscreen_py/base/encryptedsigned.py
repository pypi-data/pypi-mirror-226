from ..internal.sunscreenpool import SunscreenPool
from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encrypted import Encrypted


class EncryptedSigned(Encrypted):
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
            .encrypt_signed(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                number,
            )
        )

        if EncryptedSigned.standard_noise_for_fresh_cipher is None:
            EncryptedSigned.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, cipher, key_set_override
                )
            )

        result = EncryptedSigned(
            cipher,
            context,
            True,
            EncryptedSigned.standard_noise_for_fresh_cipher,
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
        return EncryptedSigned(cipher, context, is_fresh, noise_budget, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        _cls, cipher, context, is_fresh=False, noise_budget=None, key_set_override=None
    ):
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedSigned(cipher, context, is_fresh, noise_budget, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedSigned.create_from_plain(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.noise_budget = reencrypted.noise_budget
        self.is_fresh = True

    def decrypt(self):
        return self.rust_library.get().decrypt_signed(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
        )

    def shape(self):
        return [1, 1]

    @classmethod
    def __check_if_zero__(_cls, value):
        if isinstance(value, EncryptedSignedZero) or (
            (isinstance(value, int)) and int(value) == 0
        ):
            return True
        return False


class EncryptedSignedZero(EncryptedSigned):
    def __init__(self, context, key_set_override):
        EncryptedSigned.__init__(
            self,
            None,
            context,
            True,
            EncryptedSigned.standard_noise_for_fresh_cipher,
            key_set_override,
        )
        if EncryptedSigned.standard_noise_for_fresh_cipher is None:
            self.pointer = self.rust_library.get().encrypt_signed(
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                0,
            )
            EncryptedSigned.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, self.pointer, key_set_override
                )
            )
            self.noise_budget = EncryptedSigned.standard_noise_for_fresh_cipher

    def get(self):
        with self.lock:
            if not self.pointer:
                self.pointer = self.rust_library.get().encrypt_signed(
                    self.context.get_inner_context(),
                    self.context.get_public_key(self.key_set_override),
                    0,
                )

            return self.pointer
