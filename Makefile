run:
	uvicorn server.main:app --reload

dbcon:
	sqlite3 db.sqlite3
