if __name__ == "__main__":
    import astropy.units as u

    from heinlein import Region
    from heinlein.region.sampling import Sampler

    box = Region.box(0, 5, 5, 10)
    sampler = Sampler(box)
    sampler.get_circular_samples(45 * u.arcsec, 1000)
