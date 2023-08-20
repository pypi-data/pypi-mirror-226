import datetime
import time
import glob
from copy import deepcopy
import datetime
from astropy.time import Time
import warnings


def ezcount(fmt="", delta_t=3):
    print("---------- time ---------- \t count \t incr")
    c0 = 0
    while True:
        c1 = len(glob.glob(fmt))
        print(datetime.datetime.now(), "\t", c1, "\t", c1 - c0)
        c0 = deepcopy(c1)
        time.sleep(delta_t)
    return


def YQ():
    warnings.filterwarnings("ignore")
    t0 = Time("2022-02-24T22:49:00", format="isot")
    t1 = Time(datetime.datetime.now())
    dt = t1 - t0
    print("{:.7f} days since YQ.".format(dt.value))


def run5km():
    warnings.filterwarnings("ignore")
    t0 = Time("2022-08-30T12:00:00", format="isot")
    t1 = Time(datetime.datetime.now())
    dt = t0 - t1
    print("{:.7f} days .".format(dt.value))


def tianhao():
    """ time away from H. Tian's first house """
    warnings.filterwarnings("ignore")
    t0 = Time(datetime.datetime.now())
    t1 = Time("2032-02-11T08:00:00", format="isot")
    dt = t1 - t0
    print("{:.5f} days away from H. Tian's first big house. ".format(dt.value))


def ads(lib_id="v89_ChWTSKOUFvCpxOm6Tg", token="6OEonb0MGO6EzpatpzomBSJrXXbJziaiz6qzPTQn", tofile=None, rows=500,
        sep="%"):
    """

    Parameters
    ----------
    lib_id:
        ads library ID
    token:
        ADS API token, get it from https://ui.adsabs.harvard.edu/user/settings/token
    tofile:
        if not None, save to text file
    rows:
        max entries
    sep:
        detaults to "%" (a line starts with "%")
        the content above the sep line will be reserved during the update

    Returns
    -------
    if tofile is None, return bibtex, else nothing

    """
    import os
    import requests
    import json
    # get the data for a specific library
    r = requests.get("https://api.adsabs.harvard.edu/v1/biblib/libraries/{}".format(lib_id),
                     headers={"Authorization": "Bearer " + token}, params={"rows": rows})
    bibtags = r.json()["documents"]

    # get the AASTeX entries for multiple bibcodes
    payload = {"bibcode": bibtags,
               "sort": "year desc"}
    r = requests.post("https://api.adsabs.harvard.edu/v1/export/bibtex",
                      headers={"Authorization": "Bearer " + token, "Content-type": "application/json"},
                      data=json.dumps(payload))
    print(r.json()["msg"])
    bibtex = r.json()["export"]

    if tofile is None:
        return bibtex
    else:
        if not os.path.exists(tofile):
            # if file does not exist
            with open(tofile, "w+") as f:
                f.write(bibtex)
        else:
            # if file exists
            with open(tofile, "r") as f:
                old = f.readlines()
            reserved = []
            for _i, _ in enumerate(old):
                if _.startswith(sep):
                    reserved = old[:_i + 1]
            # remove file
            os.remove(tofile)
            # write a new file
            with open(tofile, "w+") as f:
                f.writelines(reserved)
                f.writelines(["\n", ])
                f.writelines(bibtex)
        print("@Bo: bibtex saved to {}\n".format(tofile))
        return
