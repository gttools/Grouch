import scrapy
from grouch.loaders import CourseLoader, SectionLoader
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
        terms = [term for term in terms if
                term.endswith(grouch.settings.SEMESTER_ACCEPT)]
        for term in terms[:grouch.settings.SEMESTER_STOP]:
            self.semester, _, self.year = term.partition(" ")
            yield scrapy.FormRequest.from_response(response,
                                                   callback=self.parse_term,
                                                   formdata={term_name: term})

    def parse_term(self, response):
        subjects = response.css("#subj_id option::attr(value)").re(".*")
        if grouch.settings.SUBJECTS:
            subjects = grouch.settings.SUBJECTS
        for subject in subjects:  # subjects:
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
        loader.add_value("semester", self.semester)
        loader.add_value("year", self.year)
        loader.add_css('fields', 'span.fieldlabeltext::text', re=r'^(.*?):')
        loader.add_css('fullname', 'td.nttitle::text', re=r'.*')
        loader.add_css('name', 'td.nttitle::text', re=r'- (.*)')
        loader.add_css('school', 'td.nttitle::text', re=r'(.*?) ')
        loader.add_css('number', 'td.nttitle::text', re=r'([\dX]+\w?)')
        loader.add_css('hours', 'td.ntdefault', re=r'([\s\S]*?)<span')
        loader.add_css('identifier', 'td.nttitle::text', re=r'(.*?) -')

        for field in loader._values['fields']:  # introspect the loader
            # wonky way to deal with adding the regex
            regex = r"{}.{}<\/span>([\S\s]*?)(?:<span|<\/td>)".format(field, "{0,5}")
            loader.add_css(self.field_formats[field], 'td.ntdefault', re=regex)

        url = response.css('td.ntdefault a::attr(href)').re('.*listcrse.*')

        if url:
            return scrapy.Request(self.base+url[0], self.parse_section, meta={'course': loader})
        else:
            return loader.load_item()

    def parse_section(self, response):
        course_loader = response.meta['course']
        section_table = response.css('div.pagebodydiv>table.datadisplaytable>tr')[:-1]
        
        sections = []
        for header, body in zip(*[iter(section_table)]*2):
            # https://docs.python.org/2/library/functions.html#zip
            # This makes possible an idiom for clustering a data series into n-length
            # groups using zip(*[iter(s)]*n).
            sections.append(self._parse_section_helper(header, body))

        course_loader.add_value('sections', sections)
        return course_loader.load_item()

    def _parse_section_helper(self, header, body):
        loader = SectionLoader(item=items.Section())
        loader.add_value('section_id', header.re(r'(?:-.*)+ - (.*?)<'))
        loader.add_value('crn', header.re(r' - (\d{5}) - '))
        loader.add_value('term', body.css('td::text').re(r'Associated Term'))
        loader.add_value('campus', body.css('td::text').re(r'Undergraduate Semester \n(.*)\n'))
        meetings = []
        instructors = set()
        for row in body.css('tr')[2:]:
            blocks = row.css('td.dddefault')
            meet = dict()
            meet['time'] = blocks[1].css('td::text').extract()
            meet['days'] = blocks[2].css('td::text').extract()
            meet['location'] = blocks[3].css('td::text').extract()
            meet['type'] = blocks[5].css('td::text').extract()

            for attr in ['time', 'days', 'location', 'type']:
                meet[attr] = meet[attr][0] if meet[attr] else None
                meet[attr] = None if meet[attr] == u'\xa0' else meet[attr]

            meet['instructor'] = "".join(blocks[6].css('td::text').extract()).replace('()', '').split(',')
            meet['instructor'] = [i.strip() for i in meet['instructor']]
            for i in meet['instructor']:
                instructors.add(i)
            meetings.append(meet)

        loader.add_value('meetings', meetings)
        loader.add_value('instructors', list(instructors))

        return loader.load_item()
