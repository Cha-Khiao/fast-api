from app.main import app
from mangum import Mangum

# Mangum ทำให้ FastAPI ทำงานบน AWS Lambda / Serverless ได้
handler = Mangum(app)
