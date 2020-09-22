# Deploying the application

## Pre-requisites

Hopefully the following steps will be automated in a future version.

### AWS

Create the deployment pipeline using the following steps:

- Navigate to ECR
- Create a repository called `autistica-prototype`
- Navigate to CodePipeline
- Create a pipeline called `autistica-prototype`
- Keep **New service role** selected. Click **Next**
- In **Add source stage**, set up connection to GitHub repo. Click **Next**
- In **Add build stage**, select **AWS CodeBuild** and click **Create project**. This opens a new window for CodeBuild
- In the new window (**Create build project**), fill in details
- In the **Environment** section, keep **New service role** selected, and make a note of the **Role name**
- In the **Environment** section, expand **Additional configuration**
- Add the following environment variables:

```
AWS_DEFAULT_REGION=<region>
AWS_ACCOUNT_ID=<account-id>
IMAGE_TAG=latest
IMAGE_REPO_NAME=autistica-prototype
```

- Under **Buildspec** keep **Use a buildspec file** selected. This uses the build steps defined in `./buildspec.yml`
- Click **Continue to CodePipeline**
- This will close the **Create build project** window, and should take you back to the **Add build stage** window
(if it doesn't take you back, navigate back to the previous window yourself)
- Back in the **Add build stage** window, click **Next** 
- In **Add deploy stage**, click **Skip deploy stage**. A popup will ask if you want to do this - click **Skip**
- In **Review**, click **Create pipeline**
- Navigate to IAM
- Find the service role you made a note of when setting up the CodeBuild project
- Create a new inline policy with the following settings:

```json
{
    "Statement": [
        {
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ],
    "Version": "2012-10-17"
}
```

Now, whenever someone pushes to the GitHub branch specified in the setup, the build will run, create a new Docker
image, and push that image to ECR.

### Local machine

Set up your machine so you can create the runtime stack using the following steps:

- Install python
- Install AWS CLI
- Install AWS CDK
- Ensure the CLI is using the account / credentials you want


## Create the runtime stack from your local machine

For the following to work, there **must** be at least one docker image in the ECR repo. So if the build hasn't run,
trigger it manually.

From the repo root, run the following commands:

```bash
cd aws/deployed_environment
. ./.env/bin/activate
pip install -r requirements.txt
cdk deploy
```

You now have a runtime environment using the a Docker image of the latest version of the code. The publicly-accessible
URL is printed in the terminal, and will be something along the lines of
http://deplo-autis-AA2EHG3N73H0-1776356449.eu-west-2.elb.amazonaws.com. Note that it may take a minute for the 
container to spin-up, but otherwise you should be good to go.


## Deploying a new version

The build pipeline does not include an auto-deploy step. This has to be done manually. To deploy a new version
of the app, do the following:

- Push the code to GitHub
- The build will automatically trigger. Wait for the build to complete and push a new Docker image to ECR
- Navigate to ECS
- Find the cluster, and under **Services**, click the service
- On the service page, click **Update**
- Select **Force new deployment**
- Click **Skip to review**
- Click **Update Service**
- Wait for the new task to spin up
