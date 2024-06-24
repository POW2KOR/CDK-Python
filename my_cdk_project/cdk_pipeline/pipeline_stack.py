# cdk_pipeline/pipeline_stack.py
from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as actions
from aws_cdk import aws_codebuild as codebuild

class MyPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define source and build artifacts
        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        # Define CodeBuild project
        build_project = codebuild.PipelineProject(self, "BuildProject",
            build_spec=codebuild.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'build': {
                        'commands': [
                            'echo Build completed on `date`',
                            'mvn package'
                        ]
                    }
                },
                'artifacts': {
                    'files': [
                        '**/*'
                    ]
                }
            })
        )

        # Define CodePipeline
        pipeline = codepipeline.Pipeline(self, "MyPipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        actions.GitHubSourceAction(
                            action_name="GitHub_Source",
                            owner="your-github-owner",
                            repo="your-repo",
                            oauth_token=core.SecretValue.secrets_manager("your-github-token"),
                            output=source_output,
                            branch="master"
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        actions.CodeBuildAction(
                            action_name="CodeBuild",
                            project=build_project,
                            input=source_output,
                            outputs=[build_output]
                        )
                    ]
                )
            
            ]
        )
