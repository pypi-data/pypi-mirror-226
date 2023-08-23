def sum_list(numbers):
  total = 0
  for num in numbers:
    total += num
  return total

def sub_list(numbers):
  total = numbers[0]
  for num in numbers[1:]:
    total -= num
  return total

def multi_list(numbers):
  total = numbers[0]
  for num in numbers[1:]:
    total *= num
  return total

def div_list(numbers):
  total = numbers[0]
  for num in numbers[1:]:
    total /= num
  return total