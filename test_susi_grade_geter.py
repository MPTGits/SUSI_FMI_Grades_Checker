from get_SUSI_grades import *
import unittest 

class TestSusiGradeGetter(unittest.TestCase):

    def test_when_unvalid_login_details_are_given(self):
        login_data=('UnknownName','stupidPassword')
        self.assertRaises(Exception,main_info_geter,login_data[0],login_data[1])
    
    def test_when_not_equal_list_of_subjects_lectors_grades_is_give_to_the_print_function1(self):
        lst1=[1,2,3,4]
        lst2=[4,4]
        lst3=[3,1,3]
        self.assertRaises(Exception,print_student_info)
    
    def test_when_not_equal_list_of_subjects_lectors_grades_is_give_to_the_print_function2(self):
        lst1=[1,2,3,4]
        lst2=[4,4,5]
        lst3=[3,1,3]
        self.assertRaises(Exception,print_student_info)
    def test_when_not_equal_list_of_subjects_lectors_grades_is_give_to_the_print_function3(self):
        lst1=[1,2,3,4]
        lst2=[4,4,2,1]
        lst3=[3,1,]
        self.assertRaises(Exception,print_student_info)

    def test_when_not_equal_list_of_subjects_lectors_grades_is_give_to_the_print_function4(self):
        lst1=[1,2,3]
        lst2=[4,4,2,1]
        lst3=[3,1,3,1]
        self.assertRaises(Exception,print_student_info)
    def test_when_equal_list_of_subjects_lectors_grades_is_give_to_the_print_function(self):
        lst1=[1,2,3,4]
        lst2=[4,4,2,1]
        lst3=[3,1,2,1]
        self.assertEquals(True,print_student_info(lst1,lst2,lst3))



if __name__=="__main__":
    unittest.main()