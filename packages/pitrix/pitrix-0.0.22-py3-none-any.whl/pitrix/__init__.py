import pyfiglet
from emoji import emojize

__project__ = 'pitrix'
__version__ = "0.0.21"
__description__ = f"{__project__}是一个测试工具，可以帮助您更轻松地编写pytest用例!"
__pitrix__ = pyfiglet.figlet_format(text=__project__, font='starwars')
__image__ = emojize(f"""{__pitrix__}{__description__}:fire::fire::fire:\nversion:{__version__}""")