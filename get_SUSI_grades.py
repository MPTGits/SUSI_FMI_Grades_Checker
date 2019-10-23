#A simple programm that gets your susi grades from FMI

#dict username filed name:txtUserName
#                    password:txtPassword
from requests import Session
from bs4 import BeautifulSoup as bs
import getpass
import re
import sys

#Seperate function so I can test it
def login_details():
    username=input("Please enter username:")
    password=getpass.getpass("Please enter password:")
    return (username,password)

def print_student_info(subjects,lectors,grades):
    if len(subjects)!=len(lectors) or len(lectors)!=len(grades):
        raise Exception("Unmatching values for list")
        sys.exit(1)
    for i in range(0,len(subjects)):
        print('Предмет:',subjects[i])
        print('Лектор:',lectors[i])
        print('Оценка:',grades[i],'\n')
    print('Средно аритметично то всички взети изпити:',round(sum(grades)/len(grades),3))
    return True
def main_info_geter(username='',password=''):
    
#This are the needed fileds to be filed when login in plus the needed tokens so we verify the login
    login_info={
        "txtUserName":"NULL",
        "txtPassword":"NULL",
        "__EVENTVALIDATION":"NULL",
        "__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":"",
        "__VSTATE":"NULL",
        "btnSubmit":"Влез"
    }
#We need to keep a session open with the site for as long as we use it
    with Session() as s:
        
        site=s.get("https://susi.uni-sofia.bg/ISSU/forms/Login.aspx")
        bs_content = bs(site.content, "html.parser")
        #We get the needed user login details adn find all the needed tokens from the site we need with the BeautifulSoup find function
        login_info["txtUserName"]=username
        login_info["txtPassword"]=password
        login_info["__EVENTVALIDATION"]=bs_content.find("input", {"name":"__EVENTVALIDATION"})["value"]
        login_info["__VSTATE"]=bs_content.find("input", {"name":"__VSTATE"})["value"]

        #Throwing an exception if our login was not accurate
        result=s.post("https://susi.uni-sofia.bg/ISSU/forms/Login.aspx",login_info)
        if "PageError1_lblError" in result.text:
            raise Exception("Sorry,Invalid login!")
            sys.exit(1)
        #Geting the page content
        grades_page=s.get("https://susi.uni-sofia.bg/ISSU/forms/students/ReportExams.aspx")
        bs_content2 = bs(grades_page.content, "html.parser")

        grades={
        "Report_Exams1:chkTaken":"on",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":"",
        "__VSTATE":"NULL",
        "__EVENTVALIDATION":"NULL",
        "__EVENTTARGET":"Report_Exams1$btnReportExams"
    }
        #Geting all the info we need for out post request to tic the checkbox with the grades of the course we passed
        grades["__EVENTVALIDATION"]=bs_content2.find("input", {"name":"__EVENTVALIDATION"})["value"]
        grades["__VSTATE"]=bs_content2.find("input", {"name":"__VSTATE"})["value"]
         
        my_grades=s.post("https://susi.uni-sofia.bg/ISSU/forms/students/ReportExams.aspx",grades) 

        #Taking the fileds that we will need with beautifulsoup(subject names,lector names,grades)
        soup = bs(my_grades.content,"html.parser")
        subjects=soup.find_all('td',{"width":"40%"})
        lectors=soup.find_all('td',{"width":"24%"})
        grades=soup.find_all('td',{"width":"7%"})
        #Formating the grades and geting rid of trash data(taking only the float values)
        formated_grades=[]
        for grade in grades:
            try:
                float(grade.text)
            except Exception:
                pass
            else:
                formated_grades.append(float(grade.text))

        #Formating the subjects and taking only the name of the subjects
        formated_subjects=[]
        for subject in subjects:
            if subject.text.strip()!='' and subject.text.strip()!='Предмет':
                formated_subjects.append(subject.text.strip())
        #Formating the lectors and taking only the names
        formated_lectors=[]
        for lector in lectors:
            if lector.text.strip()!='' and lector.text.strip()!='Преподавател':
                formated_lectors.append(lector.text.strip())
    #Returning the lists as tuples
    return (formated_subjects,formated_lectors,formated_grades)

def main():
    login_data=login_details()
    resulted_lists=main_info_geter(login_data[0],login_data[1])
    print_student_info(resulted_lists[0],resulted_lists[1],resulted_lists[2])

if __name__=='__main__':
    main()


