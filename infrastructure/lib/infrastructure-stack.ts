import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import * as apiGateway from 'aws-cdk-lib/aws-apigateway'
import * as dotenv from "dotenv"

dotenv.config()

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const layer = new lambda.LayerVersion(this, "BaseLayer", {
      code: lambda.Code.fromAsset("lambda_base_layer/layer.zip"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_10],
    });

    const apiLambda = new lambda.Function(this, "ApiFunction", {
      runtime: lambda.Runtime.PYTHON_3_10,
      code: lambda.Code.fromAsset("../app/"),
      handler: "api.handler",
      layers: [layer],
      environment: {
        "OPENAI_API_KEY": process.env.OPENAI_API_KEY ?? "",
      },
    });


    const api = new apiGateway.RestApi(this, "RestAPI", {
      restApiName: "Revenuro API",
    });

    api.root.addProxy({
      defaultIntegration: new apiGateway.LambdaIntegration(apiLambda)
    });
  }
}
