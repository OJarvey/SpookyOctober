from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """
    Home page view for SpookyOctober
    """
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SpookyOctober</title>
            <style>
                body {
                    background-color: #1a1a1a;
                    color: #ff6600;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 1.2em;
                    color: #cccccc;
                }
            </style>
        </head>
        <body>
            <h1>🎃 SpookyOctober 🎃</h1>
            <p>Welcome to the Halloween Hackathon!</p>
            <p>Django + PostgreSQL + Heroku</p>
            <p><em>Ready for deployment!</em></p>
        </body>
        </html>
    """)
