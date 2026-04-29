# AI Usage

## Tools Used
- Claude (Anthropic)

## Tasks AI Assisted With
- Explaining Flask route structure and how parameterized queries prevent SQL injection
- Suggesting which indexes to create based on the application's query patterns
- Explaining transaction concepts (isolation levels, FOR UPDATE locks, rollback)
- Drafting the transaction code for request_ride and update_request routes
- Guiding the GitHub setup process

## How Output Was Verified and Modified
- Ran all CREATE INDEX statements in MySQL Workbench and confirmed with SHOW INDEX
- Ran EXPLAIN queries in MySQL Workbench to verify indexes are actually being used
- Tested every route in the browser (add student, add driver, post ride,
  request ride, accept/decline) to confirm the app works correctly
- Read and understood each transaction code block before adding it to app.py
- Cross-referenced MySQL documentation on isolation levels to verify correctness
- Reviewed all AI suggestions and confirmed they matched our database schema