
def remove_leading_zero(ip):
    nums = [str(int(n)) for n in ip.split('.')]
    return ".".join(nums)

print remove_leading_zero("10.020.30.040")