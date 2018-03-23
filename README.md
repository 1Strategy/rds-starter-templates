# 1Strategy AWS RDS starter templates

This set of templates are a complete set of CloudFormation templates to build out a AWS RDS instances in a secure manner by provisioning an SSM parameter and encrypting it with an KMS key. A password is randomly generated and placed in the encrypted SSM parameter and also applied to the RDS instance as the master password. 

Please see the diagram for a visual representation of the resources provisioned. 

## AWS RDS Starter Solutions 

Since AWS RDS suppports for provisioning various engine types, three solutions were created to support the specific demands of each engine type. Therefore, Aurora, SQL Sever, and Open Source (mysql, mariadb, and postgresql) databases have their own folder. The solutions are extremely similiar but do require different parameters depending on the database engine chosen.   

---

## AWS RDS Starter Template Parameters

To deploy this AWS RDS template, you'll need to provide several parameters depending on which database engine chosen.

| Parameter                 | Description                                      | Example      | Required for Aurora |Required for SQL Server | Required for Open Source Databases | 
|---------------------------|------------------------------|--------------|----------------------|------------------------|------------------------------------|
| AllocatedStorage            |  The allocated storage size, specified in gigabytes (GB) | 20  | No | Yes | Yes |
| AllowMajorVersionUpgrade    | If you update the EngineVersion property to a version that's different from the DB instance's current major version, set this property to true.     | False | Yes | Yes | Yes |
| AutoMinorVersionUpgrade    | Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. The default value is true.   |      True      | Yes | Yes | Yes |
| BackupRetentionPeriod    | The number of days during which automatic DB snapshots are retained. |      7      | Yes | Yes | Yes |
| DBInstanceClass   | The name of the compute and memory capacity classes of the DB instance.   |  db.t2.medium  | Yes | Yes | Yes |
| DBName   | The name of the database inside the instance.    |     mysqldb     | Yes | No | Yes |
| DBClusterIdentifier   | Name of the database cluster.  |      auroracluster      | No | No | Yes |
| Engine   | The name of the database engine to be used for this instance. |      mysql      | Yes | Yes | Yes |
| DBSubnetGroupName   | A DB subnet group to associate with the DB instance.    |      default-vpc-85fe97e3      | Yes | Yes | Yes |
| VPCSecurityGroups   | Specifies if the database instance is a multiple Availability Zone deployment.  |      sg-dfca07a2, sg-a7c805da      | Yes | Yes | Yes |
| MasterUsername   |  The master user name for the DB instance. |      mysql-master      | Yes | Yes | Yes |
| MultiAZ   | Specifies if the database instance is a multiple Availability Zone deployment.    |      True      | No | Yes* | Yes |
| SSMParameterName   | Parameter name under which to store the master password for the RDS instace.   |      RDSMasterPassword      | Yes | Yes | Yes |
| IAMRoleName   | Name of the IAM Role that should be used when creating the IAM Role that Lambda functions will be assuming.  |      RDS-Starter-Template-LambdaExecutionRole      | Yes | Yes | Yes |
| IAMManagedPolicyName   |  Name of the IAM policy that will be created that allows users to decrypt SSM RDS Master password parameter.   |      GrantUsageKMSKey      | Yes | Yes | Yes |
| RDSInstanceTemplateURL   | RDS Instance Nested Stack Template URL    |      https://s3-us-west-2.amazonaws.com/pavelyarema-public/aurora-rds-instance.yml      | Yes | Yes | Yes |


*SQL Server Express and Web Editions are not eligible for Multi-AZ. In this case, the parameter is ignored. 

Each database engine has diverse limitations, such as the ability to deploy Multi-AZ, storage requirements, and instance class requirements. The solutions was designed accomodate majority of these requirements and limitation. However, I would strongly suggest referencing the RDS API reference to fully understand all limitations of each database engine. https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html


To make it easier to specify these parameters on the command line, you can use the example Parameters files included in the `parameters/` directory in each of the solutions.

## How to Deploy

NOTE: The following shows how to deploy open-source RDS instance but the process to provision Aurora and or SQL Server is the same.

### Prerequisites

1) If you'd like to deploy this stack via the command line, you'll need the AWS CLI.
2) The appropriate rds-instance.yml has to be stored in a publicly accessible S3 bucket since the rds-starter-template.yml will need to reference the template. For example, if you are provisioning a mysql rds instance, upload the opensource-rds-instance.yml to a publically accessible s3 location. The url of the opensource-rds-instance.yml file will be placed in the RDSInstanceTemplateURL parameter in the opensource-rds-starter-template.yml CloudFormation template.  


### Validate/Lint Stack

```shell
aws cloudformation validate-template --template-body file://opensource-rds-starter-template.yml
```

### Deploy Stack

You will need to verify you have the appropriate parameters file for the AWS Region and account/environment you want to deploy to. See `./parameters/<region>/<acct>.json`. For example `parameters/us-west-2/dev.json`.

```shell
aws cloudformation create-stack --template-body file://opensource-rds-starter-template.yml --stack-name rdsmysql --parameters file://parameters/us-west-2/dev.json
```

### Update Stack

```shell
aws cloudformation update-stack --template-body file://opensource-rds-starter-template.yml --stack-name rdsmysql --parameters file://parameters/us-west-2/dev.json
```

## Template Outputs/Exports

AWS CloudFormation supports [exporting Resource names and properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-exports.html). You can import these [Cross-Stack References](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-importvalue.html) in other templates.

In each solutions, the RDS instance template (executed as a nested stack from the rds-starter-template) exports the following values for use in other CloudFormaton templates. Each export (except in the SQL Server solution) is prefixed with the **Stack Name**, **Engine**, and **DBName**. In the SQL Server solution, the exports are prefixed with only **Stack Name** and **Engine**. For example, if you name the stack "rdsmysql", running "mysql" engine and specify the DBName to be "mysqldb" when you launch it, the RDS instance endpoint will be exported as "_rdsmysql-mysql-mysqldb-endpoint_". If you name the stack "sqlserver", running "sqlserver-ex", the RDS endpoint will be "_sqlserver-sqlserver-ex-endpoint_". 


### Open-Source Databases Export Values:
| Export                         | Description                                          | Example         |
|--------------------------------|------------------------------------------------------|-----------------|
| _DBEndpoint_               | The connection endpoint for the database.	 | ss1c00eft3fv646.cqdrcz4yja3d.us-west-2.rds.amazonaws.com    |
| _DBInstanceIdentifier_          | RDS Instance ID	 | ss1c00eft3fv646    |
| _DBPort_  | The port number on which the database accepts connections.	 | 3306 |

### Aurora Export Values
| Export                         | Description                                          | Example         |
|--------------------------------|------------------------------------------------------|-----------------|
| _DBEndpoint_               | The connection endpoint for the database.	 | ss1c00eft3fv646.cqdrcz4yja3d.us-west-2.rds.amazonaws.com    |
| _DBInstanceIdentifier_          | RDS Instance ID	 | ss1c00eft3fv646    |
| _DBPort_  | The port number on which the database accepts connections.	 | 3306 |
| _RREndpoint_               | The connection endpoint for the read-replica database.	 | ""   |
| _RRInstanceIdentifier_          | Read-replica RDS Instance ID	 | ""    |
| _RRPort_  | The port number on which the read-replica database accepts connections.	 | "" |

### SQL Server Export Values:


#### SQL Server Express and Web Editions
| Export                         | Description                                          | Example         |
|--------------------------------|------------------------------------------------------|-----------------|
| _DBInstanceIdentifierLowerEditions_               | The connection endpoint for the database.	 | ss1c00eft3fv646.cqdrcz4yja3d.us-west-2.rds.amazonaws.com    |
| _DBEndpointLowerEditions_          | RDS Instance ID	 | ss1c00eft3fv646    |
| _DBPortLowerEditions_  | The port number on which the database accepts connections.	 | 1433 |


#### SQL Server Enteprise and Standard Editions
| Export                         | Description                                          | Example         |
|--------------------------------|------------------------------------------------------|-----------------|
| _DBInstanceIdentifierHigherEditions_               | The connection endpoint for the database.	 | ss1c00eft3fv646.cqdrcz4yja3d.us-west-2.rds.amazonaws.com    |
| _DBEndpointHigherEditions_          | RDS Instance ID	 | ss1c00eft3fv646    |
| _DBPortHigherEditions_  | The port number on which the database accepts connections.	 | 1433 |




## License

Licensed under the Apache License, Version 2.0.