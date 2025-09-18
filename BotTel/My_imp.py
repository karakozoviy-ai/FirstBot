#Токен бота
from BotToken import  BT
#Библиотеки для телеграма
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
#Сторонние библиотеки
from turtledemo.clock import current_day
import requests
from pprint import pprint
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont  # Импортируем Pillow
import io  # Для работы с изображением в памяти

