# Ansible

An ansible playbook for deploying Praelatus

# How to Use

First change the appropriate environment variables in
`envfile.example` then source it using:

```bash
source envfile.example
```

Then set up the appropriate servers in your inventory file, there is
an example file in `inventory.example` that you can use as a reference.

You can then run the ansible playbook using `ansible-playbook`
