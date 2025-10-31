import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)

try:
    import pystray
    print("pystray location:", pystray.__file__)
    print("pystray version:", pystray.__version__ if hasattr(pystray, '__version__') else 'unknown')
    print("✓ pystray OK")
except ImportError as e:
    print("✗ pystray NOT FOUND:", e)

try:
    import customtkinter
    print("✓ customtkinter OK")
except ImportError as e:
    print("✗ customtkinter NOT FOUND:", e)

try:
    import darkdetect
    print("✓ darkdetect OK")
except ImportError as e:
    print("✗ darkdetect NOT FOUND:", e)
