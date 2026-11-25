.PHONY: api ui

api:
	uvicorn api.main:app --reload

ui:
	streamlit run ui/app.py
