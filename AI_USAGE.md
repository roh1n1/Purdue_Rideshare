# AI Usage

## Tools Used
- Claude (Anthropic)

## Tasks AI Assisted With
- Generating boilerplate Flask route structure and Jinja2 templates
- Writing and debugging SQL JOIN queries for the home page and report page
- Suggesting index strategy based on query patterns in the application
- Drafting transaction logic with appropriate isolation levels
- Guiding the GitHub setup process

## How Output Was Verified and Modified
- All SQL queries were tested manually against the MySQL database in Workbench
- Indexes were confirmed with EXPLAIN SELECT to verify they were being used
- Flask routes were tested end-to-end in the browser
- MySQL documentation was consulted to verify isolation level behavior
- AI-suggested code was reviewed and modified to fit our schema
- Ran all CREATE INDEX statements in MySQL Workbench and confirmed with SHOW INDEX
- Ran EXPLAIN queries in MySQL Workbench to verify indexes are actually being used
- Tested every route in the browser (add student, add driver, post ride,
  request ride, accept/decline) to confirm the app works correctly
- Read and understood each transaction code block before adding it to app.py
- Cross-referenced MySQL documentation on isolation levels to verify correctness
- Reviewed all AI suggestions and confirmed they matched our database schema