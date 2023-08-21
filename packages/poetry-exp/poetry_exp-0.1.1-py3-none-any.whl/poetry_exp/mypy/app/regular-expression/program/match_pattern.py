import re

# There can only be 4 controller ranges from 0 to 3
# 1 SCSI controller can have maximum 16 disks ranges from 0 to 15
# 1 SATA controller can have maximum 30 disks ranges from 0 to 29

SCSI_DISK_PATTERN = r'^scsi[0-3]:([0-9]|1[0-5]).ctkEnabled$'
SATA_DISK_PATTERN = r'^sata[0-3]:([0-9]|1[0-9]|2[0-9]).ctkEnabled$'
IDE_DISK_PATTERN = r'^ide[0-1]:[0-1].ctkEnabled$'

CBT_ENABLED_DISKS_PATTERN =\
    r'(^scsi[0-3]:([0-9]|1[0-5]).ctkEnabled$)|(^sata[0-3]:' \
    r'([0-9]|1[0-9]|2[0-9]).ctkEnabled$)|(^ide[0-1]:[0-1].ctkEnabled$)'
strings = [
    'scsi0:0.ctkEnabled',
    'scsi1:0.ctkEnabled',
    'scsi3:0.ctkEnabled',
    'scsi0:15.ctkEnabled',
    'scsi0:1.ctkEnabled',
    'scsi0:10.ctkEnabled',
    'scsi4:0.ctkEnabled',
    'scsi0:16.ctkEnabled',
    'scsi0:155.ctkEnabled',
    'scsi0:00.ctkEnabled',
    'scsi0::0.ctkEnabled',
    'scsi0::0ctkEnabled',
    '1scsi0:0.ctkEnabled',
    'scsi0:0.ctkEnabled1',

    'sata0:0.ctkEnabled',
    'sata1:0.ctkEnabled',
    'sata3:0.ctkEnabled',
    'sata0:10.ctkEnabled',
    'sata0:11.ctkEnabled',
    'sata0:20.ctkEnabled',
    'sata0:21.ctkEnabled',
    'sata0:29.ctkEnabled',
    'sata0:1.ctkEnabled',
    'sata0:10.ctkEnabled',
    'sata4:0.ctkEnabled',
    'sata0:16.ctkEnabled',
    'sata0:155.ctkEnabled',
    'sata0:00.ctkEnabled',
    'sata0::0.ctkEnabled',
    'sata0::0ctkEnabled',
    '1sata0:0.ctkEnabled',
    'sata0:0.ctkEnabled1',

    'ide0:0.ctkEnabled',
    'ide0:1.ctkEnabled',
    'ide1:0ctkEnabled',
    'ide1:1.ctkEnabled',
    'ide0:2.ctkEnabled',
    'ide2:0.ct,kEnabled',
    'ide0:2.ctkEnabled1'

]

for s in strings:

    matched = re.match(CBT_ENABLED_DISKS_PATTERN, s)
    if matched:
        print(f'String: {s} matched')
    else:
        print(f'String: {s} not matched')
