from time import sleep
import paramiko


class VPNConnection:
    def __init__(self):
        print('functions are: connect, create, disconnect\n')
        self.function = input('please insert function:')
        self.vpn_main_config_text = """pty "pptp {} --nolaunchpppd --debug"
name {}
password {}
remotename PPTP
require-mppe-128
require-mschap-v2
refuse-eap
refuse-pap
refuse-chap
refuse-mschap
noauth
debug
persist
maxfail 0
defaultroute
replacedefaultroute
usepeerdns
"""
        self.operations()

    # vpn host , username, password, filename
    def operations(self):
        if self.function == "create":
            vpn_host = input('import vpn host name/ip: ')
            vpn_username = input('import vpn host username: ')
            vpn_password = input('import vpn host password: ')
            vpn_filename = input('import vpn filename: ')

            target_host = input('import target host name/ip: ')
            target_username = input('import target host ssh username: ')
            target_password = input('import target host ssh password: ')

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target_host, 22, username=target_username, password=target_password)
            sftp = ssh.open_sftp()
            file = sftp.file(vpn_filename, 'w', -1)
            file.write(self.vpn_main_config_text.format(vpn_host, vpn_username, vpn_password))
            file.flush()
            sftp.close()

            stdin, stdout, stderr = ssh.exec_command("sudo -S cp {} /etc/ppp/peers/".format(vpn_filename))
            stdin.write(vpn_password + '\n')
            stdin.flush()
            sleep(1)
            stdin, stdout, stderr = ssh.exec_command(
                "sudo -S chmod 600 /etc/ppp/peers/{}".format(vpn_filename))
            stdin.write(vpn_password + '\n')
            stdin.flush()
            sleep(1)
            look_for_file_in, look_for_file_out, look_for_file_err = ssh.exec_command("ls /etc/ppp/peers/")
            message = "ooops"
            if vpn_filename + "\n" in look_for_file_out.readlines():
                message = "ok"
            ssh.close()
            print(message)

        elif self.function == "connect":
            pptp_name = input('import vpn filename: ')

            target_host = input('import target host name/ip: ')
            target_username = input('import target host ssh username: ')
            target_password = input('import target host ssh password: ')

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target_host, 22, username=target_username, password=target_password)
            stdin, stdout, stderr = ssh.exec_command("sudo -S pon {}".format(pptp_name))
            stdin.write(target_password + '\n')
            stdin.flush()
            sleep(2)
            stdin, stdout, stderr = ssh.exec_command("ifconfig")
            output = stdout.readlines()
            for line in output:
                if "ppp" in line:
                    print("ok")
                    return

            ssh.close()
            print("Hey, let's check it!")
            return
        elif self.function == "disconnect":
            pptp_name = input('import vpn filename: ')

            target_host = input('import target host name/ip: ')
            target_username = input('import target host ssh username: ')
            target_password = input('import target host ssh password: ')

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target_host, 22, username=target_username, password=target_password)
            stdin, stdout, stderr = ssh.exec_command("sudo -S poff {}".format(pptp_name))
            stdin.write(target_password + '\n')
            stdin.flush()
            sleep(2)
            stdin, stdout, stderr = ssh.exec_command("ifconfig")
            output = stdout.readlines()
            for line in output:
                if "ppp" in line:
                    print("Error, let's check it!")
                    return

            ssh.close()
            print("ok")
            return


VPNConnection()
