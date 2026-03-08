## Introduction

Congratulations on making it to our project stage. This take-home project gives you the opportunity to showcase your real-world coding skillset. 

We encourage the use of AI tools, but we will ask you detailed questions about your implementation, so make sure you have reviewed and can explain all code that AI has written. 

You can choose the tech stack that allows you to showcase your best work. Yellow’s stack uses a FastAPI backend, Postgres database and Vue.js frontend (with Quasar: [https://quasar.dev](https://quasar.dev/))

Please spend **no more than 5 hours** on this project. 

## Deliverables

- A public Github link with your code
- A video demo (using a tool like Loom: [https://loom.com](http://loom.com/)) of your UI flow.
- (Optional) A live URL with a demo of your website

Email these back to the person who sent you the project.

## The challenge

Create a simple sign up form for a user to apply for a loan with Yellow. The form should capture:

- Biographical information (name, ID number, birthday)
- Income information (How much they earn with a supporting proof document)
- A way to choose a specific phone with prices (You can make up your own phone database with prices.)

### Functionality

- Assume all applications happen in South Africa, and validate that IDs are valid SA ID numbers. ID numbers should be unique - multiple applications from the same ID number should not be allowed.
- Only people age 18-65 (inclusive) should be allowed to apply
- The pricing for each phone should include:
    - **A “cash” price:** how much the phone would cost if they were to buy it without finance
    - **A deposit percent:** how much of the cash price is due at purchase time to buy the phone - like a downpayment on a house
    - ⇒ This will allow you to calculate the loan principal - how much we’re loaning the customer (`loanPrincipal = cashPrice * (1-depositPercent)`)
    - **An interest rate:** how much annual interest we charge on the loan principal
    - ⇒ Using this information, calculate the total loan amount ( `loanAmount = loanPrincipal * (1+interestRate)`)
- Assume all loans are for one year (360 days) and require daily payment. You should then show the daily price of each phone (`loanAmount / 360`)
- To see an example implementation of this UI, visit [https://yellow.africa/phones/pricing](https://yellow.africa/phones/pricing/mw)

### Data considerations

At a minimum, you should implement:

- An application object that stores user information and phone choice
- A phone object that contains the pricing information

### UX considerations

- Most applications will happen on a mobile phone, so make sure your design is mobile-friendly
- Make your best determination about whether the form is best as one long page or as multiple pages.
- Make sure you include both frontend and backend validations for input data

## Extras

If you find that you’ve finished early, you can try to implement any of the following. Play to your strengths!

- **Live demo**: deploy your code to a hosting platform such as [fly.io](http://fly.io) and send a URL link
- **UI styling**: make your UI match Yellow’s web style
- **Risk scoring**: This requires a multi-step flow. Using the user’s birthday, implement a risk score like this:
    - Age 18-30: risk group 1
    - Age 31-50: risk group 2
    - Age 51-65: risk group 3
    - Then update the phone pricing so that there is a different interest rate and/or deposit percent per risk group, and the user is shown the pricing based off of their risk score. In this case, the user should not be allowed to go back and change their age once they submit it.
- **Affordability**: Using the income information, only show phones where the **monthly income** of the customer is > 10x the **monthly price** of the phone.
- **Payment**: Checkout with a mock payment, keeping track of applications started vs. completed.

## Questions

We encourage you to ask questions before you begin by email. This will not count against your 5 hour time limit. 

Good luck!