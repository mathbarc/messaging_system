from messaging_api.app import app
import uvicorn

def main():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000
    )

if __name__ == "__main__":
    
    main()