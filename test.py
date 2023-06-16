def convert_list(strrr : str):
    def convert_grades_to_12_scale(grades_5_scale):
            grades_12_scale = []
            for grade in grades_5_scale:
                if grade == 5:
                    grades_12_scale.append(12)
                elif grade == 4:
                    grades_12_scale.append(9)
                elif grade == 3:
                    grades_12_scale.append(6)
                elif grade == 2:
                    grades_12_scale.append(3)
                else:
                    grades_12_scale.append(0)
            return grades_12_scale

    
    data_parts = strrr.split()
    name = ' '.join(data_parts[:3])
    grades_12_scale = list(map(int, data_parts[3].split(',')))
    grades_5_scale = list(map(int, data_parts[4].split(',')))

    grades_12_scale_converted = convert_grades_to_12_scale(grades_5_scale)


    return {name : grades_12_scale + grades_12_scale_converted}
    
with open("input.txt", "r", encoding="utf8") as file:
    lines = file.readlines()
    
data = []
    
for i in lines:
    data.append(convert_list(i))
    
def calculate_average_marks(marks):
    return sum(marks) / len(marks)

averages = []
for student in data:
    name = list(student.keys())[0]
    marks = list(student.values())[0]
    average = calculate_average_marks(marks)
    averages.append({name: average})

sorted_averages = sorted(averages, key=lambda x: list(x.values())[0], reverse=True)

marks_count = {}
for student in data:
    name = list(student.keys())[0]
    marks = list(student.values())[0]
    marks_count[name] = len(marks)

good_students = []
for student in data:
    name = list(student.keys())[0]
    marks = list(student.values())[0]
    if min(marks) >= 7:
        good_students.append(name)

bad_students = []
for student in data:
    name = list(student.keys())[0]
    marks = list(student.values())[0]
    if any(mark < 4 for mark in marks):
        bad_students.append(name)

with open('sorted_averages.txt', 'w', encoding="utf8") as file:
    for item in sorted_averages:
        name = list(item.keys())[0]
        average = list(item.values())[0]
        file.write(f'{name}: {average}\n')

with open('marks_count.txt', 'w', encoding="utf8") as file:
    for name, count in marks_count.items():
        file.write(f'{name}: {count}\n')

with open('good_students.txt', 'w', encoding="utf8") as file:
    for student in good_students:
        file.write(f'{student}\n')

with open('bad_students.txt', 'w', encoding="utf8") as file:
    for student in bad_students:
        file.write(f'{student}\n')