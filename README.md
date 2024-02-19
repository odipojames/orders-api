# Savana Technical Challange

Vercel Staging URL - https://orders-api-chi.vercel.app/api/v1/
## End points:
***
   * https://orders-api-chi.vercel.app/api/v1/auth/register/
   * https://orders-api-chi.vercel.app/api/v1/auth/login/
   * https://orders-api-chi.vercel.app/api/v1/customers/  (for post and get)
   * https://orders-api-chi.vercel.app/api/v1/customers/id/
   * https://orders-api-chi.vercel.app/api/v1/ordesr/  (for post and get)
   * https://orders-api-chi.vercel.app/api/v1/orders/id/
### How to run locally
Clone the project in your machine and open  it on CMD or Terminal
, please do the following:
`ensure that python3.9 is installed in your machine`
`create a virtual enviroment and activate it`
`pip install -r requirements.txt`
`create .env file in the root directory and provide enviroment variables, example check .env.example file`
`python manage.py runserver`
`open the running port in your browser to interact with API documentation`

### How to run with Docker
* `ensure docker is installed in your machine`
* `navigate or cd to cloned project and run command:`
* `docker compose up -d ordersapi`
* `open app on localhost:8000 in your browser to interact with api end points`

Once you have run these commands, you're good to go.

