from pathlib import Path
from src.Installer import Installer
from src.MPIInstaller import MPIInstaller


class PETScInstaller(Installer):
    """
    Installer object for installing PETSc
    """

    def __init__(self,
                 config_path=Path(__file__).parent.joinpath('config.ini'),
                 petsc_log_path=Path(__file__).parents[1].joinpath('log',
                                                                   'petsc.log'),
                 mpi_log_path=Path(__file__).parents[1].joinpath('log',
                                                                 'mpi.log'),
                 overwrite_on_exist=False):
        """
        Gets the version and url of PETSc and calls the super constructor

        The constructor will also make an object of the MPI installer and

        Parameters
        ----------
        config_path : Path or str
            The path to the get_configure_command file
        petsc_log_path : None or Path or str
            Path to the log file for PETSc
            If None, the log will directed to stderr
        mpi_log_path : None or Path or str
            Path to the log file for MPI
            If None, the log will directed to stderr
        overwrite_on_exist : bool
            Whether to overwrite the package if it is already found
        """

        self.overwrite_on_exist = overwrite_on_exist

        super().__init__(config_path=config_path, log_path=petsc_log_path)

        self.petsc_version = self.config['versions']['petsc']
        self.petsc_url = (f'http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/'
                          f'petsc-{self.petsc_version}.tar.gz')

        # Create dependency installer
        self.mpi = MPIInstaller(config_path=config_path,
                                log_path=mpi_log_path)

        self.file_from_make = self.local_dir.joinpath('bin', 'petsc-wisdom')

        self.extra_config_options = {'with-clanguage': 'cxx',
                                     'with-mpi': 1,
                                     'with-precision': 'double',
                                     'with-scalar-type': 'real',
                                     'with-shared-libraries': 0,
                                     'download-fblaslapack': 1,
                                     'download-f2cblaslapack': 1}

    @staticmethod
    def get_configure_command(config_options=None):
        """
        Get the command to configure the package.

        Notes
        -----
        Configuring happens through python 2
        https://github.com/petsc/petsc/blob/master/configure

        Parameters
        ----------
        config_options : dict
            Configuration options to use with `./configure`.
            The configuration options will be converted to `--key=val` during
            runtime

        Returns
        -------
        config_str : str
            The configuration command
        """

        options = ''
        if config_options is not None:
            for key, val in config_options.items():
                if val is not None:
                    options += f' --{key}={val}'
                else:
                    options += f' --{key}'

        config_str = f'python2 ./configure{options}'
        return config_str

    def make(self, path):
        """
        Make the package using make all and make test

        Parameters
        ----------
        path : Path or str
            Path to the get_configure_command file
        """

        make_options = (f'PETSC_DIR={self.local_dir}/petsc-{self.petsc_version}' 
                        f' PETSC_ARCH=arch-linux2-cxx-debug')

        make_all_str = f'make {make_options} all'
        self.run_subprocess(make_all_str, path)

        make_test_str = f'make {make_options} test'
        self.run_subprocess(make_test_str, path)

    def install(self):
        """
        Installs the MPI and the PETSc package
        """

        # Install dependencies
        self.mpi.install()

        self.logger.info('Installing PETSc')
        self.install_package(url=self.petsc_url,
                             file_from_make=self.file_from_make,
                             extra_config_option=self.extra_config_options,
                             overwrite_on_exist=self.overwrite_on_exist)
        self.logger.info('Installation completed successfully')
