
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

[cc-by-nc-sa]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://mirrors.creativecommons.org/presskit/buttons/80x15/svg/by-nc-sa.svg

# Adv-Reinforcement-Learning-Workshop
All the necessary files and notebooks for hosting a Reinforcement Learning workshop on AWS, maintained by 310zzj

## AWS

### Setup

A predefined AWS Image is used to create a docker container with the reinforcement learning environment and automatically launching a Jupyter Notebook on port 8888. To access this notebook, a link is generated which holds the corresponding IP, port and token.

### Steps to launch instances for the WS

1. Select the number of instances you want to start
2. Paste in the user data
3. Attach the right network security group (that opens port 8888) and IAM role (to grant write access to s3)

### Visualization
Visualizations in the DQN-notebooks are only supported for Linux and OSX, as well as headless Linux servers such as an AWS EC2 Linux instance.