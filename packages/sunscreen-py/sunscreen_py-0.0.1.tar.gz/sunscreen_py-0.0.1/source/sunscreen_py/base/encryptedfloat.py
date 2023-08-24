from ..internal.sunscreenpool import SunscreenPool
from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encrypted import Encrypted


class EncryptedFloat(Encrypted):
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

        if EncryptedFloat.standard_noise_for_fresh_cipher is None:
            EncryptedFloat.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, cipher, key_set_override
                )
            )

        result = EncryptedFloat(
            cipher,
            context,
            True,
            EncryptedFloat.standard_noise_for_fresh_cipher,
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
        return EncryptedFloat(cipher, context, is_fresh, noise_budget, key_set_override)

    @classmethod
    def create_from_encrypted_cipher_pointer(
        _cls, cipher, context, is_fresh=False, noise_budget=None, key_set_override=None
    ):
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedFloat(cipher, context, is_fresh, noise_budget, key_set_override)

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedFloat.create_from_plain(
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

    def shape(self):
        return [1, 1]

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if EncryptedFloat.__check_if_zero__(other) or EncryptedFloat.__check_if_zero__(
            self
        ):
            return EncryptedFloatZero()

        if isinstance(other, EncryptedFloat):
            (noise, result) = self.context.execute_function(
                "product_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, int):
            other = float(other)

        if isinstance(other, float):
            other = Encrypted.fix_zero_in_plain(other)
            (noise, result) = self.context.execute_function(
                "product_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        from .encryptedfloatinternalarray import EncryptedFloatInternalArray

        if isinstance(other, EncryptedFloatInternalArray):
            (noise, result) = self.context.execute_function(
                "vector_scale_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                other,
                self,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        from .encryptedfloatarray import EncryptedFloatArray

        if isinstance(other, EncryptedFloatArray):
            return other * self

        if isinstance(other, list):

            def execute(data):
                return other[data] * self

            interim_result = SunscreenPool.get_instance().map(
                execute, range(0, len(other))
            )

            return EncryptedFloatArray.create_from_encrypted_vector_objects(
                interim_result, self.context, False, self.key_set_override
            )

        raise Exception(
            "Multiplication is not supported for anything other than floats or encrypted floats. But we got "
            + str(other)
        )

    def __div__(self, _):
        raise Exception("Division is unsupported")

    def __rsub__(self, other):
        if isinstance(other, EncryptedFloat):
            (noise, result) = self.context.execute_function(
                "difference_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, int):
            other = float(other)

        if isinstance(other, float):
            (noise, result) = self.context.execute_function(
                "difference_with_plain_reverse",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Subtraction is not supported for anything other than floats or encrypted floats"
        )

    def __sub__(self, other):
        if EncryptedFloat.__check_if_zero__(other):
            return self

        if isinstance(other, EncryptedFloat):
            (noise, result) = self.context.execute_function(
                "difference_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, int):
            other = float(other)

        if isinstance(other, float):
            (noise, result) = self.context.execute_function(
                "difference_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Subtraction is not supported for anything other than floats or encrypted floats"
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if EncryptedFloat.__check_if_zero__(other):
            return self

        if isinstance(other, EncryptedFloat):
            (noise, result) = self.context.execute_function(
                "sum_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, int):
            other = float(other)

        if isinstance(other, float):
            (noise, result) = self.context.execute_function(
                "sum_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Addition is not supported for anything other than floats or encrypted floats "
            + str(type(other))
        )

    @classmethod
    def __check_if_zero__(_cls, value):
        if isinstance(value, EncryptedFloatZero) or (
            (isinstance(value, float) or isinstance(value, int)) and float(value) == 0.0
        ):
            return True
        return False


class EncryptedFloatZero(EncryptedFloat):
    def __init__(self, context, key_set_override):
        EncryptedFloat.__init__(
            self,
            None,
            context,
            True,
            EncryptedFloat.standard_noise_for_fresh_cipher,
            key_set_override,
        )
        if EncryptedFloat.standard_noise_for_fresh_cipher is None:
            self.pointer = self.rust_library.get().encrypt_float(
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                0,
            )
            EncryptedFloat.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, self.pointer, key_set_override
                )
            )
            self.noise_budget = EncryptedFloat.standard_noise_for_fresh_cipher

    def get(self):
        with self.lock:
            if not self.pointer:
                self.pointer = self.rust_library.get().encrypt_float(
                    self.context.get_inner_context(),
                    self.context.get_public_key(self.key_set_override),
                    0,
                )

            return self.pointer
