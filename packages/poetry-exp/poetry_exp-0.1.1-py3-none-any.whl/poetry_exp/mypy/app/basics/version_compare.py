
def version_tuple(version):
    ver_arr = []
    for point in version.split("."):
        ver_arr.append(point.zfill(8))

    #print ver_arr
    #print(tuple(ver_arr))
    return tuple(ver_arr)


if __name__=='__main__':
    print(version_tuple("4.3.1-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.1-2318.51") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.1-2319.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.2-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.4.1-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("5.3.1-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.1-3318.50") >= version_tuple("4.3.1-2318.50"))
    print("False casses.........")
    print(version_tuple("4.3.1-2318.49") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.1-2317.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.3.0-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("4.2.1-2318.50") >= version_tuple("4.3.1-2318.50"))
    print(version_tuple("3.3.1-2318.50") >= version_tuple("4.3.1-2318.50"))

    # print (version_tuple("7.4.2") == version_tuple("7.4.2")) # True
    # print (version_tuple("7.4.2") < version_tuple("7.4.3")) # True
    # print (version_tuple("7.4.2") < version_tuple("7.5.1"))  # True
    # print (version_tuple("7.4.2") < version_tuple("8.4.3"))  # True
    # print (version_tuple("7.4.2") < version_tuple("6.4.3"))  # False
    # print (version_tuple("7.4.2") < version_tuple("7.3.3"))  # False
    # print (version_tuple("9.4.5") > version_tuple("2.4.5"))  # True
    # print (version_tuple("10a.4.5.23-alpha") > version_tuple("2a.4.5.23-alpha"))  # True
    # print (version_tuple("10a.4.5.23-alpha") > version_tuple("10a.4.5.24-alpha"))  # False