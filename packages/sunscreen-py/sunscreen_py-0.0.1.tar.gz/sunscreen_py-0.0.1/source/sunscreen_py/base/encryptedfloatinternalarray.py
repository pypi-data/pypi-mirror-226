from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encryptedfloat import EncryptedFloat
from .encrypted import Encrypted
import json


class EncryptedFloatInternalArray(Encrypted):
    STANDARD_LENGTH = 15
    standard_noise_for_fresh_cipher = None

    def __init__(self, pointer, context, is_fresh, noise_budget, key_set_override=None):
        Encrypted.__init__(
            self, pointer, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def create_from_plain_vector(_cls, vector, context, key_set_override=None):
        vector = EncryptedFloatInternalArray.standardize_length(vector)

        vector_string = json.dumps(vector)
        vector_buffer = SunscreenInteropBuffer.create_from_string(
            vector_string, context.get_rust_library()
        )
        cipher = (
            context.get_rust_library()
            .get()
            .encrypt_float_array(
                context.get_inner_context(),
                context.get_public_key(key_set_override),
                vector_buffer.get(),
            )
        )

        if EncryptedFloatInternalArray.standard_noise_for_fresh_cipher is None:
            EncryptedFloatInternalArray.standard_noise_for_fresh_cipher = (
                Encrypted.get_noise_budget_from_runtime(
                    context, cipher, key_set_override
                )
            )

        return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
            cipher,
            context,
            True,
            EncryptedFloatInternalArray.standard_noise_for_fresh_cipher,
            key_set_override,
        )

    @classmethod
    def create_from_encrypted_vector_string(
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
        return EncryptedFloatInternalArray(
            cipher, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def create_from_encrypted_vector_pointer(
        _cls, cipher, context, is_fresh=False, noise_budget=None, key_set_override=None
    ):
        if not noise_budget:
            noise_budget = Encrypted.get_noise_budget_from_runtime(
                context, cipher, key_set_override
            )
        return EncryptedFloatInternalArray(
            cipher, context, is_fresh, noise_budget, key_set_override
        )

    @classmethod
    def standardize_length(_cls, vector):
        if len(vector) > EncryptedFloatInternalArray.STANDARD_LENGTH:
            raise Exception("Arrays longer than {STANDARD_LENGTH} are not supported")

        if len(vector) < EncryptedFloatInternalArray.STANDARD_LENGTH:
            vector = vector + [0.0] * (
                EncryptedFloatInternalArray.STANDARD_LENGTH - len(vector)
            )

        return vector

    def reencrypt(self):
        value = self.decrypt()
        reencrypted = EncryptedFloatInternalArray.create_from_plain_vector(
            value, self.context, self.key_set_override
        )
        self.replace_pointer(reencrypted.release())
        self.noise_budget = reencrypted.noise_budget
        self.is_fresh = True

    def decrypt(self):
        vector_buffer = SunscreenInteropBuffer.create_for_length(
            DEFAULT_BUFFER_LENGTH, self.rust_library
        )
        self.rust_library.get().decrypt_float_array(
            self.context.get_inner_context(),
            self.context.get_private_key(self.key_set_override),
            self.get(),
            vector_buffer.get(),
        )
        vector_string = vector_buffer.get_string()
        return json.loads(vector_string)

    def dot(self, other):
        if isinstance(other, EncryptedFloatInternalArray):
            (noise, result) = self.context.execute_function(
                "dot_product_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, list) and isinstance(other[0], int):
            other = [float(i) for i in other]

        if isinstance(other, list) and isinstance(other[0], float):
            other = EncryptedFloatInternalArray.standardize_length(other)
            other = [Encrypted.fix_zero_in_plain(i) for i in other]

            vector_string = json.dumps(other)
            vector_buffer = SunscreenInteropBuffer.create_from_string(
                vector_string, self.rust_library
            )
            (noise, result) = self.context.execute_function(
                "dot_product_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                vector_buffer,
            )

            return EncryptedFloat.create_from_encrypted_cipher_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception("Dot product not supported for other types")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, EncryptedFloatInternalArray):
            (noise, result) = self.context.execute_function(
                "vector_product_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, list) and isinstance(other[0], int):
            other = [float(i) for i in other]

        if isinstance(other, list) and isinstance(other[0], float):
            other = EncryptedFloatInternalArray.standardize_length(other)
            other = [Encrypted.fix_zero_in_plain(i) for i in other]

            vector_string = json.dumps(other)
            vector_buffer = SunscreenInteropBuffer.create_from_string(
                vector_string, self.rust_library
            )
            (noise, result) = self.context.execute_function(
                "vector_product_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                vector_buffer,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, int):
            other = float(other)

        if isinstance(other, float):
            other = Encrypted.fix_zero_in_plain(other)

            (noise, result) = self.context.execute_function(
                "vector_scale_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, EncryptedFloat):
            (noise, result) = self.context.execute_function(
                "vector_scale_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Multiplication is only supported for arrays of floats and encrypted arrays of floats"
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, EncryptedFloatInternalArray):
            (noise, result) = self.context.execute_function(
                "vector_sum_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, list) and isinstance(other[0], int):
            other = [float(i) for i in other]

        if isinstance(other, list) and isinstance(other[0], float):
            other = EncryptedFloatInternalArray.standardize_length(other)

            vector_string = json.dumps(other)
            vector_buffer = SunscreenInteropBuffer.create_from_string(
                vector_string, self.rust_library
            )
            (noise, result) = self.context.execute_function(
                "vector_sum_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                vector_buffer,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Addition is only supported for arrays of floats and encrypted arrays of floats"
        )

    def __div__(self, _):
        raise Exception("Division is unsupported")

    def __sub__(self, other):
        if isinstance(other, EncryptedFloatInternalArray):
            (noise, result) = self.context.execute_function(
                "vector_difference_with_cipher",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                other,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        if isinstance(other, list) and isinstance(other[0], int):
            other = [float(i) for i in other]

        if isinstance(other, list) and isinstance(other[0], float):
            other = EncryptedFloatInternalArray.standardize_length(other)

            vector_string = json.dumps(other)
            vector_buffer = SunscreenInteropBuffer.create_from_string(
                vector_string, self.rust_library
            )
            (noise, result) = self.context.execute_function(
                "vector_difference_with_plain",
                self.context.get_inner_context(),
                self.context.get_public_key(self.key_set_override),
                self,
                vector_buffer,
            )

            return EncryptedFloatInternalArray.create_from_encrypted_vector_pointer(
                result, self.context, False, noise, self.key_set_override
            )

        raise Exception(
            "Addition is only supported for arrays of floats and encrypted arrays of floats"
        )
