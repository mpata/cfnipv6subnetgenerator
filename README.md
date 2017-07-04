# cfnipv6subnetgenerator

This is a very simple Lambda function to generate a list of valid subnets based on a IPv6 CIDR Block.

At the moment of this writing, there's no native solution in CloudFormation to create a *new* Stack with IPv6 CIDR Blocks associated with your subnets. This is due to the fact that the IPv6 CIDR block allocated to your VPC is dynamically assigned at creation time.

This is a simple solution to overcome this problem.


## AWS CloudFormation Custom Resource

### Example (Custom Resource)
```json
{
	"Type": "Custom::Ipv6SubnetGenerator",
	"Properties": {
		"ServiceToken": "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:<FUNCTION_NAME>",
		"Ipv6CidrBlock": {
			"Fn::Select": ["0", {
				"Fn::GetAtt": ["VPC", "Ipv6CidrBlocks"]
			}]
		},
		"Prefix": "64",
		"Count": 3
	}
}
```
### Properties
* ServiceToken: Lambda function ARN
* Ipv6CidrBlock: IPv6 CIDR Block allocated to your VPC (http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#w1ab2c19c12d333c13)
* Prefix: Desired subnet prefix length
* Count: Desired number of subnets

### Return Values
* List of subnets (length: Count)

## Usage
### Example (SubnetCidrBlock)
```json
{
	"Type": "AWS::EC2::SubnetCidrBlock",
	"Properties": {
		"Ipv6CidrBlock": {
			"Fn::Select": ["0", {
				"Fn::GetAtt": ["Ipv6SubnetGenerator", "Subnets"]
			}]
		},
		"SubnetId": {
			"Ref": "PublicSubnet"
		}
	}
}
```

## Installation/Usage
1. Create the Lambda function to be used as a CloudFormation Custom Resource
```shell
cd /tmp
git clone git@github.com:mpata/cfnipv6subnetgenerator.git
cd /tmp/cfnipv6subnetgenerator
pip install -t . -r requirements.txt
zip -j /tmp/cfnipv6subnetgenerator.zip /tmp/cfnipv6subnetgenerator
aws lambda create-function --function-name CFNIPv6SubnetGenerator \
			   --runtime python2.7			  \
			   --handler ipv6subnets.lambda_handler   \
			   ...
			   ...
```
2. In your CloudFormation template add a Custom Resource like in the example above
3. You can now use the 'Fn::Select' intrinsic function to select a generated subnet from the CustomResource you've just created.
