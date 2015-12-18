import scrapy
from grouch.loaders import CourseLoader
import grouch
from grouch import items


class OscarSpider(scrapy.Spider):
    name = "oscar"
    allowed_domains = ['oscar.gatech.edu']
    start_urls = ['https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_dyn_ctlg']
    base = 'https://oscar.gatech.edu'

    field_formats = {
        "Grade Basis": "grade_basis",
        "Restrictions": "restrictions",
        "Prerequisites": "prerequisites",
        "Course Attributes": 'course_attributes',
        "Corequisites": 'corequisites' 
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
        loader = CourseLoader(item=items.Course(), response=response)
        loader.add_css('fields', 'span.fieldlabeltext::text', re='^(.*?):')
        loader.add_css('fullname', 'td.nttitle::text', re='.*')
        loader.add_css('name', 'td.nttitle::text', re='- (.*)')
        loader.add_css('school', 'td.nttitle::text', re='(.*?) ')
        loader.add_css('number', 'td.nttitle::text', re='\d+')
        loader.add_css('hours', 'td.ntdefault', re='([\s\S]*?)<span')
        loader.add_css('identifier', 'td.nttitle::text', re='(.*?) -')
        
        for field in loader._values['fields']:  # introspect the loader
            # wonky way to deal with adding the regex
            regex = "{}.{}<\/span>([\S\s]*?)(?:<span|<\/td>)".format(field, "{0,5}")
            loader.add_css(self.field_formats[field], 'td.ntdefault', re=regex)

        urls = response.css('td.nttitle a::attr(href)').re('.*listcrse.*?')
        for url in urls:
            loader.add_value('sections', scrapy.Request(self.base+url, self.parse_section))

        return loader.load_item()

    def parse_section(self, response):
        return None
