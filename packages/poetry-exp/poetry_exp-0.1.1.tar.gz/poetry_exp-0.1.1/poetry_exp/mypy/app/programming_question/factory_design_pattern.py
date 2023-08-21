
class Backup(object):
    def backup(self):
        pass

    def restore(self):
        pass


class HyperV1BackupDriver(Backup):
    def backup(self):
        print 'Taking backup using Hyperv1..'

    def restore(self):
        print "Resstoring using Hyperv1"


class HyperV2BackupDriver(Backup):
    def backup(self):
        print 'Taking backup using Hyperv2..'

    def restore(self):
        print "Resstoring using Hyperv2"


# It is supposed to be enum
class HyperVType(object):
    HyperV1 = 1
    HyperV2 = 2


class BackupFactory(object):
    def __init__(self, hyperv_ip, username, password):
        self.hyperv_ip = hyperv_ip
        self.username = username
        self.password = password

    def get_hyperv_type(self):
        # Discover the type of hyperv using ip, username and password
        return {
            "10.10.1.2": HyperVType.HyperV1,
            "10.20.1.2":  HyperVType.HyperV2
        }.get(self.hyperv_ip)

    def create_backup_driver(self):
        # Similar to switch case
        return {
            HyperVType.HyperV1: HyperV1BackupDriver(),
            HyperVType.HyperV2: HyperV2BackupDriver()
        }.get(self.get_hyperv_type(), None)


if __name__ == '__main__':
    bpf = BackupFactory("10.10.1.2", "admin", "password")
    # bpf = BackupFactory("10.20.1.2", "admin", "password")
    bpd = bpf.create_backup_driver()
    bpd.backup()
    bpd.restore()

