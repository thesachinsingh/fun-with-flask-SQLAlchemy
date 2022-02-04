from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

