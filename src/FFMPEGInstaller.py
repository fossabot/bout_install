from pathlib import Path
from src.Installer import Installer


class FFMPEGInstaller(Installer):
    """
    Installer object for installing FFMPEG
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 ffmpeg_log_path=\
                    Path(__file__).parents[1].joinpath('log', 'ffmpeg.log'),
                 nasm_log_path=\
                    Path(__file__).parents[1].joinpath('log', 'nasm.log'),
                 yasm_log_path=\
                    Path(__file__).parents[1].joinpath('log', 'yasm.log'),
                 x264_log_path=\
                    Path(__file__).parents[1].joinpath('log', 'x264.log'),
                 overwrite_on_exist=False):
        """
        Gets the FFMPEG version, sets the FFMPEG url and calls the super
        constructor

        Parameters
        ----------
        config_path : Path or str
            The path to the get_configure_command file
        ffmpeg_log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=ffmpeg_log_path)

        self.ffmpeg_version = self.config['versions']['ffmpeg']
        self.ffmpeg_url = (f'http://www.ffmpeg.org/ffmpeg-'
                           f'{self.ffmpeg_version}.tar.gz')
        self.file_from_make = self.local_dir.joinpath('bin', 'ffmpeg-wisdom')

        # Create dependency installers
        self.nasm = \
            NASMInstaller(config_path=config_path, log_path=nasm_log_path)
        self.yasm = \
            YASMInstaller(config_path=config_path, log_path=yasm_log_path)
        self.x264 = \
            X264Installer(config_path=config_path, log_path=x264_log_path)

        self.extra_config_options = \
            {'enable-gpl': None,
             'enable-libx264': None,
             'extra-ldflags': f'L{self.local_dir.joinpath("lib")}',
             'extra-cflags': f'I{self.local_dir.joinpath("include")}'}

    def install(self):
        """
        Installs the FFMPEG package
        """

        # Install dependencies
        self.nasm.install()
        self.yasm.install()
        self.x264.install()

        self.logger.info('Installing FFMPEG')
        self.install_package(url=self.ffmpeg_url,
                             file_from_make=self.file_from_make,
                             extra_config_option=self.extra_config_options,
                             overwrite_on_exist=self.overwrite_on_exist)
        self.logger.info('Installation completed successfully')


class NASMInstaller(Installer):
    """
    Installer object for installing NASM
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 log_path=Path(__file__).parents[1].joinpath('log', 'nasm.log'),
                 overwrite_on_exist=False):
        """
        Gets the NASM version, sets the NASM url and calls the super
        constructor

        Parameters
        ----------
        config_path : Path or str
            The path to the get_configure_command file
        log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=log_path)

        self.nasm_version = self.config['versions']['nasm']
        self.nasm_url = (f'http://www.nasm.us/pub/nasm/releasebuilds/'
                         f'{self.nasm_version}/'
                         f'nasm-{self.nasm_version}.tar.gz')

        self.file_from_make = self.local_dir.joinpath('bin', 'nasm')

    def install(self):
        """
        Installs the NASM package
        """

        self.logger.info('Installing NASM')

        self.install_package(url=self.nasm_url,
                             file_from_make=self.file_from_make,
                             overwrite_on_exist=self.overwrite_on_exist)
        self.logger.info('Installation completed successfully')


class YASMInstaller(Installer):
    """
    Installer object for installing YASM
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 log_path=Path(__file__).parents[1].joinpath('log', 'yasm.log'),
                 overwrite_on_exist=False):
        """
        Gets the YASM version, sets the YASM url and calls the super
        constructor

        Parameters
        ----------
        config_path : Path or str
            The path to the get_configure_command file
        log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=log_path)

        self.yasm_version = self.config['versions']['yasm']
        self.yasm_url = (
            f'http://www.tortall.net/projects/yasm/releases/yasm-'
            f'{self.yasm_version}.tar.gz')

        self.file_from_make = self.local_dir.joinpath('bin', 'yasm')

    def install(self):
        """
        Installs the YASM package
        """

        self.logger.info('Installing YASM')

        self.install_package(url=self.yasm_url,
                             file_from_make=self.file_from_make,
                             overwrite_on_exist=self.overwrite_on_exist)
        self.logger.info('Installation completed successfully')


class X264Installer(Installer):
    """
    Installer object for installing X264
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 log_path=Path(__file__).parents[1].joinpath('log', 'x264.log'),
                 overwrite_on_exist=False):
        """
        Gets the X264 version, sets the X264 url and calls the super
        constructor

        Parameters
        ----------
        config_path : Path or str
            The path to the get_configure_command file
        log_path : None or Path or str
            Path to the log file containing the log of Installer.
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=log_path)

        self.x264_version = self.config['versions']['x264']
        self.x264_url = (f'https://download.videolan.org/pub/videolan/x264/' 
                         f'snapshots/{self.x264_version}.tar.bz2')

        self.file_from_make = self.local_dir.joinpath('bin', 'x264')

        self.extra_config_options = \
            {'enable-static': None,
             'enable-shared': None,
             'extra-ldflags': f'L{self.local_dir.joinpath("lib")}',
             'extra-cflags': f'I{self.local_dir.joinpath("include")}'}

    def install(self):
        """
        Installs the X264 package
        """

        self.logger.info('Installing X264')

        self.install_package(url=self.x264_url,
                             file_from_make=self.file_from_make,
                             extra_config_option=self.extra_config_options,
                             overwrite_on_exist=self.overwrite_on_exist)
        self.logger.info('Installation completed successfully')
