# Pricetracker

Pricetracker is a tool for tracking prices of products in online stores. It allows users to save products they want to track and provides them with up-to-date information about the prices of those products.

## [Price tracker site](https://price-tracker-76kz.onrender.com/)

## Features

- Compare prices of products from multiple stores
- Displaying product’s price history
- scanning barcode for fast product search

![barcode example](images/barcode_example.gif)

## Technologies used:
 - Python
 - Django
 - Tailwind CSS
 - PostgreSQL
 - [Barcodescanner lib](https://github.com/mebjas/html5-qrcode)
 - [Chart.js lib](https://github.com/chartjs/Chart.js)
 - [Splide lib](https://github.com/Splidejs/splide)
 
## Installation dev

1. Clone repo
2. set '.env' file, example is availbe in '.env.example' 

2. Install dependencies
```bash
pip install -r requirements.txt
```
3. makemigrations to database
```bash
python manage.py makemigrations
```
4. run server
```bash
python manage.py runserver
```
5. install js dependencies
```bash
npm install
```
6. watch css files for changes
```bash
npm run tailwind
```
