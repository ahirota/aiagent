from functions.get_files_info import get_files_info


def test_case_1():
    response = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(response)

def test_case_2():
    response = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(response)

def test_case_3():
    response = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(response)

def test_case_4():
    response = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(response)

def main():
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()

if __name__ == "__main__":
    main()