from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from explorer.forms import ExplorerForm
from explorer.utils.explorer import get_spectral_access_services, get_spectral_graphic, get_spectral_graphic_2


def index(request):
    if request.method == 'POST':
        print("request", request)
        print("request post ", request.POST)

        service_type = request.POST.get("service_type", "")
        waveband = request.POST.get("waveband", "")
        spectral_access_services = get_spectral_access_services(waveband=waveband, servicetype=service_type)

        string_services = []
        for service in spectral_access_services:
            name = str(service.short_name)
            # string_services.append(name)
            string_services.append(service.short_name)

        services_table = spectral_access_services.to_table()['ivoid', 'short_name']

        form_cikti = service_type + waveband
        # return HttpResponseRedirect('/explorer/')
        context = {'form_cikti': form_cikti, 'spectral_access_services': spectral_access_services,
                   'services_table': services_table, 'string_services': string_services,
                   'service_type': service_type, 'waveband': waveband}
        return render(request, 'emplorer/index.html', context)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = ""

    sonuc = "sonuc"

    context = {'context_1': sonuc,}
    return render(request, 'emplorer/index.html', context)


def explorer2(request):
    if request.method == 'POST':
        print("request", request)
        print("request post ", request.POST)

        service_type = request.POST.get("service_type", "")
        waveband = request.POST.get("waveband", "")
        services = request.POST.get("services", "")

        sky_name = request.POST.get("sky_name", "")
        sky_dec = request.POST.get("sky_dec", "")
        sky_ra = request.POST.get("sky_ra", "")
        sky_obstime = request.POST.get("sky_obstime", "")
        print("service_type",service_type)
        print("waveband", waveband)
        print("services", services)

        print("sky_name", sky_name)
        print("sky_dec", sky_dec)
        print("sky_ra", sky_ra)
        print("sky_obstime", sky_obstime)

        if service_type and waveband and services and sky_name:
            graphic_data = get_spectral_graphic(servicetype=service_type, waveband=waveband, sky_name=sky_name,
                                                service_name=services)
            context = {'service_type': service_type, 'waveband': waveband, 'services': services,
                       'graphic_data': graphic_data}
            return render(request, 'emplorer/explorer_2.html', context)

        if service_type and waveband and services and sky_dec and sky_ra and sky_obstime:
            graphic_data = get_spectral_graphic_2(servicetype= service_type , waveband =waveband , service_name = services, sky_dec = sky_dec, sky_ra= sky_ra, sky_obstime= sky_obstime)
            context = {'service_type': service_type, 'waveband': waveband, 'services': services,
                       'graphic_data': graphic_data}
            return render(request, 'emplorer/explorer_2.html', context)

        if service_type and waveband and services:
            context = {'service_type': service_type, 'waveband': waveband, 'services': services}
            return render(request, 'emplorer/explorer_2.html', context)


    else:
        data2 = ""

    sonuc = "sonuc"
    ##data = get_spectral_graphic(servicetype="ssa", waveband="x-ray", service_name="Delta Ori")
    data = ""

    context = {'context_1': sonuc, 'graphic': data}
    return render(request, 'emplorer/explorer_2.html', context)


def mainPage(request):
    return render(request, 'index.html')
