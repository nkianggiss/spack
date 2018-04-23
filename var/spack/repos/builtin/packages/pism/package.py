##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Pism(CMakePackage):
    """Parallel Ice Sheet Model"""

    homepage = "http://pism-docs.org/wiki/doku.php:="
    url      = "https://github.com/pism/pism/tarball/v123"
    # https://github.com/pism/pism/archive/v0.7.3.tar.gz

    maintainers = ['citibeth']

    version('0.7.3', '7cfb034100d99d5c313c4ac06b7f17b6')

    version('0.7.x', git='https://github.com/pism/pism.git',
        branch='stable0.7')

    version('glint2', git='https://github.com/pism/pism.git',
        branch='efischer/glint2')

    version('dev', git='https://github.com/pism/pism.git',
        branch='dev')

    variant('extra', default=False,
            description='Build extra executables (testing/verification)')
    variant('shared', default=True,
            description='Build shared Pism libraries')
    variant('python', default=False,
            description='Build python bindings')
    variant('icebin', default=False,
            description='Build classes needed by IceBin')
    variant('proj', default=True,
            description='Use Proj.4 to compute cell areas, '
            'longitudes, and latitudes.')
    variant('parallel-netcdf4', default=False,
            description='Enables parallel NetCDF-4 I/O.')
    variant('parallel-netcdf3', default=False,
            description='Enables parallel NetCDF-3 I/O using PnetCDF.')
    variant('parallel-hdf5', default=False,
            description='Enables parallel HDF5 I/O.')
    # variant('tao', default=False,
    #         description='Use TAO in inverse solvers.')
    variant('doc', default=False,
            description='Build PISM documentation (requires LaTeX and Doxygen)')
    variant('examples', default=False,
            description='Install examples directory')
    variant('everytrace', default=False,
            description='Report errors through Everytrace (requires Everytrace)')

    # CMake build options not transferred to Spack variants
    # (except from CMakeLists.txt)
    #
    # option (Pism_TEST_USING_VALGRIND "Add extra regression tests
    #         using valgrind" OFF)
    # mark_as_advanced (Pism_TEST_USING_VALGRIND)
    #
    # option (Pism_ADD_FPIC "Add -fPIC to C++ compiler flags
    #         (CMAKE_CXX_FLAGS). Try turning it off if it does not work." ON)
    # option (Pism_LINK_STATICALLY
    #         "Set CMake flags to try to ensure that everything is
    #         linked statically")
    # option (Pism_LOOK_FOR_LIBRARIES
    #         "Specifies whether PISM should look for libraries. (Disable
    #         this on Crays.)" ON)
    # option (Pism_USE_TR1
    #        "Use the std::tr1 namespace to access shared pointer
    #        definitions. Disable to get shared pointers from the std
    #        namespace (might be needed with some compilers)." ON)
    # option (Pism_USE_TAO "Use TAO in inverse solvers." OFF)

    depends_on('fftw')
    depends_on('gsl')
    depends_on('mpi')
    depends_on('netcdf')    # Only the C interface is used, no netcdf-cxx4
#    depends_on('petsc', when='@0:')
    depends_on('petsc')
#    depends_on('petsc@3.4.5~superlu-dist', when='@glint2')
    depends_on('udunits2')
    depends_on('proj')
    depends_on('everytrace', when='+everytrace')

    extends('python', when='+python')
    depends_on('python@2.7', when='+python')
    depends_on('py-matplotlib', when='+python')  # Implies py-numpy too

    depends_on('cmake', type='build')

    def cmake_args(self):
        spec = self.spec

        return [
            '-DPism_BUILD_EXTRA_EXECS=%s' %
            ('YES' if '+extra' in spec else 'NO'),
            '-DBUILD_SHARED_LIBS=%s' %
            ('YES' if '+shared' in spec else 'NO'),
            '-DPism_BUILD_PYTHON_BINDINGS=%s' %
            ('YES' if '+python' in spec else 'NO'),
            '-DPism_BUILD_ICEBIN=%s' %
            ('YES' if '+icebin' in spec else 'NO'),
            '-DPism_USE_PROJ4=%s' %
            ('YES' if '+proj' in spec else 'NO'),
            '-DPism_USE_PARALLEL_NETCDF4=%s' %
            ('YES' if '+parallel-netcdf4' in spec else 'NO'),
            '-DPism_USE_PNETCDF=%s' %
            ('YES' if '+parallel-netcdf3' in spec else 'NO'),
            '-DPism_USE_PARALLEL_HDF5=%s' %
            ('YES' if '+parallel-hdf5' in spec else 'NO'),
            '-DPism_BUILD_PDFS=%s' %
            ('YES' if '+doc' in spec else 'NO'),
            '-DPism_INSTALL_EXAMPLES=%s' %
            ('YES' if '+examples' in spec else 'NO'),
            '-DPism_USE_EVERYTRACE=%s' %
            ('YES' if '+everytrace' in spec else 'NO')]

    def install_install(self):
        make = self.make_make()
        with working_dir(self.build_directory, create=False):
            make('install')

    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
        env.set('PISM_PREFIX', self.prefix)
        env.set('PISM_BIN', join_path(self.prefix, 'bin', ''))


# From email correspondence with Constantine Khroulev:
#
# > Do you have handy a table of which versions of PETSc are required
# > for which versions of PISM?
#
# We don't. The installation manual [1] specifies the minimum PETSc
# version for the latest "stable" release (currently PETSc 3.3). The
# stable PISM version should support all PETSc versions starting from the
# one specified in the manual and up to the latest PETSc release.
#
# The current development PISM version should be built with the latest
# PETSc release at the time (the "maint" branch of PETSc).
#
# Thanks to Git it is relatively easy to find this info, though:
#
# | PISM version | PETSc version |
# |--------------+---------------|
# |          0.7 | 3.3 and later |
# |          0.6 | 3.3           |
# |       new_bc | 3.4.4         |
# |          0.5 | 3.2           |
# |          0.4 | 3.1           |
# |          0.3 | 2.3.3 to 3.1  |
# |          0.2 | 2.3.3 to 3.0  |
# |          0.1 | 2.3.3-p2      |