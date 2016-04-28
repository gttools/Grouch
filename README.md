Grouch
======

Grouch is a tool to gather data from the Georgia Tech's OSCAR Course registration tool and parse it into an easy machine readable format. It makes an attempt to be lightweight and extensible. It is not in any way approved by Georgia Tech.

## Table of Contents
 - [Installation](#installation)
 - [Quickstart](#quickstart)
 - [Settings](#settings)
 - [Data Format](#data-format)
 - [Extending Grouch](#extending-grouch)
 - [Contributing](#contributing)

## Installation
Installing grouch is quick and easy, simply
 - `git clone` this repository
 - `pip install scrapy` on python 2
 - If you want to test or develop, additionally
     - `pip install nose`
     - `pip install mock`
     - optionally, `pip install coverage`

 That's it, the only direct dependency is scrapy, everything else will come along with that. Note that scrapy currently only supports python 2.7, however theoretically, Grouch should support python3 as soon as scrapy finishes porting.
 
## Quickstart
With Grouch and dependencies installed, the quickest way to get going is by running `scrapy crawl -o result.json -t json oscar`. That will run a scrape over the Computer Science courses in the most recent semester, and dump the results into the file `result.json`. 

## Settings
Settings can be found in `grouch/settings.py`. There are two settings of note: `SEMESTER_STOP` and `SUBJECTS`. Semester stop takes an integer value, if it is positive, then Grouch will only scrape that many semesters into the past, so a value of 3 would scrape (as of this writing) Spring 2015 as well as the two language institute semesters availible on OSCAR. A value of -1 scrapes all of them, a value of 0 does nothing. Subjects is a way to filter by subject, a value of `['CS', 'AE', 'LMC']` would only return courses from LMC, AE and CS schools. An empty list gets data from all schools.

##Data Format
While Grouch allows you to reformat the data however you want, it is written in python and the default output is in json, so I'll describe the output in that regard.

When run, Grouch will output a json object in the following format.

The top level is a list of Course objects. A course object is structured as follows:

```
{
"restrictions": {
    "restrictions": ["Campuses"], 
    "Campuses": {
        "positive": true, 
        "requirements": ["Georgia Tech-Atlanta *"]
        }
    }, 
    "school": "CS", 
    "name": "User Interface Software", 
    "prerequisites": {
        "courses": ["CS 2340", {
            "courses": ["CS 3750", "PSYC 3750"], 
            "type": "or"
            }], 
        "type": "and"
        }, 
    "fields": ["Grade Basis", "Course Attributes", "Restrictions", "Prerequisites"], 
    "number": "4470", 
    "hours": "3.000 Credit hours", 
    "grade_basis": "ALP", 
    "course_attributes": "Tech Elect CS, Engr, &amp;Sciences", 
    "fullname": "CS 4470 - User Interface Software", 
    "identifier": "CS 4470"},
```
These are the attributes a course object can have:

 - Required
     - school: The abbreviation for the school in which the course is taught
     - name: The string name of the course, like "User interface design"
     - number: The 4 digit course number, can also contain Xs (as in PHYS 2XXX)
     - hours: a list containing strings of the hours the course can be worth (lecture, lab, credit)
     - fullname: The school, number, and name together
     - identifier: school followed by number
     - fields: A list containing course attributes, grade basis, restrictiions, prerequisites, or corequisites, depending on which optional attributes the course has (note that sections is not in this list)
 - optional
     - course_attributes: a list of attributes from OSCAR
     - grade_basis: a string, generally 'ALP', or a subset of those, letters, but others are possible
     - restrictions: a nested structure of restrictions
     - prerequisites: an arbitrarilly nested json object
     - corequisites: an object in the same form as prerequisites
     - sections: a complex json object
 
 - restrictions
     - The restriction object contains a list, 'restrictions', that contains other accessible attributes
     - Each other attribute contains a boolean 'positive' and a list 'requirements'
     - positive true if the requirements are positive, false if the are negated
         - so if positive is true and the requirement is campus is Georgia Tech atlanta, one must take this course in Atlanta, if positive is false, it must instead be taken abroad
 - prerequisites
     - this and corequisites are the same in theory, but prerequisites can be much more complex in reality
     - recursively nested, but easily parsable
     - Each level contains two things, a list of prereqs, and a type
     - if the type is 'and', the prereqs must all be satisfied, if the type is 'or', only one must be satisified
     - each prereq can either be a course identifier or another prerequisite object
     - in the above example, one must always take CS 2340, but can take either CS 3750 or PSYC 3750
 - sections
```
"sections": [
    {
        "meetings": [
            {
                "instructor": ["Jacob R  Eisenstein"], 
                "location": "Clough Undergraduate Commons 102", 
                "type": "Lecture*", 
                "days": "TR", 
                "time": "3:05 pm - 4:25 pm"
                }, 
            ]
        "instructors": ["Jacob R  Eisenstein"], 
        "crn": "30062", 
        "section_id": "A"
     }
 ]
```
The sections attribute contains a list of section objects. Each section object has the following attributes

 - crn: the course registration number for the course, a 5 digit uid by semester
 - section_id: the 1-3(?) digit alphanumeric section identifier
 - a list of instructors for the section
 - a list of meeting objects with
     - instructor: a list of instructors for this meeting (yes there can be more than 1)
     - location: a string location
     - type: type of meeting, Lecture, self study, etc.
     - days: MTWRF for monday, tues, wednesday, thursday and friday
     - time: time range

## Extending Grouch
Much of grouch relies on scrapy, so familiarize yourself with scrapy, and realize that scrapy has tools to do things like serialize to a database (using the item pipeline and middlewear). Further, if you want to add or change how something is scraped, most of that has been compartmentalized quite well. Want courses to have another attribute, the plain language description that OSCAR provides. Its a 3 line change, one in `grouch/items.py`, one in `grouch/loaders.py` and one in `grouch/scrapers/oscar_scraper.py`.

## Contributing
 - Fork the repository here
 - `git clone`
 - `git branch dev`
 - `git checkout dev`
 - make your changes
 - write some tests, make sure they pass and that you test all added functionality
 - `git push origin dev`
 - submit a pull request
