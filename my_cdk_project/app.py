# app.py
from aws_cdk import core
from cdk_pipeline.pipeline_stack import MyPipelineStack

app = core.App()
MyPipelineStack(app, "MyPipelineStack")
app.synth()
