import cv2
from astropy.coordinates import SkyCoord, match_coordinates_sky
from astroquery.astrometry_net import AstrometryNet
from astroquery.simbad import Simbad

import astropy.units as u
import matplotlib.pyplot as plt
from astropy.wcs import WCS

import numpy as np

from StarFinder import find_stars, plot_detected_stars


def __world_coordinates(img_path: str) -> WCS:
    # get world coordinates of the image
    ast = AstrometryNet()
    ast.api_key = 'xxsgfjptzhctedzp'
    # Perform plate solving using Astrometry.net
    solver = AstrometryNet()
    wcs_header = solver.solve_from_image(img_path, solve_timeout=120)
    # Extract the WCS information from the header
    w = WCS(wcs_header)
    return w


def get_stars_names(points: np.ndarray, world_coordinates_system: WCS) -> np.ndarray:
    points_world_coordinates = world_coordinates_system.all_pix2world(points, 1)
    coords = SkyCoord(ra=points_world_coordinates[:, 0], dec=points_world_coordinates[:, 1],
                      unit=(u.deg, u.deg),
                      frame='icrs')
    # result_table = Ned.query_region(coords, radius=0.05 * u.deg)
    # print(result_table)
    result_table = Simbad.query_region(coords, radius=0.1 * u.deg)
    # Match coordinates with result_table
    simbad_coords = SkyCoord(ra=result_table['RA'], dec=result_table['DEC'], unit=(u.deg, u.deg), frame='icrs')
    # idx, d2d, _ = coords.match_to_catalog_sky(matched_coords)
    # idx, d2d, _ = matched_coords.search_around_sky(coords, 1 * u.deg)
    idx, sep2d, _ = match_coordinates_sky(coords, simbad_coords)
    # Extract relevant information from matched rows
    # _, sources = np.unique(idx, return_index=True)
    source_names = result_table[idx]['MAIN_ID']
    return source_names


def plot_star_name(img, points, names):
    fig, ax = plt.subplots(ncols=1, figsize=(10, 10))
    ax.imshow(im1, cmap='gray')
    num = 1
    for p in enumerate(points, 1):
        x, y, r, b = points[num - 1]
        ax.text(x, y, f"{names[num - 1]}", color='b', fontsize=8, horizontalalignment='left',
                verticalalignment='baseline')
        ax.add_patch(plt.Circle((x, y), radius=r, edgecolor='r', facecolor='none'))
        num += 1

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    im1_path = "ST_db1.jpg"
    im1 = cv2.imread(im1_path, cv2.IMREAD_GRAYSCALE)
    points = find_stars(im1, method="blob")
    plot_detected_stars(im1, points[1])

    points_world_coordinates = __world_coordinates(im1_path)
    names = get_stars_names(points[0], points_world_coordinates)
    plot_star_name(im1, points[1], names)
