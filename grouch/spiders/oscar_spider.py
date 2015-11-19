import scrapy
from grouch.loaders import CourseLoader
import grouch


class OscarSpider(scrapy.Spider):
    name = "oscar"
    allowed_domains = ['oscar.gatech.edu']
    start_urls = ['https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_dyn_ctlg']
    base = 'https://oscar.gatech.edu'
    

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

    field_formats = {
        "Grade Basis": get_grade_basis,
        "Restrictions": get_restrictions,
        "Prerequisites": get_prerequisites,
        "Course Attributes": get_attributes,
        "Corequisites": get_corequisites
    }

    def parse(self, response):
        return self.parse_catalog(response)

    def parse_catalog(self, response):
        # url = response.css(".pagebodydiv form::attr(action)").re(".*")[0]  # url
        term_name = response.css("#term_input_id::attr(name)").re(".*")[0]
        terms = response.css("#term_input_id option::attr(value)").re("\d{6}")
        for term in terms[:grouch.settings.SEMESTER_STOP]:
            yield scrapy.FormRequest.from_response(response,
                                                   callback=self.parse_term,
                                                   formdata={term_name: term})

    def parse_term(self, response):
        subjects = response.css("#subj_id option::attr(value)").re(".*")
        if grouch.settings.SUBJECTS:
            subjects = grouch.settings.SUBJECTS
        for subject in subjects :  #subjects:
            yield scrapy.FormRequest.from_response(response,
                                                   callback=self.parse_courses,
                                                   formdata={"sel_subj": ["dummy", subject]})

    def parse_courses(self, response):
        # titles = response.css(".nttitle a::text").re(".*")
        urls = response.css("td.nttitle a::attr(href)").re(".*detail.*")
        # only pulls urls for course pages
        for url in urls:
            yield scrapy.Request(self.base+url, self.parse_detail)

    def parse_detail(self, response):
        loader = CourseLoader(item=grouch.items.Course(), response=response)
        loader.add_css('fields', 'span.fieldlabeltext::text', re='^(.*?):')
        loader.add_css('fullname', 'td.nttitle::text', re='.*')
        loader.add_css('name', 'td.nttitle::text', re='- (.*)')
        loader.add_css('school', 'td.nttitle::text', re='(.*?) ')
        loader.add_css('number', 'td.nttitle::text', re='\d+')

        for field in loader.item.fields:
            pass            

        return loader.load_item()
