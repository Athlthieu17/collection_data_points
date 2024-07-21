import requests as r
def searchLastProvince(province, max_student_in_province=110000):
    low = 0
    high = max_student_in_province
    
    while low <= high:
        mid = (low + high) // 2  
        sbd = create_sbd(province, mid)
        if isValidProvince(sbd):
            low = mid + 1
        else:
            high = mid - 1
    # No valid sbd found within the range
    if low > max_student_in_province:
        return -1

    # Return the previous sbd (potential valid sbd)
    return (low - 1)


def isValidProvince(sbd):
    url = "https://vtvapi3.vtv.vn/handlers/timdiemthi.ashx?keywords=" + str(sbd)
    content = r.get(url = url)
    response = content.content
    if len(response) > 0:
        return True
    return False

def create_sbd(province, student_number):
  """
  Creates a formatted student number (sbd) string.

  Args:
      province: The province number (1-9).
      student_number: The student number within the province.

  Returns:
      The formatted sbd string (e.g., "01001234").
  """

  province_str = f'0{province}' if province < 10 else str(province)
  sbd_str = f'{province_str}{student_number:06d}'  
  return sbd_str

def save_max_students(max_students_per_province):
  """
  Saves the maximum student numbers for each province to a JSON file.

  Args:
      max_students_per_province: A dictionary mapping province numbers to last valid student numbers.
  """

  with open('max_student_province.py', 'w') as f:
    f.write(str(max_students_per_province))


if __name__ == "__main__":
    max_students = {}
    for i in range (1,65):
        last_sbd = searchLastProvince(i)
        max_students[i] = last_sbd
    
    save_max_students(max_students)