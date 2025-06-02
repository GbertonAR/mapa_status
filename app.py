# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from checker import check_status, load_urls
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Página HTML
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🌐 Estado de los Sistemas</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #f0f4ff;
      color: #333;
    }
    h1 {
      text-align: center;
      padding: 1rem;
      font-size: 2rem;
      color: #274c77;
    }
    .container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
    }
    .card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 90%;
      max-width: 800px;
      padding: 1rem 1.5rem;
      background: white;
      border-left: 8px solid gray;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      transition: transform 0.2s ease-in-out;
    }
    .card:hover {
      transform: scale(1.01);
    }
    .url {
      font-weight: bold;
      color: #1a1a1a;
    }
    a.url {
      color: #1a73e8;
      text-decoration: none;
    }
    a.url:hover {
      text-decoration: underline;
    }
    .status {
      font-weight: bold;
      font-size: 1.2rem;
    }
    .ok     { border-color: #38b000; color: #38b000; }
    .offline { border-color: #d90429; color: #d90429; }
    .inactive { border-color: #f9a825; color: #f9a825; }
    .unresolvable { border-color: #616161; color: #616161; font-style: italic; }
  </style>
</head>
<body>
  <h1>🔍 Estado de los Sistemas</h1>
  <div class="container" id="statusContainer">
    <p>Cargando estados...</p>
  </div>

  <script>
    fetch('/status')
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("statusContainer");
        container.innerHTML = '';

        data.forEach(entry => {
          const card = document.createElement("div");
          card.classList.add("card");
          const urlHTML = `<span class="url"><a href="${entry.url}" target="_blank">${entry.url}</a></span>`;

          if (entry.status === 200) {
            card.classList.add("ok");
            card.innerHTML = `${urlHTML}<span class="status">✅ 200 OK</span>`;
          } else if (entry.status === "offline") {
            card.classList.add("offline");
            card.innerHTML = `${urlHTML}<span class="status">❌ Offline</span>`;
          } else if (entry.status.toString().startsWith("inactive")) {
            card.classList.add("inactive");
            card.innerHTML = `${urlHTML}<span class="status">⚠️ Inactivo</span>`;
          } else if (entry.status === "unresolvable") {
            card.classList.add("unresolvable");
            card.innerHTML = `${urlHTML}<span class="status">🛑 No resuelve (DNS)</span>`;
          } else {
            card.classList.add("inactive");
            card.innerHTML = `${urlHTML}<span class="status">❔ ${entry.status}</span>`;
          }

          container.appendChild(card);
        });
      })
      .catch(err => {
        document.getElementById("statusContainer").innerHTML = `<p style="color:red;">⚠️ Error al obtener el estado: ${err}</p>`;
      });
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return HTML_PAGE

@app.get("/status")
def get_status():
    try:
        urls = load_urls("./urls.txt")
        status = check_status(urls)
        return JSONResponse(content=status)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
