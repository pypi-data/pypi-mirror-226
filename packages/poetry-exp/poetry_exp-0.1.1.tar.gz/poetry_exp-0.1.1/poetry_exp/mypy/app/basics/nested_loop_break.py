def test1():
    for x in range(10):
        for y in range(10):
            print(x * y)
            if x * y > 50:
                break
        else:
            continue  # only executed if the inner loop did NOT break
        break  # only executed if the inner loop DID break



if __name__ == '__main__':
    exit_num = 50  # 5
    for i in range(10):
        for j in range(20):
            if j == exit_num:
                print('Breaking from inner')
                break
        else:
            print(f'i: {i}, j:{j}, inner loop did not break')
            continue
        print(f'i: {i}, j:{j}, inner loop breaked')

        break