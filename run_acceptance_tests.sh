#!/usr/bin/env bash

# Deploy package caipirinha_cmdtools to test PyPI
# Create new (temporary) virtual env
# Install package: pip install caipirinha_cmdtools
# Run acceptance tests
# Delete virtual env

function DeployToTestPyPI {
    echo "Deploying package..."
}

function CreateTemporaryVirtualEnvironment {
    echo "Creating virtual env..."
    python -m venv /tmp/caipirinha_cmdtools_venv
    source /tmp/caipirinha_cmdtools_venv/bin/activate
    python -m pip install --upgrade pip
}

function InstallPackage {
    echo "Installing package..."
    python -m pip install caipirinha_cmdtools
}

function RunAcceptanceTests {
    echo "Running acceptance tests..."
    python -m pytest ./tests
}

function DeleteTemporaryVirtualEnvironment {
    echo "Deleting virtual env..."
    deactivate
    rm -rf /tmp/caipirinha_cmdtools_venv
}

DeployToTestPyPI
CreateTemporaryVirtualEnvironment
InstallPackage
RunAcceptanceTests
DeleteTemporaryVirtualEnvironment

exit 0
