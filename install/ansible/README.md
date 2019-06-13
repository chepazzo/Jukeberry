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
   ```bash
   ansible-playbook -i -k -K {{ jukeberry IP }}, -e 'user={{ user }}' jukeberry.yml
   ```
   * Don't forget the `,` after the `{{ jukeberry IP }}`.
   * The `{{ user }}` is probably going to be `pi`
   e.g.
   ```bash
   ansible-playbook -k -K -i 192.168.0.200, -e 'user=pi' jukeberry.yml
   ```

4. Load Music Library
   Navigate to http://{jukeberry IP}:5000/loadcatalog

5. Enjoy
   Navigate to http://{jukeberry IP}:5000 and play some music!

