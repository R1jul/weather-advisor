provider "aws" {
    region = "ap-south-1"
}

resource "aws_key_pair" "dev_key" {
    key_name = "devops-key"
    public_key = file("mykey.pub")
}

resource "aws_security_group" "flask_sg" {
    name_prefix = "weather_sg"
    description = "Allow Flask and SSH"

    ingress {
        from_port = 5000
        to_port = 5000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
} 

resource "aws_instance" "flask_server" {
    ami = "ami-0d176f79571d18a8f"   
    instance_type = "t2.micro"
    key_name=aws_key_pair.dev_key.key_name
    vpc_security_group_ids = [aws_security_group.flask_sg.name]
    
    user_data= <<-EOF
    #!/bin/bash
    yum update -y
    yum install docker -y
    service docker start
    docker run -d -p5000:5000 --name weather_app\
    -e WEATHER_API_KEY=${var.weather_api_key}${var.docker_image}


    EOF

    tags = {
        Name = "WeatherAdvisorServer"
    }
} 



