import astropy.units as u

from heinlein import Region, load_dataset

des_center = (13.4349, -20.2091)
hsc_center = (141.23246, 2.32358)
cfht_center = (35.2, -6.4)
radius = 120 * u.arcsecond


def test_cfht():
    print("TESTING CFHT")
    d = load_dataset("cfht")
    a = d.cone_search(cfht_center, radius, dtypes=["catalog", "mask"])
    cat = a["catalog"]
    mask = a["mask"]
    print(mask.mask(cat))
    print(a)


def test_des():
    print("TESTING DES")
    d = load_dataset("des")
    a = d.cone_search(des_center, radius, dtypes=["catalog", "mask"])
    cat = a["catalog"]
    mask = a["mask"]
    print(mask.mask(cat))
    print(a)


def test_hsc():
    print("TESTING HSC")
    d = load_dataset("hsc")
    a = d.cone_search(hsc_center, radius, dtypes=["catalog", "mask"])
    cat = a["catalog"]
    mask = a["mask"]
    print(mask.mask(cat))
    print(a)


test_cfht()
test_des()
test_hsc()
