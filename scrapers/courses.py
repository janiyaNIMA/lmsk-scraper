from bs4 import BeautifulSoup
from config import Config
from .base import BaseScraper


class CourseScraper(BaseScraper):
    def __init__(self, session=None):
        super().__init__(session)

    def extract_course_details(self, course_url):
        print(f"  Scraping course details: {course_url}")
        try:
            response = self.session.get(course_url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract course full name
            header = soup.select_one(".page-header-headings h1, .coursename")
            full_name = header.get_text(strip=True) if header else "Unknown"
            
            sections = []
            # Moodle sections are usually li.section
            section_elems = soup.select("li.section, .section-container")
            
            for i, section in enumerate(section_elems):
                title_elem = section.select_one(".sectionname, h3, .section-title")
                title = title_elem.get_text(strip=True) if title_elem else f"Section {i}"
                
                activities = []
                # Activities are usually li.activity
                activity_elems = section.select("li.activity")
                for act in activity_elems:
                    name_elem = act.select_one(".instancename, .activityname")
                    link = act.find("a", href=True)
                    
                    # Try to determine type from classes
                    act_classes = " ".join(act.get("class", []))
                    act_type = "unknown"
                    for t in ["assign", "quiz", "resource", "folder", "url", "label", "forum", "page"]:
                        if t in act_classes:
                            act_type = t
                            break
                    
                    if name_elem or link:
                        name = name_elem.get_text(strip=True) if name_elem else ""
                        # Sometimes name has "File" or "Assignment" text inside, clean it
                        if name_elem and name_elem.select_one(".accesshide"):
                            name = name.replace(name_elem.select_one(".accesshide").get_text(), "").strip()
                            
                        activities.append({
                            "type": act_type,
                            "name": name,
                            "url": link["href"] if link else "",
                            "info": act.select_one(".contentwithoutlink, .availabilityinfo").get_text(strip=True) if act.select_one(".contentwithoutlink, .availabilityinfo") else ""
                        })
                
                if activities or title_elem:
                    sections.append({
                        "title": title,
                        "activities": activities
                    })
                    
            return {
                "full_name": full_name,
                "sections": sections
            }
        except Exception as e:
            print(f"  Error scraping course details: {e}")
            return {"full_name": "Error", "sections": []}

    def extract(self):
        print("Extracting courses...")
        response = self.session.get(Config.DASHBOARD_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        courses = []

        # 1. Course overview block
        course_items = soup.select(
            '[data-region="course-content"], .course-info-container, .dashboard-card'
        )
        for item in course_items:
            link = item.find("a", href=True)
            name_elem = item.select_one(".coursename, .course-name, h5")
            if link:
                name = (
                    name_elem.get_text(strip=True)
                    if name_elem
                    else link.get_text(strip=True)
                )
                courses.append(
                    {
                        "name": name,
                        "url": link["href"],
                        "id": (
                            link["href"].split("id=")[-1]
                            if "id=" in link["href"]
                            else ""
                        ),
                    }
                )

        # 2. Side bar or other lists if empty
        if not courses:
            for link in soup.select('a[href*="course/view.php?id="]'):
                name = link.get_text(strip=True)
                if name and len(name) > 3:
                    courses.append(
                        {
                            "name": name,
                            "url": link["href"],
                            "id": link["href"].split("id=")[-1],
                        }
                    )

        # Remove duplicates
        seen = set()
        unique_courses = []
        for c in courses:
            if c["id"] not in seen:
                unique_courses.append(c)
                seen.add(c["id"])
        
        # Now extract details for each course
        for course in unique_courses:
            details = self.extract_course_details(course["url"])
            course.update(details)

        return unique_courses
