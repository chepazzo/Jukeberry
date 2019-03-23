Jukeberry Ansible Role
======================

This role will install Jukeberry on a Raspberry Pi running Raspbian.

Install
-------
1. Bootstrap your pi for use with Ansible
   a. You need a user:ansible with sudo perms
   b. You need to add your local key to the ansible user's
      authorized_keys.

2. Update the `hosts` file
   You want to make sure that your target pi is listed
   in the `[Jukeberry]` group.

3. Run ansible
   ```
   ansible-playbook -i hosts jukeberry.yml
   ```
4. Load Music Library
   Navigate to http://<jukeberry ip addr>:5000/loadcatalog

5. Enjoy
   Navigate to http://<jukeberry ip addr>:5000 and play some music!

