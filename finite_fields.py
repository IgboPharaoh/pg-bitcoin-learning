class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return "FieldElement_{}({})".format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot add numbers in different fields")

        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract numbers in different fields")

        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot multiply numbers in different fields")

        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)

        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different fields")
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)


# This algorithm is for calculating finite field addition and subtraction for bitcoin
# We calculate the values this way to ensure the result is closed, that is, it's in the field
class FiniteFieldCalculator:
    # params: prime, nums
    def __init__(self, nums: list, prime: int):
        for num in nums:
            if num >= prime or num < 0:
                error = "Num {} not in field range 0 to {}".format(num, prime - 1)
                raise ValueError(error)
        self.nums = nums
        self.prime = prime

    def __addition__(self, nums):
        return (sum(nums)) % self.prime

    def __subtraction__(self, nums):
        if len(nums) == 1:
            return (nums[0]) % self.prime
        else:
            total = nums[0]
            for num in nums[1:]:
                total -= num

        return (total) % self.prime

    def __multiplication__(self, nums):
        if len(nums) == 2:
            return (nums[0] * nums[1]) % self.prime
        else:
            total = nums[0]
            for num in nums[1:]:
                total = total * num
            return (total) % self.prime

    def __exponentiation__(
        self,
        base,
        exponent,
    ):
        exp = exponent % (self.prime - 1)
        return pow(base, exp, self.prime)

    def __division__(self, nums):
        # assuming only two numbers eg:2/7
        return (
            nums[0]
            * pow(
                nums[1],
                self.prime - 2,
            )
            % self.prime
        )

    def generate_field_elements(self, nums):
        for num in nums:
            print(sorted([num * i % self.prime for i in range(self.prime)]))

    def gen_field_pow_elems(prime, nums):
        for prime in nums:
            print(sorted([pow(i, prime - 1, prime) for i in range(1, prime)]))


calculator = FiniteFieldCalculator([0], 31)
print(
    "answer: {}".format(
        calculator.__division__(
            [
                3,
                24,
            ]
        )
    )
)

print("exp answer: {}".format(calculator.__exponentiation__(17, -3)))

print(
    "answer: {}".format(
        calculator.__multiplication__([calculator.__exponentiation__(4, -4), 11])
    )
)
