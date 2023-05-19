terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}
/* Variable Declarations */

variable "vpc_cidr" {
  type = string
}
variable "subnet_cidr" {
  type=string
  
}
variable "az" {
  type=string
}
variable "access_key" {
  type = string
}
variable "secret_key" {
  type=string
}
/* Variable Declarations */
provider "aws" {
  region = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}
/*
data "template_file" "user_data" {
  template = "${file("script.sh")}"
}
*/

resource "aws_vpc" "KCP_VPC" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  tags = {
    "name" = "KCP_VPC"
  }
}

resource "aws_subnet" "Public_KCP_Subnet1" {
    vpc_id = aws_vpc.KCP_VPC.id
    availability_zone = var.az
    cidr_block = var.subnet_cidr
    map_public_ip_on_launch = true
    tags = {
      "name" = "KCP_Public_Subnet"
    }
}
 
resource "aws_internet_gateway" "KCP_IG" {
    vpc_id = aws_vpc.KCP_VPC.id
    tags = {
      "name" = "KCP_Internet_Gateway"
    }
}

resource "aws_route_table" "Public_KCP_Route_Table" {
    vpc_id = aws_vpc.KCP_VPC.id
    route{
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.KCP_IG.id
    }
    tags = {
      "name" = "KCP_Public_Route_Table"
    }
}

resource "aws_route_table_association" "Public_KCP_Route_Table_Association" {
    subnet_id = aws_subnet.Public_KCP_Subnet1.id
    route_table_id = aws_route_table.Public_KCP_Route_Table.id
}

resource "aws_security_group" "KCP_SG1" {
    vpc_id = aws_vpc.KCP_VPC.id
    ingress{
        from_port = "5001"
        to_port = "5001"
        cidr_blocks = ["0.0.0.0/0"]
        protocol = "tcp"
    }
    ingress{
        from_port = "5050"
        to_port = "5050"
        cidr_blocks = ["0.0.0.0/0"]
        protocol = "tcp"
    }
    ingress{
        from_port = "3000"
        to_port = "3000"
        cidr_blocks = ["0.0.0.0/0"]
        protocol = "tcp"
    }
    ingress{
        from_port = "22"
        to_port = "22"
        cidr_blocks = ["0.0.0.0/0"]
        protocol = "tcp"
    }
    // Very Important - This is req since terraform does not follow the default security group setup behaviour ***
    egress {
     from_port   = 0
     to_port     = 0
     protocol    = "-1"
     cidr_blocks = ["0.0.0.0/0"]
   }
    tags={
        "name":"KCP_SG"
    }
  
}


resource "aws_instance" "KCP_Backend_Server" {
    ami = "ami-007855ac798b5175e"
    instance_type = "t2.micro"
    availability_zone = var.az
    subnet_id = aws_subnet.Public_KCP_Subnet1.id
    security_groups = [aws_security_group.KCP_SG1.id]
    root_block_device {
      volume_type           = "gp3"   # Replace with the desired volume type
      volume_size           = 20      # Replace with the desired volume size in GB
      delete_on_termination = true    # Optional: Specify if the volume should be deleted when the instance is terminated
    }
    
    user_data = "${file("script.sh")}"
    tags = {
      "name" = "KCP-Ec2-Server"
    }
}

output "server_ip" {
  value = "http://${aws_instance.KCP_Backend_Server.public_ip}:5000"
}
output "server_dns" {
  value = "http://${aws_instance.KCP_Backend_Server.public_dns}:5000"
  
}