def find_gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def find_euler_totient_func(n):
    result = 1
    for i in range(2, n):
        if find_gcd(i, n) == 1:
            result += 1
    return result


def main():
    n = int(input("Enter a number: "))
    print(f"Euler's totient function of {n} is {find_euler_totient_func(n)}")


if __name__ == "__main__":
    main()
