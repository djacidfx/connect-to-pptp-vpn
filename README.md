# connect to pptp vpn
Sometimes it is necessary to change IP with VPN to perform data mining or scraping or sending consecutive requests.

This Python code does this for Linux servers. For this, this code does not need to be executed on the target server, it can be done from any computer connected to the Internet.

To do this, first, it connects to the target server using the paramiko library, and after creating the file and making the required settings, it connects the target server to the VPN by ssh.

Note: To do this, you must have pptp installed on the target server (Linux server). 
