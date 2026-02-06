# Server

The CI is running on a hetzner VPS follow those instrucitons on how to setup a ssh connection to it.

## Connect

First you need to create a keyfile run 
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
and follow the instructions.
Then send the public key file to Anton via discord.

After Anton added it you can connect to the server using 
```bash
ssh root@77.42.84.29
```

Then you should be able to run commands
the git repo is cloned in `DD2480/DD2480-Basic-CI-Pipeline`