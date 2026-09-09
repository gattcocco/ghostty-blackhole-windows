"""Experimental Windows transport; needs a console and OSC 12/112 forwarding.

Never allocates a console window. Returns False when no console is inherited.
"""
import os


def emit_console(sequence):
    if os.name != "nt":
        return False
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD,
        wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
        wintypes.HANDLE]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WriteFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p,
        wintypes.DWORD, ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateFileW("CONOUT$", 0xC0000000, 3, None, 3, 0, None)
    if handle == ctypes.c_void_p(-1).value:
        return False
    try:
        mode = wintypes.DWORD()
        if not kernel.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        # Preserve mode bits; enable processed output and VT for the session.
        if not kernel.SetConsoleMode(handle, mode.value | 0x0001 | 0x0004):
            return False
        written = wintypes.DWORD()
        buffer = ctypes.create_string_buffer(sequence)
        return bool(kernel.WriteFile(handle, buffer, len(sequence),
                    ctypes.byref(written), None)) and written.value == len(sequence)
    finally:
        kernel.CloseHandle(handle)
