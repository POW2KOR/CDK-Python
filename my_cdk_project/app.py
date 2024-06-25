from aws_cdk import App
from cdk_pipeline.pipeline_stack import MyPipelineStack

app = App()
MyPipelineStack(app, "MyPipelineStack")
app.synth()
