# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Beast2(Package):
    """BEAST is a cross-platform program for Bayesian inference using MCMC
       of molecular sequences. It is entirely orientated towards rooted,
       time-measured phylogenies inferred using strict or relaxed molecular
       clock models. It can be used as a method of reconstructing phylogenies
       but is also a framework for testing evolutionary hypotheses without
       conditioning on a single tree topology."""

    homepage = "http://beast2.org/"
    url      = "https://github.com/CompEvol/beast2/releases/download/v2.4.6/BEAST.v2.4.6.Linux.tgz"

    version('2.4.6', 'b446f4ab121df9b991f7bb7ec94c8217')

    depends_on('java')

    def setup_environment(self, spack_env, run_env):
        run_env.set('BEAST', self.prefix)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('examples', join_path(self.prefix, 'examples'))
        install_tree('images', join_path(self.prefix, 'images'))
        install_tree('lib', prefix.lib)
        install_tree('templates', join_path(self.prefix, 'templates'))
