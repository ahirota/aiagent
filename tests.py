from functions.get_files_info import get_files_info, get_file_content


# def test_get_files_info_1():
#     response = get_files_info("calculator", ".")
#     print("Result for current directory:")
#     print(response)

# def test_get_files_info_2():
#     response = get_files_info("calculator", "pkg")
#     print("Result for 'pkg' directory:")
#     print(response)

# def test_get_files_info_3():
#     response = get_files_info("calculator", "/bin")
#     print("Result for '/bin' directory:")
#     print(response)

# def test_get_files_info_4():
#     response = get_files_info("calculator", "../")
#     print("Result for '../' directory:")
#     print(response)

# def test_get_files_content_truncation():
#     response = get_file_content("calculator", "lorem.txt")
#     print(response)

def test_get_files_content_1():
    response = get_file_content("calculator", "main.py")
    print(response)

def test_get_files_content_2():
    response = get_file_content("calculator", "pkg/calculator.py")
    print(response)

def test_get_files_content_3():
    response = get_file_content("calculator", "/bin/cat")
    print(response)

def test_get_files_content_4():
    response = get_file_content("calculator", "pkg/does_not_exist.py")
    print(response)

def main():
    # test_get_files_info_1()
    # test_get_files_info_2()
    # test_get_files_info_3()
    # test_get_files_info_4()

    # test_get_files_content_truncation()

    test_get_files_content_1()
    test_get_files_content_2()
    test_get_files_content_3()
    test_get_files_content_4()

if __name__ == "__main__":
    main()