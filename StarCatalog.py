import cv2
from astropy.coordinates import SkyCoord, match_coordinates_sky
from astroquery.astrometry_net import AstrometryNet
from astroquery.gaia import Gaia
from astroquery.simbad import Simbad
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

import astropy.units as u
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astroquery.vizier import Vizier
from astropy.table import Table



import numpy as np

from StarFinder import find_stars, plot_detected_stars


def world_coordinates(img_path: str) -> WCS:
    # get world coordinates of the image
    ast = AstrometryNet()
    ast.api_key = 'xxsgfjptzhctedzp'
    # Perform plate solving using Astrometry.net
    solver = AstrometryNet()
    try_again = True
    submission_id = None

    while try_again:
        try:
            if not submission_id:
                wcs_header = solver.solve_from_image(img_path,
                                                  submission_id=submission_id, crpix_center=True)
            else:
                wcs_header = solver.monitor_submission(submission_id, solve_timeout=120)
        except TimeoutError as e:
            submission_id = e.args[1]
        else:
            # got a result, so terminate
            try_again = False
    im1 = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    points = find_stars(im1, method="blob")
    #wcs_header = solver.solve_from_source_list(points[1][:, 0], points[1][:, 1], image_width=im1.shape[1], image_height=im1.shape[0], solve_timeout=120)
    # Extract the WCS information from the header
    w = WCS(wcs_header)
    return w


def get_stars_names(points: np.ndarray, world_coordinates_system: WCS) -> np.ndarray:
    coords = world_coordinates_system.pixel_to_world(points[:, 0], points[:, 1])
    print(coords)
    # get the names of the stars from simbad
    result_table = Simbad.query_region(coords, radius=2.0 * u.arcmin)
    if result_table is not None:
        simbad_coords = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.hourangle, u.deg))
        # Continue with the rest of your code that relies on simbad_coords
    else:
        result_table = Table()
        simbad_coords = SkyCoord(ra=[0], dec=[0], unit=(u.hourangle, u.deg))
    # # # Match coordinates with result_table
    #simbad_coords = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.hourangle, u.deg))
    idx, sep2d, _ = match_coordinates_sky(coords, simbad_coords, nthneighbor=1)
    result = []
    for i in range(len(coords)):
        if i in idx and idx[i] < len(result_table):
            if sep2d[i].arcmin < 2.0:
                result.append(result_table[idx[i]]['MAIN_ID'])
            else:
                result.append("")
        else:
            result.append("")
    return result

def plot_star_name(img, points, names):
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10))
    ax.imshow(im1, cmap='gray')
    num = 1
    for p in enumerate(points, 1):
        x, y, r, b = points[num-1]
        ax.text(x, y, f"{names[num-1]}", color='b', fontsize=8, horizontalalignment='left', verticalalignment='baseline')
        ax.add_patch(plt.Circle((x, y), radius=r, edgecolor='r', facecolor='none'))
        num +=1

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    im1_path = "fr1.jpg"
    im1 = cv2.imread(im1_path, cv2.IMREAD_GRAYSCALE)
    points = find_stars(im1, method="blob")
    plot_detected_stars(im1, points[1])


    points_world_coordinates = world_coordinates(im1_path)
    names = get_stars_names(points[0], points_world_coordinates)
    plot_star_name(im1, points[1], names)
