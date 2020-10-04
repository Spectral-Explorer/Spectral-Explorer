import base64
from io import BytesIO

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
# matplotlib inline

import requests, io

from astropy.table import Table
import astropy.io.fits as fits
from astropy.coordinates import SkyCoord
# For downloading files
from astropy.utils.data import download_file

import pyvo as vo
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames

# There are a number of relatively unimportant warnings that show up, so for now, suppress them:
import warnings

warnings.filterwarnings("ignore", module="astropy.io.votable.*")
warnings.filterwarnings("ignore", module="pyvo.utils.xml.*")


def get_spectral_access_services(servicetype, waveband):
    services = vo.regsearch(servicetype=servicetype, waveband=waveband)

    return services


def get_spectral_graphic(servicetype, waveband, service_name, sky_name):
    services = get_spectral_access_services(servicetype, waveband)

    chandra_service = [s for s in services if service_name in s.short_name][0]
    var_access_url = chandra_service.access_url
    print("var_access_url", var_access_url)

    delori = SkyCoord.from_name(sky_name)

    spec_tables = chandra_service.search(pos=delori, diameter=0.1)
    file_name = download_file(spec_tables[0].getdataurl(), cache=True)
    hdu_list = fits.open(file_name)
    spec_table = Table(hdu_list[1].data)


    matplotlib.rcParams['figure.figsize'] = (12, 10)

    for i in range(len(spec_table)):

        ax = plt.subplot(6, 2, i + 1)
        pha = plt.plot(spec_table['CHANNEL'][i], spec_table['COUNTS'][i])
        ax.set_yscale('log')

        if spec_table['TG_PART'][i] == 1:
            instr = 'HEG'
        if spec_table['TG_PART'][i] == 2:
            instr = 'MEG'
        if spec_table['TG_PART'][i] == 3:
            instr = 'LEG'

        ax.set_title("{grating}{order:+d}".format(grating=instr, order=spec_table['TG_M'][i]))

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

    return graphic

def get_spectral_graphic_2(servicetype, waveband, service_name, sky_dec, sky_ra, sky_obstime):
    services = get_spectral_access_services(servicetype, waveband)

    chandra_service = [s for s in services if service_name in s.short_name][0]
    var_access_url = chandra_service.access_url
    print("var_access_url", var_access_url)

    from astropy.coordinates import Angle, Latitude, Longitude  # Angles
    import astropy.units as u
    from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
    dec = np.array([4.5, 5.2, 6.3]) * u.deg  # Astropy Quantity
    print("dec")
    ra = Longitude([1, 2, 3], unit=u.deg)

    delori = SkyCoord(frame=ICRS, ra=ra, dec=dec, obstime='2001-01-02T12:34:56')
    print("delori")

    # spec_tables = chandra_service.search(pos=delori,diameter=0.1)
    spec_tables = chandra_service.search()

    file_name = download_file(spec_tables[0].getdataurl(), cache=True)
    hdu_list = fits.open(file_name)
    spec_table = Table(hdu_list[1].data)


    matplotlib.rcParams['figure.figsize'] = (12, 10)

    for i in range(len(spec_table)):

        ax = plt.subplot(6, 2, i + 1)
        pha = plt.plot(spec_table['CHANNEL'][i], spec_table['COUNTS'][i])
        ax.set_yscale('log')

        if spec_table['TG_PART'][i] == 1:
            instr = 'HEG'
        if spec_table['TG_PART'][i] == 2:
            instr = 'MEG'
        if spec_table['TG_PART'][i] == 3:
            instr = 'LEG'

        ax.set_title("{grating}{order:+d}".format(grating=instr, order=spec_table['TG_M'][i]))

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

    return graphic


"""
for servic in services:
    print("for : ", servic.short_name)

cikti_1 = services.to_table()['ivoid', 'short_name']

print("cikti_1", cikti_1)
"""
