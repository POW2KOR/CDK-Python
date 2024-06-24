# app.py
from aws_cdk import core
from my_cdk_project.cdk_pipeline.pipeline_stack import MyPipelineStack
# Import other stacks if needed

app = core.App()

# Instantiate your pipeline stack
pipeline_stack = MyPipelineStack(app, "MyPipelineStack")

# Synthesize and deploy your stacks
app.synth()
