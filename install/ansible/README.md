Jukeberry Ansible Deployment
==========================

This directory contains an Ansible role to deploy the Jukeberry application on a Debian-based system (like Raspbian).

## Features

- Installs system dependencies (Python, pip, git, and the selected player).
- Creates a dedicated user and group to run the application.
- Deploys the application from a Git repository or a local source directory.
- Installs Python dependencies from `requirements.txt`.
- Creates a configurable `jukeberry.conf` file from a template.
- Sets up and enables a `systemd` service to manage the application.

## Role Variables

The deployment can be customized by setting the following variables. The defaults are defined in `roles/jukeberry/defaults/main.yml`.

| Variable                  | Default                                       | Description                                                                 |
| ------------------------- | --------------------------------------------- | --------------------------------------------------------------------------- |
| `jukeberry_user`          | `"pi"`                                        | The system user to run the Jukeberry service as.                            |
| `jukeberry_group`         | `"pi"`                                        | The system group for the Jukeberry service.                                 |
| `jukeberry_install_dir`   | `"/opt/jukeberry"`                            | The directory to install the application into.                              |
| `jukeberry_repo_src`      | `"https://github.com/chepazzo/jukeberry.git"` | The source Git repository to clone.                                         |
| `jukeberry_repo_version`  | `"main"`                                      | The branch, tag, or commit to check out.                                    |
| `jukeberry_local_install` | `false`                                       | Set to `true` to install from a local path instead of Git.                  |
| `jukeberry_local_path`    | `"/path/to/local/jukeberry/repo"`             | The local source directory to copy from when `jukeberry_local_install` is `true`. |
| `music_library_path`      | `"/var/media/music"`                          | The path to the music library on the target machine.                        |
| `jukeberry_player`        | `"mpg321"`                                    | The audio player to use (e.g., `mpg321`, `omxplayer`).                      |
| `jukeberry_config_file`   | `"/etc/jukeberry.conf"`                       | The path to the generated application configuration file.                   |

## Usage

1.  **Create an Inventory File:**

    Create an `inventory` file (e.g., `hosts`) to define the target machine(s).

    ```ini
    [jukeberry_servers]
    your_raspberry_pi_ip ansible_user=pi
    ```

2.  **Create a Playbook:**

    Create a playbook file (e.g., `playbook.yml`) to apply the role.

    ```yaml
    - hosts: jukeberry_servers
      become: true
      roles:
        - role: jukeberry
          # Optionally override default variables here
          # jukeberry_player: "omxplayer"
    ```

3.  **Run the Playbook:**

    Execute the playbook from the `ansible` directory:

    ```bash
    ansible-playbook -i hosts playbook.yml
    ```

4. Load Music Library
   Navigate to http://{jukeberry IP}:5000/loadcatalog

5. Enjoy
   Navigate to http://{jukeberry IP}:5000 and play some music!
