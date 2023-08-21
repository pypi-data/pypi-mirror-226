# Requirements
   - terraform v1.1.4+
   - ansible 2.10.7+
   - python3 3.8+

# Purpose

Provisions an instance on using terraform and calls ansible playbooks specified in 
the yaml config file. See `config.yaml.sample`, the `aws` directory for sample terraform 
script and `stage.yaml` for sample ansible playbook. 

```
python3 -m pip install . 
cp ./config.yaml.sample config.yaml   # Modify as needed ssh keys, ...

# Usage
go-deploy -h

# Init 
go-deploy -d aws -init

# Deploy 
go-deploy -d aws -w <workspace> -c config.yml -verbose 
go-deploy -d aws -w <workspace> -show 
go-deploy -d aws -w <workspace> -output

# Tear Dow
go-deploy -d aws -w <workspace> -destroy -verbose 
```
