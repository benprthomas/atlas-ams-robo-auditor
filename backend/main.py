import uvicorn
import debugpy
from .base import create_app

app = create_app()

debugpy.listen(("0.0.0.0", 5678))  # You can also use ("localhost", 5678)
print("🛠️ Debugger is listening on port 5678")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
