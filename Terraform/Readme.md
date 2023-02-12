### Terraform Infra Setup 
* Install Terraform Libraries
```
terraform init
```
* Create Infra
```
terraform apply
```
* Destroy Infra
```
terraform destroy
```
### What we are doing: 

* Creating a VPC
    * Creating Subnet in an availiblity-zone - Public Ip enabled on creation
    * Creating an Internet Gateway
    * Creating Route Table and route entry with Internet Gateway
    * Associating Public Subnet with Route Table
* Creating a security group in specified subnet
* Spinning up the EC2 Instance with the bootstrap script
* Public Server and Public DNS as Output, with correct format to directly access the server