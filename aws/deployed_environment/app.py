#!/usr/bin/env python3

from aws_cdk import core

from deployed_environment.deployed_environment_stack import DeployedEnvironmentStack


app = core.App()
DeployedEnvironmentStack(app, "deployed-environment")

app.synth()
