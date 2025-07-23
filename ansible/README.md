Ansible
=======

Ansible is used to deploy and maintain Recovery Source servers.
This allows us to ensure security standards are enforced while
also ensuring that we maintain complete transparency--anyone is
free/encouraged to build their own local copy of our services and
to report any potential concerns.

Usage
-----

Deploy New Server:
```
# Log in to new server
wget https://raw.githubusercontent.com/recoverysource/services/refs/heads/release/ansible/bootstrap
bash bootstrap
```

This will install a cron task that periodically synchronizes the
server with any repository updates.

Manually push changes (Automatic Sync Will Destroy Local Changes):
```
ansible-playbook -K -l <IP> -i <IP>, maintenance.yml
# Note: The trailing comma is required without an inventory file
```

Testing
-------

From repository root:
```
make test
```

This command will:

1. Generate an initial test image (pre-install large packages)
2. Deploy this new container (using podman)
3. Run ``test/docker/test.sh``
4. Report results of the test

This will be repeated for all supported test distributions (Debian, Ubuntu, Redhat).
To run tests for a specific OS, append the OS, ex. ``make test-debian``.

Development
-----------

The command ``make login-<distro>`` starts a container and logs in; the test
script will not be executed. Once logged in, this can be invoked manually using:
```
/srv/services/test/docker/test.sh
```

At this point, the container will be a perfect replica of any sober.page service.
