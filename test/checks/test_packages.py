#!/usr/bin/env python3
##
# Validation Tests: Packages
##
import pytest


@pytest.mark.parametrize('pkg', ['bash'])
def test_package_present(host, pkg):
    '''Verify specific packages are present on the system '''
    assert host.package(pkg).is_installed


@pytest.mark.parametrize('pkg', ['nano', 'apache2', 'vim-tiny'])
def test_package_absent(host, pkg):
    '''Verify specific packages are absent on the system'''
    assert not host.package(pkg).is_installed
