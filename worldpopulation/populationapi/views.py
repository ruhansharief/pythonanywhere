from django.shortcuts import render
from django.http import HttpResponse
import json
from populationapi import utils
from  populationapi.mixins import HttpResponseMixin
import datetime
from populationapi import web_scrapper
# Create your views here.


def main_method(request):

    data = request.body
    #import pdb;pdb.set_trace()
    if data is not None:
        request_data = utils.valid_json(data)

        if request_data is None:
            msg = json.dumps({'message':'Please provide the data in vaild JSON Format'})
            return HttpResponseMixin.render_to_http_response(msg, status=400)

        requested_country = request_data.get('country')
        if requested_country is None:
            msg = json.dumps({'message':'Country is mandatory information required to retrive the data. Please proivde country.'})
            return HttpResponseMixin.render_to_http_response(msg, status=400)

        # if 'year' not in request_data.keys() and 'city' not in request_data.keys():
        #     msg = json.dumps({'message':'Please provide either the year or the city to get the data'})
        #     return HttpResponseMixin.render_to_http_response(msg, status=400)

        
        
        requested_year = request_data.get('year')
        requested_city = request_data.get('city')

        current_year = datetime.datetime.now().year
        if requested_year:
            if int(requested_year) <= current_year:
                data = historical_data(requested_country, requested_year)
                json_data = json.dumps(data)
                return HttpResponseMixin.render_to_http_response(json_data, status=200)
            else:
                data = forecast_data(requested_country, requested_year)
                if data is None:
                    msg = json.dumps({'message':'If you want forecast information then the year provided should be within 30 years limit of current year {} and should be multiple of 5'.format(current_year)})
                    return HttpResponseMixin.render_to_http_response(msg, status=400)
                else:
                    json_data = json.dumps(data)
                    return HttpResponseMixin.render_to_http_response(json_data, status=200)


        elif requested_city:
            data = city_data(requested_country, requested_city)
            if data is None:
                    msg = json.dumps({'message':'The provided country data is not present in the country\'s city list/ it is not part of the country.'})
                    return HttpResponseMixin.render_to_http_response(msg, status=400)
            else:
                json_data = json.dumps(data)
                return HttpResponseMixin.render_to_http_response(json_data, status=200)


        else:
            data = historical_data(requested_country)
            json_data = json.dumps(data)
            return HttpResponseMixin.render_to_http_response(json_data, status=200)

    else:
        msg = json.dumps({'message':'Please provide the country for which you need information'})
        return HttpResponseMixin.render_to_http_response(msg, status=400)

def historical_data(requested_country, requested_year=None):

    returned_data = web_scrapper.get_data(table_number=1, requested_country=requested_country)
    if requested_year:
        for item in returned_data:
            if requested_year == item['Year']:
                return item
    return returned_data

def forecast_data(requested_country, requested_year):
    """
    The requested year should be within 30 years from the current year
    and the should be multiples of 5
    """
    requested_year = requested_year
    current_year = datetime.datetime.now().year
    if int(requested_year) <= (current_year + 30) and int(requested_year) % 5 == 0:
        returned_data = web_scrapper.get_data(table_number=2, requested_country=requested_country)
        
        for item in returned_data:
            if requested_year == item['Year']:
                return item
    else:
        return None

def city_data(requested_country, requested_city=None):
    returned_data = web_scrapper.get_data(table_number=3,requested_country=requested_country)

    if requested_country.lower() == 'all':
        return returned_data
    else:
        for item in returned_data:
            if requested_city.lower() == item['CITY NAME'].lower():
                return item
    return None

