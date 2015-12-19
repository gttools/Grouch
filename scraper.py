import scrapy
from scrapy import FormRequest
import re

remove_tags = re.compile(r'<.*?>')
remove_semester = re.compile(r' ?Undergraduate Semester level | ?Graduate Semester level ')
remove_minimum = re.compile(r' Minimum Grade of [ABCD]')


class OscarSpider(scrapy.Spider):
    name= "OscarSpider"
    start_urls = ['https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_dyn_ctlg']

    @staticmethod
    def dummy(response):
        return ""

    @staticmethod
    def get_grade_basis(response):
        string = response.css('td.ntdefault').re("Grade Basis[\S\s]*?<br>([\S\s]*?)<span")[0]
        pass

    @staticmethod
    def get_attributes(response):
        string = response.css('td.ntdefault').re("Attributes[\S\s]*?<br>([\S\s]*?)<span")[0]
        pass

    @staticmethod
    def get_restrictions(response):
        string = response.css('td.ntdefault').re("Restrictions[\S\s]*?<br>([\S\s]*?)<span")[0]
        pass

    @staticmethod
    def get_corequisites(response):
        string = response.css('td.ntdefault').re("Corequisites[\S\s]*?<br>([\S\s]*?)<br>")[0]
        string = remove_tags.sub("", string)
        string = remove_semester.sub("", string)
        string = remove_minimum.sub("", string)
        return string.lstrip()

    @staticmethod
    def get_prerequisites(response):

        string = response.css('td.ntdefault').re("Prerequisites[\S\s]*?<br>([\S\s]*?)<br>")[0]
        string = remove_tags.sub("", string)
        string = remove_semester.sub("", string)
        string = remove_minimum.sub("", string)
        return string.lstrip()


    def parse(self, response):
        self.base = "https://oscar.gatech.edu"  # base OSCAR url
        self.field_formats = {
            "Grade Basis" : self.dummy,
            "Restrictions" : self.dummy,
            "Prerequisites" : self.get_prerequisites,
            "Course Attributes" : self.dummy,
            "Corequisites" : self.get_corequisites
        }

        self.f = open("out.txt", "w")
        self.words = set()
        return self.parse_catalog(response)

    def parse_catalog(self, response):
        # url = response.css(".pagebodydiv form::attr(action)").re(".*")[0]  # url
        term_name = response.css("#term_input_id::attr(name)").re(".*")[0]
        terms = response.css("#term_input_id option::attr(value)").re("\d{6}")
        for term in terms[0:1]:
            yield scrapy.FormRequest.from_response(response,
                                     callback=self.parse_term,
                                     formdata={term_name: term})

    def parse_term(self, response):
        subjects = response.css("#subj_id option::attr(value)").re(".*")
        for subject in ["CS"]:
            yield scrapy.FormRequest.from_response(response,
                                     callback=self.parse_courses,
                                     formdata={"sel_subj":["dummy", subject]})

    def parse_courses(self, response):
        # titles = response.css(".nttitle a::text").re(".*")
        urls = response.css("td.nttitle a::attr(href)").re(".*")
        for url in urls:
            yield scrapy.Request(self.base+url, self.parse_detail)

    def parse_detail(self, response):
        fields = response.css('span.fieldlabeltext::text').re("^(.*?):")
        fullname = response.css('td.nttitle::text').re(".*")[0]
        school = response.css('td.nttitle::text').re("^(.*?)-")
        course = response.css('td.nttitle::text').re("\d*")[0]
        name = response.css('td.nttitle::text').re("[^-]*$")[0]

        self.f.write(fullname+"\n")
        for field in fields:
            self.f.write("    "+field+"\n")
            self.f.write("        "+self.field_formats[field](response)+"\n")
