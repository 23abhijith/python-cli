import click

from flask import jsonify
import requests
import geocoder
import json

@click.group(help="CLI tool to check weather")
def cli():
    pass

@click.command()
def weatherForMe():
    currentLocation = geocoder.ip('me').latlng
    response = json.loads(requests.get('https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m&temperature_unit=fahrenheit'.format(currentLocation[0], currentLocation[1])).text)
    times = response.get('hourly').get('time')
    temps = response.get('hourly').get('temperature_2m')
    g = geocoder.osm([currentLocation[0], currentLocation[1]], method='reverse')
    tempsTime = {}
    tempsTime['address'] = g.json['address']
    weather = {}
    for idx in range(len(times)):
        weather[times[idx]] = temps[idx]
    tempsTime['weather'] = weather
    return click.echo(tempsTime)

@click.command()
@click.option('--location', nargs=2, type=float)
def weatherForLocation(location):
    a, b = location
    response = json.loads(requests.get('https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m&temperature_unit=fahrenheit'.format(a, b)).text)
    times = response.get('hourly').get('time')
    temps = response.get('hourly').get('temperature_2m')
    g = geocoder.osm([a, b], method='reverse')
    tempsTime = {}
    tempsTime['address'] = g.json['address']
    weather = {}
    for idx in range(len(times)):
        weather[times[idx]] = temps[idx]
    tempsTime['weather'] = weather
    return click.echo(tempsTime)

cli.add_command(weatherForMe)
cli.add_command(weatherForLocation)
if __name__ == '__main__':
    cli()
