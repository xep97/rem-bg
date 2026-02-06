from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from bg_remove import remove_background

app = FastAPI(title="Background Remover")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Background Remover</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #143;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: #fff2;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                width: 320px;
            }
            input[type=file] {
                margin: 15px 0;
            }
            button {
                background: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 10px;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: #fffc;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Remove Image Background</h2>
            <form action="/remove-bg" method="post" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*" required />
                <br />
                <button type="submit">Upload & Remove</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/remove-bg")
async def remove_bg(image: UploadFile = File(...)):
    image_bytes = await image.read()
    output_image = remove_background(image_bytes)

    return StreamingResponse(
        output_image,
        media_type="image/png",
        headers={
            "Content-Disposition": "attachment; filename=removed_bg.png"
        }
    )
