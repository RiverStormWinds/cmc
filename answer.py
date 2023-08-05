import random


class ClassRoom:
    def __init__(self):
        self.student_ids = []

    def add_student_id(self, student_id):
        if student_id not in self.student_ids:
            self.student_ids.append(student_id)

    def check_student_id(self, student_id):
        return student_id in self.student_ids

    def remove_student_id(self, student_id):
        if student_id in self.student_ids:
            self.student_ids.remove(student_id)

    def get_random_student_id(self):
        if self.student_ids:
            return random.choice(self.student_ids)
        else:
            return None

    def get_min_student_id(self):
        if self.student_ids:
            return min(self.student_ids)
        else:
            return None


if __name__ == '__main__':
    # 实例化一个ClassRoom对象
    classroom = ClassRoom()

    # 添加学号
    classroom.add_student_id('2023001')
    classroom.add_student_id('2023002')
    classroom.add_student_id('2023003')

    # 查找学号
    print(classroom.check_student_id('2023001'))  # True
    print(classroom.check_student_id('2023004'))  # False

    # 删除学号
    classroom.remove_student_id('2023002')

    # 随机返回学号
    print(classroom.get_random_student_id())

    # 返回最小的学号
    print(classroom.get_min_student_id())

