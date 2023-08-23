from setuptools import setup

setup(
    name='browser_cookie_3x',
    version='0.19.1',
    packages=['browser_cookie_3x'],
    package_dir={'browser_cookie_3x': 'browser_cookie_3x'},
    author='.',    
    description='Loads cookies from your browser into a cookiejar object so can download with urllib and other libraries the same content you see in the web browser.',     # noqa: E501
    url='https://google.com/',
    install_requires=[
        'lz4',
        'pycryptodomex',
        'dbus-python; python_version < "3.7" and ("bsd" in sys_platform or sys_platform == "linux")',
        'jeepney; python_version >= "3.7" and ("bsd" in sys_platform or sys_platform == "linux")'
    ],
    license='lgpl'
)
