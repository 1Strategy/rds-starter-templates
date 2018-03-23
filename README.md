# 1Strategy AWS VPC template

This RDS MySQL template is a complete CloudFormation template to provision a MySQL RDS database instance.

"Public" means subnets can receive traffic directly from the Internet. Traffic outbound from a public subnet usually goes through an Internet Gateway. "Private" means that a subnet cannot receive traffic directly from the Internet. Traffic outbound from a private subnet usually goes through a NAT Gateway.


## Template Parameters

To deploy this VPC template, you'll need to know the VPC CIDR block, the three public, and three private subnet CIDR blocks.

| Parameter                 | Description                  | Example      |
|---------------------------|------------------------------|--------------|
| _VpcCidrParam_            | IPv4 CIDR block (/16 to /28) | 10.0.0.0/16  |
| _PublicAZASubnetBlock_    | AZ A public subnet block     | 10.0.32.0/20 |
| _PublicAZBSubnetBlock_    | AZ B public subnet block     |      ""      |
| _PublicAZCSubnetBlock_    | AZ C public subnet block     |      ""      |
| _PrivateAZASubnetBlock_   | AZ A private subnet block    | 10.0.64.0/19 |
| _PrivateAZBSubnetBlock_   | AZ B private subnet block    |      ""      |
| _PrivateAZCSubnetBlock_   | AZ C private subnet block    |      ""      |


To make it easier to specify these parameters on the command line, you can use the example Parameters files included in the `parameters/` directory.

## How to Deploy

### Prerequisites

If you'd like to deploy this stack via the command line, you'll need the AWS CLI.

### Validate/Lint Stack

```shell
aws cloudformation validate-template --template-body file://rds-mysql.yml
```

### Deploy Stack

You will need to verify you have the appropriate parameters file for environment you want to deploy to. See `./parameters/<env>.json`. For example `parameters/dev.json`.

```shell
aws cloudformation create-stack --template-body file://rds-mysql.yml --stack-name mysql-db --parameters file://parameters/dev.json
```

### Update Stack

```shell
aws cloudformation update-stack --template-body file://rds-mysql.yml --stack-name mysql-db --parameters file://parameters/dev.json
```

## Template Outputs/Exports

AWS CloudFormation supports [exporting Resource names and properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-exports.html). You can import these [Cross-Stack References](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-importvalue.html) in other templates.

This VPC template exports the following values for use in other CloudFormaton templates. Each export is prefixed with the **Stack Name**. For example, if you name the stack "main-vpc" when you launch it, the VPC's public route table will be exported as "_main-vpc-public-rtb_"

| Export                         | Description                                          | Example         |
|--------------------------------|------------------------------------------------------|-----------------|
| _main-vpc-VpcId_               | VPC Id                                               | vpc-1234abcd    |
| _main-vpc-public-rtb_          | Public Route table Id (shared by all public subnets) | rtb-1234abcd    |
| _main-vpc-public-AZ-A-subnet_  | AZ A public subnet Id                                | subnet-1234abcd |
| _main-vpc-public-AZ-B-subnet_  | AZ B public subnet Id                                |        ""       |
| _main-vpc-public-AZ-C-subnet_  | AZ C public subnet Id                                |        ""       |
| _main-vpc-private-AZ-A-subnet_ | AZ A private subnet Id                               | subnet-abcd1234 |
| _main-vpc-private-AZ-B-subnet_ | AZ A private subnet Id                               |        ""       |
| _main-vpc-private-AZ-C-subnet_ | AZ A private subnet Id                               |        ""       |
| _main-vpc-private-AZ-A-rtb_    | Route table for private subnets in AZ A              | rtb-abcd1234    |
| _main-vpc-private-AZ-B-rtb_    | Route table for private subnets in AZ B              |        ""       |
| _main-vpc-private-AZ-C-rtb_    | Route table for private subnets in AZ C              |        ""       |

## License

Licensed under the Apache License, Version 2.0.