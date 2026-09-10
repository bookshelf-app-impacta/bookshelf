"""Ponto de entrada. E o que a variavel FLASK_APP aponta."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
