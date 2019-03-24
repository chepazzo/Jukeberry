Jukeberry Ansible Role
======================

This role will install Jukeberry on a Raspberry Pi running Raspbian.

Install
-------
1. Bootstrap your pi for use with Ansible
   a. You need a user:ansible with sudo perms
   b. You need to add your local key to the ansible user's
      authorized_keys.

3. Run ansible
   ```
   ansible-playbook -i <jukeberry IP>, jukeberry.yml
   ```
   Don't forget the `,` after the <jukeberry IP>.
4. Load Music Library
   Navigate to http://<jukeberry IP>:5000/loadcatalog

5. Enjoy
   Navigate to http://<jukeberry IP>:5000 and play some music!

