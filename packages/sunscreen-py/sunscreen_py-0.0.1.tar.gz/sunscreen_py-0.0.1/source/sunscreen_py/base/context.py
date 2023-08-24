import ctypes
from .buffer import SunscreenInteropBuffer, DEFAULT_BUFFER_LENGTH
from .encrypted import Encrypted
from .rustlibrary import RustLibrary
from enum import IntFlag
from ..internal.sunscreenpool import SunscreenPool


class OperationsSupported(IntFlag):
    NoOperation = 0
    CipherPlainSum = 1 << 0
    CipherCipherSum = 1 << 1
    CipherPlainDifference = 1 << 2
    PlainCipherDifference = 1 << 3
    CipherCipherDifference = 1 << 4
    CipherPlainProduct = 1 << 5
    CipherCipherProduct = 1 << 6


#    VectorCipherPlainDotProduct = 1 << 7
#    VectorCipherCipherDotProduct = 1 << 8
#    VectorCipherPlainSum = 1 << 9
#    VectorCipherCipherSum = 1 << 10
#    VectorCipherPlainScale = 1 << 11
#    VectorCipherCipherScale = 1 << 12
#    VectorPlainCipherScale = 1 << 13
#    VectorCipherPlainDifference = 1 << 14
#    VectorPlainCipherDifference = 1 << 15
#    VectorCipherCipherDifference = 1 << 16
#    VectorCipherCipherProduct = 1 << 17
#    VectorCipherPlainProduct = 1 << 18
#    MLLogisticRegressionTraining = 1 << 19
#    MLLogisticRegressionInference = 1 << 20


class SunscreenFHEContext:
    def __init__(self, rust_library, context):
        self.rust_library = rust_library
        self.context = context
        self.function_noise_budgets = {}
        self.functions_use_count = {}
        self.key_set = None
        self.thread_count = 100
        SunscreenPool.initialize(self.thread_count)

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
        context = rust_library.get().initialize_context_with_params(
            lattice_dimension, plain_modulus
        )
        return SunscreenFHEContext(rust_library, context)

    @classmethod
    def create_for_supported_operations(_cls, operations, enable_chaining=True):
        rust_library = RustLibrary()
        context = rust_library.get().initialize_context(operations, enable_chaining)
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

    def is_reencrypt_enabled(self):
        return False

    def execute_function(self, function_name, *args):
        min_noise_needed_after_operation = 16
        min_noise_in_ciphers = 2048
        fn_noise_needed = self.get_noise_budget_for_function(function_name)
        fn_noise_needed = (
            None
            if self.should_noise_budget_be_updated(function_name)
            else fn_noise_needed
        )

        arg_list = list(args)
        key_set_override = None
        for idx, arg in enumerate(arg_list):
            if (
                self.is_reencrypt_enabled()
                and isinstance(arg, Encrypted)
                and arg.noise_budget is not None
            ):
                if not arg.is_fresh and (
                    fn_noise_needed is None
                    or fn_noise_needed
                    >= (arg.noise_budget + min_noise_needed_after_operation)
                ):
                    # Re-encrypt the cipher
                    key_set_override = arg.key_set_override
                    arg.reencrypt()
                    if min_noise_in_ciphers > arg.noise_budget:
                        min_noise_in_ciphers = arg.noise_budget
                elif min_noise_in_ciphers > arg.noise_budget:
                    min_noise_in_ciphers = arg.noise_budget

        for idx, arg in enumerate(arg_list):
            if isinstance(arg, Encrypted) or isinstance(arg, SunscreenInteropBuffer):
                arg_list[idx] = arg.get()

        f = getattr(self.get_rust_library().get(), function_name)
        updated_args = tuple(arg_list)
        result = f(*updated_args)

        noise_budget_in_answer = None
        if fn_noise_needed is None and f.restype == ctypes.c_void_p:
            noise_budget_in_answer = Encrypted.get_noise_budget_from_runtime(
                self, result, key_set_override
            )
            if noise_budget_in_answer is not None:
                noise_needed = min_noise_in_ciphers - noise_budget_in_answer
                self.update_noise_budget_for_function(function_name, noise_needed)
        else:
            noise_budget_in_answer = min_noise_in_ciphers - fn_noise_needed

        self.record_function_noise_use(function_name)
        return (noise_budget_in_answer, result)

    def get_noise_budget_for_function(self, function_name):
        if function_name in self.function_noise_budgets:
            return self.function_noise_budgets[function_name]

        return None

    def update_noise_budget_for_function(self, function_name, budget):
        if function_name in self.function_noise_budgets:
            if self.function_noise_budgets[function_name] < budget:
                self.function_noise_budgets[function_name] = budget
        else:
            self.function_noise_budgets[function_name] = budget

    def record_function_noise_use(self, function_name):
        if function_name in self.functions_use_count:
            self.functions_use_count[function_name] += 1
        else:
            self.functions_use_count[function_name] = 1

    def should_noise_budget_be_updated(self, function_name):
        if function_name in self.functions_use_count:
            usage = self.functions_use_count[function_name]
            return usage % 6 == 0  # (usage & (usage - 1) == 0) and usage != 0
        else:
            return True


class KeySet:
    def __init__(self, public_key, private_key, rust_library):
        self.public_key = public_key
        self.private_key = private_key
        self.rust_library = rust_library

    @classmethod
    def initialize_from_pointers(_cls, public_key, private_key):
        return KeySet(public_key, private_key, RustLibrary())

    @classmethod
    def initialize_from_string(_cls, public_key, private_key):
        library = RustLibrary()
        buffer = SunscreenInteropBuffer.create_from_string(public_key, library)
        public_key = library.get().get_public_key_from_string(buffer.get())
        return KeySet(public_key, None, library)

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
