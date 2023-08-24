import ctypes
from threading import RLock

DEFAULT_BUFFER_LENGTH = 50 * 1024 * 1024


class SunscreenInteropBuffer:
    def __init__(self, buffer, rust_library):
        self.library = rust_library
        self.buffer = buffer
        self.lock = RLock()

    @classmethod
    def create_from_string(_cls, data, rust_library):
        encoded = bytearray(data, encoding="UTF-8")
        length = len(encoded)
        buffer = None
        try:
            buffer = SunscreenInteropBuffer.__malloc_rust(length, rust_library)
            pointer = rust_library.get().buffer_data(buffer)
            encoded_ptr = (ctypes.c_char * length).from_buffer(encoded)
            ctypes.memmove(pointer, encoded_ptr, length)
            rust_library.get().set_buffer_length(buffer, length)
            return SunscreenInteropBuffer(buffer, rust_library)
        except:
            if buffer:
                SunscreenInteropBuffer.__free_rust(buffer, rust_library)
            raise

    @classmethod
    def create_for_length(_cls, length, rust_library):
        buffer = None
        try:
            buffer = SunscreenInteropBuffer.__malloc_rust(length, rust_library)
            return SunscreenInteropBuffer(buffer, rust_library)
        except:
            if buffer:
                SunscreenInteropBuffer.__free_rust(buffer, rust_library)
            raise

    def get_string(self):
        length = self.library.get().buffer_length(self.get())
        buffer = bytearray(length)
        buffer_ptr = (ctypes.c_char * length).from_buffer(buffer)
        pointer = self.library.get().buffer_data(self.get())
        ctypes.memmove(buffer_ptr, pointer, length)
        decoded_string = buffer.decode("UTF-8")

        return decoded_string

    def get(self):
        with self.lock:
            return self.buffer

    def release(self):
        with self.lock:
            buffer = self.buffer
            self.buffer = None
            return buffer

    def replace_buffer(self, buffer):
        with self.lock:
            self.buffer = buffer

    def __del__(self):
        if self.buffer:
            SunscreenInteropBuffer.__free_rust(self.buffer, self.library)

    @classmethod
    def __malloc_rust(_cls, size, rust_library):
        return rust_library.get().buffer_create(size)

    @classmethod
    def __free_rust(_cls, ptr, rust_library):
        rust_library.get().buffer_release(ptr)
