# Property Management Backedn Api

create a backend for a property management system. the front end will be made later using Vue js. All the below functionality needs to be fully implemented in this project

### Apartmenrs

- List all apartments in the database
  - Pagination
  - Select specific fields in result
  - Limit number of results
  - Filter by fields
- Search apartments by radius from zipcode
  - Use a geocoder to get exact location and coords from a single address field
- Get single apartment
- Create new apartment
  - Authenticated users only
  - Must have the role "manager" or "admin"
  - Only one apartment per manager (admins can create more)
  - Field validation via Mongoose
- Upload a photo for apartment
  - Owner only
  - Photo will be uploaded to local filesystem
- Update apartments
  - Owner only
  - Validation on update
- Delete apartment
  - Owner only
- Calculate the average cost of all houses for an apartment
- Calculate the average rating from the reviews for an apartment

### houses

- List all houses for an apartment
- List all houses in general
  - Pagination, filtering, etc
- Get single house
- Create new house
  - Authenticated users only
  - Must have the role "manager" or "admin"
  - Only the manager or an admin can create a house for an apartment
  - managers can create multiple houses
- Update house
  - manager only
- Delete house

  - manager only

### Reviews

- List all reviews for an apartment
- List all reviews in general
  - Pagination, filtering, etc
- Get a single review
- Create a review
  - Authenticated users only
  - Must have the role "tenant" or "admin" (no publishers)
- Update review
  - Owner only
- Delete review
  - Owner only

### Users & Authentication

- Authentication will be done using JWT/cookies
  - JWT and cookie should expire in 30 days
- User registration
  - Register as a "tenant" or "manager"
  - Once registered, a token will be sent along with a cookie (token = xxx)
  - Passwords must be hashed
- Tenants login
  - Tenants can login with email and password
  - Plain text password will compare with stored hashed password
  - Once logged in, a token will be sent along with a cookie (token = xxx)
- tenant logout
  - Cookie will be sent to set token = none
- Get tenant
  - Route to get the currently logged in tenant (via token)
- Password reset (lost password)
  - Tenant can request to reset password
  - A hashed token will be emailed to the Tenant registered email address
  - A put request can be made to the generated url to reset password
  - The token will expire after 10 minutes
- Update tenant info
  - Authenticated tenant only
  - Separate route to update password
- Tenant CRUD
  - Admin or manager only
- Users can only be made admin by updating the database field manually

## Security

- Encrypt passwords and reset tokens
- Prevent cross site scripting - XSS
- Prevent NoSQL injections
- Add a rate limit for requests of 100 requests per 10 minutes
- Protect against http param polution
- Add headers for security (helmet)
- Use cors to make API public (for now)

## Documentation

- Use Postman to create documentation
- Use docgen to create HTML files from Postman
- Add html files as the / route for the api

## Deployment (Digital Ocean)

- Push to Github
- Create a droplet - https://m.do.co/c/5424d440c63a
- Clone repo on to server
- Use PM2 process manager
- Enable firewall (ufw) and open needed ports
- Create an NGINX reverse proxy for port 80
- Connect a domain name
- Install an SSL using Let's Encrypt

## Code Related Suggestions

- NPM scripts for dev and production env
- Config file for important constants
- Use controller methods with documented descriptions/routes
- Error handling middleware
- Authentication middleware for protecting routes and setting user roles
- Validation using Mongoose and no external libraries
- Use async/await (create middleware to clean up controller methods)
- Create a database seeder to import and destroy data
