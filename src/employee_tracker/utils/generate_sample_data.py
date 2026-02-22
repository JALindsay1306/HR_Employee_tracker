from datetime import date

from employee_tracker.domain.tracker import Tracker
from employee_tracker.storage.storage import DATA_DIR


def generate_sample_data() -> Tracker:
    tracker = Tracker()


    DATA_DIR.mkdir(parents=True, exist_ok=True)

    tracker.create_permission("payroll")
    tracker.create_permission("finance_edit")
    tracker.create_permission("hr_read")
    tracker.create_permission("hr_write")
    tracker.create_permission("it_admin")

    e1 = tracker.create_employee(
        name="Alice Johnson",
        role="HR Manager",
        start_date=date(2021, 4, 12),
        salary=52000,
        address="10 King Street, London",
        permissions=["hr_read","hr_write"],
    )
    e2 = tracker.create_employee(
        name="Ben Carter",
        role="Software Engineer",
        start_date=date(2022, 9, 5),
        salary=65000,
        address="22 Baker Street, London",
        permissions=["it_admin"],
    )
    e3 = tracker.create_employee(
        name="Chloe Singh",
        role="Payroll Specialist",
        start_date=date(2020, 1, 20),
        salary=48000,
        address="18 High Road, Croydon",
        permissions=["payroll", "hr_read"],
    )
    e4 = tracker.create_employee(
        name="Daniel Evans",
        role="Customer Support",
        start_date=date(2023, 2, 1),
        salary=32000,
        address="3 Station Road, Watford",
        permissions=[],
    )
    e5 = tracker.create_employee(
        name="Evelyn Brown",
        role="Finance Analyst",
        start_date=date(2021, 11, 15),
        salary=56000,
        address="77 Queensway, London",
        permissions=["payroll"],
    )
    e6 = tracker.create_employee(
        name="Frank Mitchell",
        role="Backend Developer",
        start_date=date(2020, 6, 8),
        salary=68000,
        address="14 Elm Street, Manchester",
        permissions=["it_admin"],
    )

    e7 = tracker.create_employee(
        name="Grace Turner",
        role="Recruitment Officer",
        start_date=date(2022, 3, 14),
        salary=45000,
        address="22 Victoria Road, Birmingham",
        permissions=["hr_read"],
    )

    e8 = tracker.create_employee(
        name="Hannah Patel",
        role="Data Analyst",
        start_date=date(2021, 9, 30),
        salary=59000,
        address="5 Riverside Drive, Leeds",
        permissions=["it_admin"],
    )

    e9 = tracker.create_employee(
        name="Ian Robertson",
        role="Systems Administrator",
        start_date=date(2019, 11, 18),
        salary=72000,
        address="31 Hill Lane, Bristol",
        permissions=["it_admin"],
    )

    e10 = tracker.create_employee(
        name="Jasmine Clark",
        role="Payroll Assistant",
        start_date=date(2023, 1, 9),
        salary=40000,
        address="9 Oak Avenue, Liverpool",
        permissions=["payroll"],
    )

    e11 = tracker.create_employee(
        name="Kevin O'Neill",
        role="DevOps Engineer",
        start_date=date(2020, 8, 3),
        salary=70000,
        address="18 Park Crescent, Nottingham",
        permissions=["it_admin"],
    )

    e12 = tracker.create_employee(
        name="Laura Simmons",
        role="HR Advisor",
        start_date=date(2021, 5, 21),
        salary=48000,
        address="44 Maple Street, Sheffield",
        permissions=["hr_read", "hr_write"],
    )

    e13 = tracker.create_employee(
        name="Marcus Reed",
        role="Frontend Developer",
        start_date=date(2022, 7, 12),
        salary=63000,
        address="7 Grove Lane, Oxford",
        permissions=["it_admin"],
    )

    e14 = tracker.create_employee(
        name="Natalie Hughes",
        role="Financial Controller",
        start_date=date(2018, 4, 2),
        salary=82000,
        address="11 Harbour Road, Southampton",
        permissions=["payroll"],
    )

    e15 = tracker.create_employee(
        name="Oliver Grant",
        role="IT Support Technician",
        start_date=date(2023, 6, 5),
        salary=35000,
        address="62 Brook Street, Leicester",
        permissions=["it_admin"],
    )

    e16 = tracker.create_employee(
        name="Priya Shah",
        role="Business Analyst",
        start_date=date(2020, 2, 17),
        salary=61000,
        address="27 Station Road, Reading",
        permissions=["hr_read"],
    )

    e17 = tracker.create_employee(
        name="Quentin Moore",
        role="Security Engineer",
        start_date=date(2019, 10, 28),
        salary=75000,
        address="3 Mill Lane, Cambridge",
        permissions=["it_admin"],
    )

    e18 = tracker.create_employee(
        name="Rachel Adams",
        role="Customer Success Manager",
        start_date=date(2021, 12, 1),
        salary=54000,
        address="88 Market Street, York",
        permissions=[],
    )

    e19 = tracker.create_employee(
        name="Samuel Davies",
        role="Accountant",
        start_date=date(2017, 9, 19),
        salary=60000,
        address="16 Bridge Road, Cardiff",
        permissions=["payroll"],
    )

    e20 = tracker.create_employee(
        name="Tara Wilson",
        role="UX Designer",
        start_date=date(2022, 4, 25),
        salary=58000,
        address="29 Queen Street, Newcastle",
        permissions=[],
    )

    e21 = tracker.create_employee(
        name="Umar Khan",
        role="Technical Architect",
        start_date=date(2016, 3, 7),
        salary=90000,
        address="2 Kingsway, Edinburgh",
        permissions=[],
    )

    e22 = tracker.create_employee(
        name="Victoria Lewis",
        role="HR Administrator",
        start_date=date(2023, 8, 14),
        salary=38000,
        address="13 Chapel Street, Coventry",
        permissions=["hr_read"],
    )

    e23 = tracker.create_employee(
        name="William Scott",
        role="Product Manager",
        start_date=date(2020, 11, 23),
        salary=77000,
        address="40 City Road, Glasgow",
        permissions=[],
    )

    e24 = tracker.create_employee(
        name="Xenia Brooks",
        role="Compliance Officer",
        start_date=date(2019, 1, 15),
        salary=62000,
        address="6 Manor Close, Plymouth",
        permissions=["hr_read", "payroll"],
    )

    e25 = tracker.create_employee(
        name="Yusuf Ali",
        role="Network Engineer",
        start_date=date(2021, 7, 6),
        salary=69000,
        address="55 Green Lane, Derby",
        permissions=["it_admin"],
    )

    d1 = tracker.create_department(
        name="Human Resources",
        description="Hiring, onboarding, policies",
        head_of_department=e1.id,
        parent_department=None,
        members=[e1.id, e7.id, e12.id, e22.id, e24.id],
    )

    d2 = tracker.create_department(
        name="Engineering",
        description="Product development and systems",
        head_of_department=e21.id,  # Technical Architect
        parent_department=None,
        members=[e2.id, e6.id, e8.id, e13.id, e16.id, e20.id, e21.id, e23.id],
    )

    d3 = tracker.create_department(
        name="Finance",
        description="Budgeting, payroll, reporting",
        head_of_department=e14.id,  # Financial Controller
        parent_department=None,
        members=[e3.id, e5.id, e10.id, e14.id, e19.id],
    )

    d4 = tracker.create_department(
        name="Support",
        description="Customer support operations",
        head_of_department=e18.id,  # Customer Success Manager
        parent_department=None,
        members=[e4.id, e18.id],
    )

    d5 = tracker.create_department(
        name="IT Operations",
        description="Infrastructure, support, security, networks",
        head_of_department=e9.id,  # Systems Administrator
        parent_department=None,
        members=[e9.id, e11.id, e15.id, e17.id, e25.id],
    )

    tracker.save_to_storage() 

    return tracker

if __name__ == "__main__":
    generate_sample_data()
    print(f"Same CSVs written to: {DATA_DIR}")
