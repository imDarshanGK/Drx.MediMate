import os
import json
import base64
from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
import google.generativeai as genai