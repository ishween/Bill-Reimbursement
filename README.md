# Bill-Reimbursement

## What is Bill-Reimbursemt about ?
This will help a company to maintain bill records of employees and easily accept or reject them.  
This project is aimed at providing companies a outsourced service for a bill submission / reimbursement system without going into the complexity & costs of doing the same themselves. Most companies require more or less a system where the employees can submit their bills which can then be reviewed by their managers/concerned people so that the bills can be reimbursed. The employee should be able to track the status of his reimbursement claim at any point of time. Similarly the concerned people should have the ability to see the submitted bills along with the proofs and accept/reject them.  
Since this part is common to most companies and the only variation is the reimbursement amount & departments within a company, this project can serve as a prototype for such a system.

---

## Live Demo
This project is currently live using the __Heroku__ deployment service.  
https://billreimbursement.herokuapp.com/

---

## Technologies

- Python (Flask Framework)
- MongoDB for database (Hosted)
- SendGrid for E-Mail service
- Jinja for Server-Templating

---

## Major Entities
This system includes three major entities:  

- **Admin** - Manages departments their bill types, managers and employees of the company.  
- **Director** - Reviewm Accept, Reject bills of managers under their department.  
- **Manager** - Review, Accept or Reject bills of employee under their department.  
              - Add, Update or Delete bills for reimbursment.  
- **Employee** - Add, Update or Delete bills for reimbursement.  

---

## Other Info
- Once Admin enters managers and employees a mail is sent containing their login credentials. 
- After first login, manager and employee can set their desired password.  
- Sorting and Filtering are provided for easy display of information according to user.  
